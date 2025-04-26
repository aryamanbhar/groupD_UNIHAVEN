from django.db import models
from common.services.geocoding_service import GeoCodingService
import math
from datetime import date
from django.db.models import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.mail import send_mail
import smtplib
import sys
from email.mime.text import MIMEText

class CedarsSpecialist(models.Model):
        cedars_specialist_id = models.AutoField(primary_key=True)
        email = models.EmailField(unique=True)

class Student(models.Model):
    student_id = models.CharField(max_length=255, unique=True, default='')
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255, default='')  # added default
    degree_type = models.CharField(max_length=100, default='')  # added default
    
class Accommodation(models.Model):
    property_id = models.CharField(max_length=255, unique=True, default='')
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

    # Address components
    room_number = models.CharField(max_length=50, null=True, blank=True, default= '')  # May be null for entire flats
    flat_number = models.CharField(max_length=50, default= '')
    floor_number = models.CharField(max_length=50, default= '')
    geo_address = models.TextField(default= '')

    class Meta:
        # Enforce uniqueness for the address components
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
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="reservations", default='')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="reservations", unique=True)
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
        if self.status == "reserved":
            self.accommodation.status = "unavailable"
        elif self.status == "cancelled":
            self.accommodation.status = "available"
        
        self.accommodation.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reservation {self.id}: {self.student.name} - {self.accommodation.name} ({self.status})"

class Contract(models.Model):
    contract_id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today) 
    contract_status = models.CharField(
        max_length=50,
        choices=[
            ('draft', 'Draft'),
            ('signed', 'Signed'),
            ('completed', 'Completed'),
            ('failed', 'Failed') 
        ],
        default='draft'
    )

    def save(self, *args, **kwargs):
        """
        Override save method to handle status updates when contract_status is set to 'failed'.
        """
        # Check if the contract status is being set to 'failed'
        if self.contract_status == 'failed':
            # Update the reservation status to 'cancelled'
            self.reservation.status = 'cancelled'
            self.reservation.save()

            # Update the accommodation status to 'available'
            accommodation = self.reservation.accommodation
            accommodation.status = 'available'
            accommodation.save()

        super().save(*args, **kwargs)

    def has_failed(self):
        """
        Check if the contract has failed.
        """
        return self.contract_status == 'failed'

    def __str__(self):
        return f"Contract for Reservation {self.reservation.student} - Status: {self.contract_status}"

class Rating(models.Model):
        student = models.ForeignKey(
            'Student', 
            on_delete=models.CASCADE,
            related_name='student_ratings'
        )
        accommodation = models.ForeignKey(
            'Accommodation',
            on_delete=models.CASCADE,
            related_name='accommodation_ratings'
        )
        score = models.IntegerField(
            choices=[(i, f"{i}") for i in range(1, 6)],
            validators=[
                MinValueValidator(1),
                MaxValueValidator(5)
            ]
        )
        comment = models.TextField(blank=True)
        photo = models.ImageField(
            upload_to='rating_photos/',
            blank=True,
            null=True
        )
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

class Meta:
        unique_together = ['student', 'accommodation']

def __str__(self):
        return f"{self.student.name}'s rating ({self.score}) for {self.accommodation.name}"

# class Notification(models.Model):
#     student = models.ForeignKey('Student', on_delete=models.CASCADE, default=1)
#     detail = models.TextField(default='')  # added default
#     is_read = models.BooleanField(default=False)
#     cedars_specialist = models.ForeignKey('CedarsSpecialist', on_delete=models.CASCADE, default=1)  # Make sure ID 1 exists!