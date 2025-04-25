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
    Contract, Rating, Student
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

class AccommodationSearch(generics.ListAPIView):
    serializer_class = AccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["type", "name"]
    # ordering_fields = ["type", "number_of_beds", "number_of_bedrooms", "Main Campus", "Sassoon Road Campus", "Swire Institute of Marine Science", "Kadoorie Centre", "Faculty of Dentistry", "availability_start", "availability_end", "price"]
    ordering_fields = ["type", "number_of_beds", "number_of_bedrooms", "availability_start", "availability_end", "price", "distance"]

    def get_queryset(self):
        # queryset = Accommodation.objects.all()
        return Accommodation.objects.filter(status="available")


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

class ReservationCedarsListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationStudentView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        return Reservation.objects.filter(student__student_id=student_id)


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save()


class ReservationCancelView(generics.DestroyAPIView):
    def delete(self, request, student_id):
        # Find the student's reservation
        try:
            reservation = Reservation.objects.get(student__student_id=student_id)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the reservation
        reservation.delete()
        return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_204_NO_CONTENT)


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



class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["score", "student", "accommodation"]

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Contract

def update_contract_status(request, contract_id):

    contract = get_object_or_404(Contract, pk=contract_id)

    contract.contract_status = 'failed'
    contract.save()  
    return JsonResponse({'success': f'Contract {contract_id} status updated to failed.'})

class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CedarsSpecialistCreateView(generics.CreateAPIView):
    queryset = CedarsSpecialist.objects.all()
    serializer_class = CedarsSpecialistSerializer

class CedarsSpecialistListView(generics.ListAPIView):
    queryset = CedarsSpecialist.objects.all()
    serializer_class = CedarsSpecialistSerializer
