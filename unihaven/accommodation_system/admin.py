from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Accommodation)
admin.site.register(Reservation)
admin.site.register(Student)
admin.site.register(Rating)
admin.site.register(CedarsSpecialist)
admin.site.register(Notification)
