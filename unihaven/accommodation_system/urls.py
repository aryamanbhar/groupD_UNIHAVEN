from django.urls import path
from . import views

urlpatterns = [
    # Accommodation endpoints
    # path('accommodations/', views.accommodation_list),

    path('accommodations/', views.accommodation_list, name='accommodation-list'),
    
    # Student endpoints
    path('students/', views.student_list),
    
    # Reservation endpoints
    path('reservations/', views.reservation_list),
    
    # Rating endpoints
    path('ratings/', views.rating_list),
    
    # Specialist endpoints
    path('specialists/', views.specialist_list),
    
    # Notification endpoints
    path('notifications/', views.notification_list),

]