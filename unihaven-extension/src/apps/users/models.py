from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    UNIVERSITY_CHOICES = (
        ('HKUST', 'HKUST'),
        ('CUHK', 'CUHK'),
        ('HKU', 'HKU'),
    )
    university = models.CharField(max_length=50, choices=UNIVERSITY_CHOICES, default='HKUST')