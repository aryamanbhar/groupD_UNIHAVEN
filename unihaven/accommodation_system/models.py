from django.db import models
from .services.geocoding_service import GeoCodingService
import math

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    type = models.CharField(max_length=100)
    owner_info = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    area = models.FloatField()
    distance = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    availability_start = models.DateField()
    availability_end = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    degree_type = models.CharField(max_length=100)

class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

class Contract(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    date = models.DateField()
    document = models.FileField(upload_to='contracts/')
    signed_at = models.DateTimeField(null=True, blank=True)
    contract_status = models.CharField(max_length=50)

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()

class CedarsSpecialist(models.Model):
    department = models.CharField(max_length=255)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detail = models.TextField()
    is_read = models.BooleanField(default=False)
