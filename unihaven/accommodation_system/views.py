from django.http import JsonResponse
from .models import Accommodation, Reservation, Student, Rating, CedarsSpecialist, Notification

# Accommodation Views
def accommodation_list(request):
    if request.method == 'GET':
        accommodations = Accommodation.objects.all()
        data = []
        for acc in accommodations:
            # Get distances to all campuses
            distances = acc.distances()
            
            # Create descriptive sentences for each campus
            distance_sentences = [
                f"The distance to {campus} is {distance:.2f} km."
                for campus, distance in distances.items()
            ]
            
            # Add accommodation data with distance sentences
            data.append({
                'id': acc.id,
                'name': acc.name,
                'price': str(acc.price),
                'latitude': acc.latitude,
                'longitude': acc.longitude,
                'availability': acc.availability,
                'status': acc.status,
                'distances': distance_sentences,  # List of sentences
            })
        return JsonResponse({'accommodations': data})

# Student Views
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        data = [{
            'id': stu.id,
            'name': stu.name,
            'email': stu.email,
            'degree_type': stu.degree_type
        } for stu in students]
        return JsonResponse({'students': data})

# Reservation Views
def reservation_list(request):
    if request.method == 'GET':
        reservations = Reservation.objects.all()
        data = [{
            'id': res.id,
            'accommodation_id': res.accommodation.id,
            'accommodation_name': res.accommodation.name,
            'status': res.status
        } for res in reservations]
        return JsonResponse({'reservations': data})

# Rating Views
def rating_list(request):
    if request.method == 'GET':
        ratings = Rating.objects.all()
        data = [{
            'id': rat.id,
            'student_id': rat.student.id,
            'student_name': rat.student.name,
            'score': rat.score
        } for rat in ratings]
        return JsonResponse({'ratings': data})

# CedarsSpecialist Views
def specialist_list(request):
    if request.method == 'GET':
        specialists = CedarsSpecialist.objects.all()
        data = [{
            'id': spec.id,
            'department': spec.department
        } for spec in specialists]
        return JsonResponse({'specialists': data})

# Notification Views
def notification_list(request):
    if request.method == 'GET':
        notifications = Notification.objects.all()
        data = [{
            'id': notif.id,
            'detail': notif.detail,
            'is_read': notif.is_read
        } for notif in notifications]
        return JsonResponse({'notifications': data})
