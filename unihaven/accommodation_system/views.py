from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
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
                'id': acc.property_id,
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

def view_all(request):
    context = {
        "accommodations": Accommodation.objects.all()
        "students": Student.objects.all()
        "reservations": Reservation.objects.all()
        "ratings": Rating.objects.all()
        "specialists": CedarsSpecialist.objects.all()
        "notifications": Notification.objects.all()
    }
    return render(request, 'view_all.html', context=context)

#filters
from django.db.models import Q
from .models import Accommodation

def filter_accommodations(filters):
    """
    Filters accommodations based on the provided criteria with the following logic:
    - availability_start <= desired_start AND availability_end >= desired_end
    - number_of_beds >= desired_beds
    - number_of_bedrooms >= desired_bedrooms
    - price >= desired_price_min AND price <= desired_price_max
    - distance <= desired_distance_max
    
    :param filters: A dictionary containing filter criteria.
    :return: A QuerySet of filtered accommodations.
    """
    queryset = Accommodation.objects.all()

    if 'type' in filters:
        queryset = queryset.filter(type=filters['type'])

    if 'availability_start' in filters and 'availability_end' in filters:
        queryset = queryset.filter(
            availability_start__lte=filters['availability_start'],  
            availability_end__gte=filters['availability_end']       
        )
    elif 'availability_start' in filters:
        queryset = queryset.filter(
            availability_start__lte=filters['availability_start']
        )
    elif 'availability_end' in filters:
        queryset = queryset.filter(
            availability_end__gte=filters['availability_end']
        )

    if 'number_of_beds' in filters:
        queryset = queryset.filter(
            number_of_beds__gte=filters['number_of_beds']
        )

    if 'number_of_bedrooms' in filters:
        queryset = queryset.filter(
            number_of_bedrooms__gte=filters['number_of_bedrooms']
        )

    price_filters = Q()
    if 'price_min' in filters:
        price_filters &= Q(price__gte=filters['price_min'])
    if 'price_max' in filters:
        price_filters &= Q(price__lte=filters['price_max'])
    if price_filters:
        queryset = queryset.filter(price_filters)


    if 'distance_max' in filters:
        queryset = queryset.filter(
            distance_to_campus__lte=filters['distance_max']
        )

    return queryset
