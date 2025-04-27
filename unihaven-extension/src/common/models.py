from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='accommodations')
    property_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    type = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    owner_info = models.TextField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_beds = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    availability_start = models.DateField()
    availability_end = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=[
            ("available", "Available"),
            ("reserved", "Reserved"),
            ("unavailable", "Unavailable")
        ],
        default="available",
        max_length=50
    )

    def __str__(self):
        return self.name

class Reservation(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name="reservations")
    student_email = models.EmailField()
    status = models.CharField(
        choices=[
            ("reserved", "Reserved"),
            ("cancelled", "Cancelled")
        ],
        default="reserved",
        max_length=50
    )
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.accommodation.name} by {self.student_email}"

class Specialist(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='specialists')
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class Rating(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    images = models.ManyToManyField(UploadedImage)

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='rating_images/')
