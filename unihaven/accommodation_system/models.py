from django.db import models

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

    def __str__(self):
        return self.name

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
