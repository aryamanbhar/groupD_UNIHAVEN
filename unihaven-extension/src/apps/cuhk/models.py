from django.db import models
from common.services.geocoding_service import GeoCodingService
import math
from datetime import date
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.mail import send_mail
import smtplib
import sys, os
from email.mime.text import MIMEText


class CedarsSpecialist(models.Model):
    cedars_specialist_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)

class Student(models.Model):
    student_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255, default='')  # added default'
    contact = models.IntegerField(default=0)
    university = models.CharField(max_length=100, default='')  # added default
    
class Accommodation(models.Model):
    property_id = models.AutoField(primary_key=True)  # Automatically incremented integer
    property_name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    type = models.CharField(max_length=100, default='')
    area = models.CharField(max_length=100, default='')
    owner_info = models.TextField(default='')
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    distance = JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    number_of_beds = models.IntegerField(default=0)
    number_of_bedrooms = models.IntegerField(default=0)
    availability_start = models.DateField(default=date.today)
    availability_end = models.DateField(default=date.today)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved")
        ],
        default="available",
        max_length=50
    )
    total_rating = models.IntegerField(default=0)
    num_ratings = models.IntegerField(default=0)

    def average_rating(self):
        if self.num_ratings == 0:
            return None
        return round(self.total_rating / self.num_ratings, 2)

    # Address components
    room_number = models.CharField(max_length=50, null=True, blank=True, default='')
    flat_number = models.CharField(max_length=50, default='')
    floor_number = models.CharField(max_length=50, default='')
    geo_address = models.TextField(default='')

    class Meta:
        unique_together = ('room_number', 'flat_number', 'floor_number', 'geo_address')

    def save(self, *args, **kwargs):
        # Automatically fetch latitude and longitude if not provided
        if not self.latitude or not self.longitude:
            geo_data = GeoCodingService.get_coordinates(self.geo_address)
            if geo_data:
                self.latitude = geo_data['latitude']
                self.longitude = geo_data['longitude']

        self.distance = self.calculate_distance()
        super().save(*args, **kwargs)

    def calculate_distance(self):
        """
        Uses the Equirectangular approximation formula.
        """
        radius_of_earth_km = 6371
        CUHK_CAMPUSES = {
            "Main Campus": {"latitude": 22.41907, "longitude": 114.20693},
        }

        def equirectangular(lat1, lon1, lat2, lon2):
            x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
            y = math.radians(lat2 - lat1)
            return math.sqrt(x**2 + y**2) * radius_of_earth_km

        formatted_distances = []
        for campus, coords in CUHK_CAMPUSES.items():
            distance = equirectangular(self.latitude, self.longitude, coords["latitude"], coords["longitude"])
            formatted_distances.append(f"The distance to {campus} is {distance:.2f} km.")

        return formatted_distances


    def __str__(self):
        return f"Accommodation at {self.geo_address} (Lat: {self.latitude}, Long: {self.longitude})"

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reservations", default='')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="reservations")
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)    
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
        # if self.pk:  # Check if the reservation already exists in the database
        #     old_status = Reservation.objects.get(pk=self.pk).status
        # else:
        #     old_status = None
        # # Update the accommodation status based on reservation status
        # if self.status in ["available", "cancelled"]:
        #     self.accommodation.status = "available"
        # elif self.status == "reserved":
        #     self.accommodation.status = "reserved"
        
        # self.accommodation.save()  # Save accommodation status

        # # Send email if the status has changed
        # if old_status != self.status:
        #     self.send_status_change_email()

        # super().save(*args, **kwargs)  # Ensure the reservation is saved last
        if self.status in ["available", "cancelled"]:
            self.accommodation.status = "available"
        elif self.status == "reserved":
            self.accommodation.status = "reserved"
 
         # Save the updated accommodation status
        self.accommodation.save()

        if not self.pk:
            self.send_status_change_email()
        
        super().save(*args, **kwargs)

    def send_status_change_email(self):
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
        
            msg = MIMEText(f"The reservation {self.reservation_id} for {self.accommodation.geo_address} has changed to {self.status} by student {self.student.student_id}.")
            msg['Subject'] = f"Reservation Status Changed for {self.accommodation.geo_address}"
            msg['From'] = 'unihavengroupd@gmail.com'
            msg['To'] = email_addresses_str
        
            server.send_message(msg)
            print("\n=== Send Successfully ===\n")
        
        except Exception as e:
            print(f"\n!!! Error: {e} !!!\n")
        finally:
            server.quit()

    def __str__(self):
        return f"Reservation {self.reservation_id}: {self.student.name} - {self.accommodation.geo_address} ({self.status})"
    



class Contract(models.Model):
    contract_id = models.IntegerField(primary_key=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    date = models.DateField(default=date.today) 
    contract_status = models.CharField(
        max_length=50,
        choices=[
            ('unsigned', 'unsigned'),
            ('signed', 'Signed'),
            ('failed', 'Failed'),
        ],
        default='draft'
    )

    def save(self, *args, **kwargs):
        if not self.contract_id:
            self.contract_id = self.reservation.reservation_id
        super().save(*args, **kwargs)
        """
        Override save method to handle status updates when contract_status is set to 'failed'.
        """
        if self.contract_status == 'failed':
            self.reservation.status = 'cancelled'
            self.reservation.save()
            self.reservation.send_status_change_email()

            accommodation = self.reservation.accommodation
            accommodation.status = 'available'
            accommodation.save()

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Contract for Reservation {self.reservation.accommodation} - Status: {self.contract_status}"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='rating_images/')

