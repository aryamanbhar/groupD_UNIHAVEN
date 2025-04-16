from django.db import models
from .services.geocoding_service import GeoCodingService
import math
from datetime import date
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.mail import send_mail
import smtplib
import sys
from email.mime.text import MIMEText

class CedarsSpecialist(models.Model):
    department = models.CharField(max_length=255, default='')  # added default

class Student(models.Model):
    student_id = models.CharField(max_length=255, unique=True, default='')
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255, default='')  # added default
    degree_type = models.CharField(max_length=100, default='')  # added default
    
class Accommodation(models.Model):
    property_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    type = models.CharField(max_length=100, default='')
    area = models.CharField(max_length=100, default='')
    owner_info = models.TextField(default='')  # fixed
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    # distance = models.FloatField(default=0.0)
    distance = JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    number_of_beds = models.IntegerField(default=0)  # fixed
    number_of_bedrooms = models.IntegerField(default=0)  # fixed
    availability_start = models.DateField(default=date.today)  # fixed
    availability_end = models.DateField(default=date.today)  # fixed
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved")
        ],
        default="available",
        max_length=50
    )

    def save(self, *args, **kwargs):
        # Automatically fetch latitude and longitude if not provided
        if not self.latitude or not self.longitude:
            geo_data = GeoCodingService.get_coordinates(self.name)
            if geo_data:
                self.latitude = geo_data['latitude']
                self.longitude = geo_data['longitude']

        self.distance = self.calculate_distance()
        super().save(*args, **kwargs)

    def calculate_distance(self):
        """
        Uses the Equirectangular approximation formula.
        """
        # Earth's radius in kilometers
        radius_of_earth_km = 6371

        # HKU campuses with their latitudes and longitudes
        HKU_CAMPUSES = {
            "Main Campus": {"latitude": 22.28405, "longitude": 114.13784},
            "Sassoon Road Campus": {"latitude": 22.2675, "longitude": 114.12881},
            "Swire Institute of Marine Science": {"latitude": 22.20805, "longitude": 114.26021},
            "Kadoorie Centre": {"latitude": 22.43022, "longitude": 114.11429},
            "Faculty of Dentistry": {"latitude": 22.28649, "longitude": 114.14426},
        }

        # Function to calculate the Equirectangular distance
        def equirectangular(lat1, lon1, lat2, lon2):
            x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
            y = math.radians(lat2 - lat1)
            return math.sqrt(x**2 + y**2) * radius_of_earth_km

        # Calculate distances to all campuses
        formatted_distances = []
        for campus, coords in HKU_CAMPUSES.items():
            distance = equirectangular(self.latitude, self.longitude, coords["latitude"], coords["longitude"])
            formatted_distances.append(f"The distance to {campus} is {distance:.2f} km.")

        return formatted_distances

    def __str__(self):
        return self.name
        return self.latitude, self.longitude
        return self.distance

class Reservation(models.Model):
    reservation_id = models.CharField(max_length=255, unique=True, default='')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reservations", default='')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="reservations")
    status = models.CharField(
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("cancelled", "Cancelled")
        ],
        default="available",
        max_length=50
    )

    def save(self, *args, **kwargs):
        if self.accommodation.status:
            print (f"Accommodation status: {self.accommodation.status}")
        old_status = self.accommodation.status

        try:
            print(f"Old status: {old_status}")
        except Reservation.DoesNotExist:
            old_status = None
    
        if old_status != self.status:
            print(f"Status changed from {old_status} to {self.status}")

            specialists = CedarsSpecialist.objects.all()
            email_addresses = [specialist.email for specialist in specialists if specialist.email]
            print(f"Sending email to: {email_addresses}")

            class SMTPLogger:
                def write(self, message):
                    direction = "SERVER -> CLIENT" if message.startswith('reply:') else "CLIENT -> SERVER"
                    cleaned = message.replace('reply: ', '').replace('send: ', '').strip()
                    print(f"{direction}: {cleaned}")
                    sys.stdout.flush()

            debug_logger = SMTPLogger()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(1)
            server.debugout = debug_logger

            try:
                server.starttls()
                server.login('unihavengroupd@gmail.com', 'xlbr whjy hihb njuh')
                email_addresses_str = ", ".join(email_addresses)
            
                msg = MIMEText(f"The reservation {self.reservation_id} for {self.accommodation.name} has changed to {self.status} by student {self.student.student_id}.")
                msg['Subject'] = f"Reservation Status Changed for {self.accommodation.name}"
                msg['From'] = 'unihavengroupd@gmail.com'
                msg['To'] = email_addresses_str
            
                server.send_message(msg)
                print("\n=== Send Successfully ===\n")
            
            except Exception as e:
                print(f"\n!!! Error: {e} !!!\n")
            finally:
                server.quit()

                def __str__(self):
                    return f"Reservation {self.reservation_id}: {self.student.name} - {self.accommodation.name} ({self.status})"
    
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reservation {self.reservation_id}: {self.student.name} - {self.accommodation.name} ({self.status})"

class Contract(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today)  # added default
    contract_status = models.CharField(max_length=50, default='draft')  # added default

class Rating(models.Model):
    student = models.ForeignKey(
        'Student', 
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    accommodation = models.ForeignKey(
        'Accommodation',
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='rating_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('student', 'accommodation')

    def __str__(self):
        return f"{self.student.name}'s rating ({self.score}) for {self.accommodation.name}"

class Notification(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, default=1)
    detail = models.TextField(default='')  # added default
    is_read = models.BooleanField(default=False)
    cedars_specialist = models.ForeignKey('CedarsSpecialist', on_delete=models.CASCADE, default=1)  # Make sure ID 1 exists!
