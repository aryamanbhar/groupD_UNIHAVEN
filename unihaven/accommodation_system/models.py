from django.db import models
# Create your models here.
class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField()
    availability = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    degree_type = models.CharField(max_length=100)

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()

class CedarsSpecialist(models.Model):
    department = models.CharField(max_length=255)

class Notification(models.Model):
    detail = models.TextField()
    is_read = models.BooleanField(default=False)