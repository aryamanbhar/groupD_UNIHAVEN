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
    CedarsSpecialist, Accommodation, Reservation,
    Contract, Rating, Notification, Student
)
from .serializers import (
    CedarsSpecialistSerializer, AccommodationSerializer, StudentSerializer,
    ReservationSerializer, ContractSerializer, RatingSerializer
)


#ACCOMMODATIONS

class AccommodationsViewAll(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    pagination_class = None  # Remove if you want pagination

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


class AccommodationDetail(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'name'

class AccommodationListView(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["type", "status", "price", "number_of_beds"]
    ordering_fields = ["price", "distance"]
    search_fields = ["name", "owner_info"]

    
class AccommodationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'



#RESERVATION


class ReservationViewAll(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'


class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "student"]


class ReservationCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    

# class ReservationCreateView(generics.ListCreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

#     def perform_create(self, serializer):
#         student_id = self.request.data.get("student_id")
#         if not student_id:
#             raise ValidationError({"detail": "Student ID must be provided."})
#         try:
#             student = User.objects.get(id=student_id)
#         except User.DoesNotExist:
#             raise ValidationError({"detail": "Student not found."})
        
#         accommodation_name = self.request.data.get("accommodation_name")
#         if not accommodation_name:
#             raise ValidationError({"detail": "Accommodation name must be provided."})
        
#         try:
#             accommodation = Accommodation.objects.get(name=accommodation_name)
#         except Accommodation.DoesNotExist:
#             raise ValidationError({"detail": "Accommodation not found with the provided name."})
        
#         accommodation.status = "reserved"
#         accommodation.save()
#         serializer.save(student=student, accommodation=accommodation)



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



#RATINGS



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
        student_id = serializer.validated_data.get("student_id")
        # student = Student.objects.get_or_create(id=student_id)

        student, created = Student.objects.get_or_create(id=student_id)
        # student_id = serializer.validated_data.pop("student_id")
        # student = get_object_or_404(Student, id=student_id) 

        # accommodation_id = serializer.validated_data["accommodation"].id
        # accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        accommodation = serializer.validated_data.get("accommodation")
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
        







# class UserListCreateView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer