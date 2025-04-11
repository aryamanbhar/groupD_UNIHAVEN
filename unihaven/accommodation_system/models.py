from django.db import models
from .services.geocoding_service import GeoCodingService
import math
from datetime import date

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default='')  # added default

class CedarsSpecialist(models.Model):
    department = models.CharField(max_length=255, default='')  # added default

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255, default='')  # added default
    degree_type = models.CharField(max_length=100, default='')  # added default
    
class Accommodation(models.Model):
    property_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    type = models.CharField(max_length=100, default='')
    owner_info = models.TextField(default='')  # fixed
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    distance = models.FloatField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    number_of_beds = models.IntegerField(default=0)  # fixed
    number_of_bedrooms = models.IntegerField(default=0)  # fixed
    availability_start = models.DateField(default=date.today)  # fixed
    availability_end = models.DateField(default=date.today)  # fixed
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        # Automatically fetch latitude and longitude if not provided
        if not self.latitude or not self.longitude:
            geo_data = GeoCodingService.get_coordinates(self.name)
            if geo_data:
                self.latitude = geo_data['latitude']
                self.longitude = geo_data['longitude']
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
        distances = {}
        for campus, coords in HKU_CAMPUSES.items():
            distances[campus] = equirectangular(self.latitude, self.longitude, coords["latitude"], coords["longitude"])

        return distances

    def __str__(self):
        return self.name
        return self.latitude, self.longitude, self.distance

class Reservation(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, default=1)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=50, default='pending')  # added default

class Contract(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today)  # added default
    contract_status = models.CharField(max_length=50, default='draft')  # added default

class Rating(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, default=1)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE, default=1)
    score = models.IntegerField(default=0)  # added default

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=1)
    detail = models.TextField(default='')  # added default
    is_read = models.BooleanField(default=False)
    cedars_specialist = models.ForeignKey('CedarsSpecialist', on_delete=models.CASCADE, default=1)  # Make sure ID 1 exists!
