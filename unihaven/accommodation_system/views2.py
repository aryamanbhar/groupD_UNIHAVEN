from rest_framework import generics, filters, viewsets
from .filters import AccommodationFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import (
    User, CedarsSpecialist, Accommodation, Reservation,
    Contract, Rating, Notification, Student
)
from .serializers import (
    UserSerializer, CedarsSpecialistSerializer, AccommodationSerializer, StudentSerializer,
    ReservationSerializer, ContractSerializer, RatingSerializer, NotificationSerializer
)

class AccommodationUpload(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer


# class AccommodationSearch(generics.ListAPIView):
#     queryset = Accommodation.objects.all()
#     serializer_class = AccommodationSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ["name"]
#     search_fields = ["name", "type"]
#     ordering_fields = ["distance"]

#     def get_queryset(self):
#         queryset = Accommodation.objects.all()
#         user_lat = self.request.query_params.get('latitude')
#         user_lng = self.request.query_params.get('longitude')

#         if user_lat and user_lng:
#             # Annotate each accommodation with dynamic distance
#             for acc in queryset:
#                 acc.distance = acc.calculate_distance(float(user_lat), float(user_lng))
            
#             # Sort if requested (?ordering=distance)
#             if self.request.query_params.get('ordering') == 'distance':
#                 queryset = sorted(queryset, key=lambda x: x.distance)

#         return queryset

class AccommodationSearch(generics.ListAPIView):
    serializer_class = AccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["type", "name"]
    # ordering_fields = ["type", "number_of_beds", "number_of_bedrooms", "Main Campus", "Sassoon Road Campus", "Swire Institute of Marine Science", "Kadoorie Centre", "Faculty of Dentistry", "availability_start", "availability_end", "price"]
    ordering_fields = ["type", "number_of_beds", "number_of_bedrooms", "availability_start", "availability_end", "price", "distance"]

    def get_queryset(self):
        queryset = Accommodation.objects.all()

        return queryset

# class AccommodationSearchAPI(generics.ListAPIView):
#     serializer_class = AccommodationSerializer

#     def get_queryset(self):
#         queryset = Accommodation.objects.all()
        
#         # Access query params from the request
#         request = self.request
        
#         property_type = request.GET.get('type')
#         beds = request.GET.get('number_of_beds')
#         bedrooms = request.GET.get('number_of_bedrooms')
#         max_price = request.GET.get('price')
#         available_from = request.GET.get('availability_start')
#         available_to = request.GET.get('availability_end')

#         # Dynamically filter queryset based on query parameters
#         if property_type:
#             queryset = queryset.filter(type__iexact=property_type)
#         if beds:
#             queryset = queryset.filter(number_of_beds__gte=int(beds))
#         if bedrooms:
#             queryset = queryset.filter(number_of_bedrooms__gte=int(bedrooms))
#         if max_price:
#             queryset = queryset.filter(price__lte=float(max_price))
#         if available_from:
#             queryset = queryset.filter(availability_start__lte=available_from)
#         if available_to:
#             queryset = queryset.filter(availability_end__gte=available_to)

#         return queryset

class AccommodationDetail(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'
    
class AccommodationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'





class ReservationViewAll(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'








class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class ReservationListCreateView(generics.ListCreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

# class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
    def perform_create(self, serializer):
        student = self.request.user.student
        accommodation_id = self.request.data.get('accommodation')
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        
        has_contract = Contract.objects.filter(
            reservation__student=student,
            reservation__accommodation=accommodation,
            contract_status='signed'
        ).exists()
            
        serializer.save(student=student, accommodation=accommodation)

class RatingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        rating = super().get_object()
        if rating.student.user != self.request.user:
            raise PermissionDenied("You can only modify your own ratings")
        return rating

class AccommodationListView(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["type", "status", "price", "number_of_beds"]
    ordering_fields = ["price", "distance"]
    search_fields = ["name", "owner_info"]


class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "student"]

class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer): 
        student_id = self.request.data.get("student_id")
        if not student_id:
            raise ValidationError({"detail": "You must provide your Student ID."})

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise ValidationError({"detail": "Invalid Student ID. No matching student found."})

        accommodation_id = self.request.data.get("accommodation_id")
        accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        serializer.save(student=student, accommodation=accommodation)


class ReservationCancelView(generics.DestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'reservation_id'

    def perform_destroy(self, instance):
        if instance.status == "cancelled":
            raise ValidationError({"detail": "This reservation has already been cancelled."})
        
        instance.status = "cancelled"
        instance.save()

        accommodation = instance.accommodation
        accommodation.status = "available"
        accommodation.save()

        instance.delete()

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["score", "student", "accommodation"]
        
class AccommodationDetailAPI(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'  # Use property_id instead of default PK

