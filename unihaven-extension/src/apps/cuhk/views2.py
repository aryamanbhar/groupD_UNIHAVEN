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
    ReservationSerializer, ContractSerializer, RatingSerializer, AccommodationRatingSerializer
)
from common.utils.permissions import IsCUHK, IsStaff, IsStudent, IsAdmin


#ACCOMMODATIONS

class AccommodationsViewAll(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    pagination_class = None  # Remove if you want pagination

    def get_queryset(self):
        # only return those still available
        return Accommodation.objects.all()
    
class AccommodationUpload(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class AccommodationSearch(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["number_of_beds", "number_of_bedrooms", "availability_start", "availability_end", "price", "distance"]
    search_fields = ["type", "geo_address"]
    ordering_fields = ["distance"]
    # ordering_fields = ["type", "number_of_beds", "number_of_bedrooms", "availability_start", "availability_end", "price", "distance"]

    def get_queryset(self):
        queryset = Accommodation.objects.filter(status="available")
        ordering = self.request.query_params.get('ordering', 'distance')  # Default to 'distance'
        queryset = queryset.order_by(ordering)

        # if not self.request.query_params.get('ordering'):
        #     queryset = queryset.order_by('distance')  # Default: ascending
        
        return queryset


class AccommodationDetail(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_name'

#RESERVATION

class ReservationCedarsListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.all()
        # return Reservation.objects.exclude(status="cancelled")


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(status='reserved')

class ReservationStudentViewOrCancel(generics.ListAPIView):
    serializer_class = ReservationSerializer
    lookup_field     = 'student__student_id'
    lookup_url_kwarg = 'student_id'

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Reservation.objects.filter(student__student_id=student_id)


    def delete(self, request, student_id):
        try:
            reservation = Reservation.objects.get(student__student_id=student_id)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

        accommodation = reservation.accommodation
        accommodation.status = 'available'
        accommodation.save()
        
        reservation.delete()
        return Response({"message": "Reservation cancelled successfully."}, status=status.HTTP_204_NO_CONTENT)
    
        serializer_class.save(status='reserved')



#RATINGS

class AccommodationRateView(generics.GenericAPIView):
    serializer_class = AccommodationRatingSerializer

    def post(self, request, property_id):
        try:
            accommodation = Accommodation.objects.get(property_id=property_id)
        except Accommodation.DoesNotExist:
            return Response({"error": "Accommodation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = serializer.validated_data['rating']

        # Update the rating
        accommodation.total_rating += rating
        accommodation.num_ratings += 1
        accommodation.save()

        return Response({
            "message": "Rating submitted successfully.",
            "new_average_rating": accommodation.average_rating()
        }, status=status.HTTP_200_OK)


# class RatingCreateView(generics.CreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
    
#     def perform_create(self, serializer):
#         student = self.request.user.student
#         accommodation_id = self.request.data.get('accommodation')
#         accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
        
#         has_contract = Contract.objects.filter(
#             reservation__student=student,
#             reservation__accommodation=accommodation,
#             contract_status='signed'
#         ).exists()
            
#         serializer.save(student=student, accommodation=accommodation)

# class RatingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         rating = super().get_object()
#         if rating.student.user != self.request.user:
#             raise PermissionDenied("You can only modify your own ratings")
#         return rating



# class RatingListView(generics.ListAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["score", "student", "accommodation"]

# contracts
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Contract

def create_contract(request, reservation_id):
    """
    Create a Contract for the given Reservation ID.
    """

    reservation = get_object_or_404(Reservation, reservation_id=reservation_id)


    if Contract.objects.filter(reservation=reservation).exists():
        return JsonResponse({
            "error": "Contract already exists for this reservation."
        }, status=400)


    contract = Contract.objects.create(
        reservation=reservation,
        contract_status='unsigned' 
    )

    return JsonResponse({
        "message": "Contract created successfully.",
        "contract_id": contract.contract_id,
        "reservation_id": reservation.reservation_id,
        "contract_status": contract.contract_status
    }, status=201)

def update_failed_status(request, contract_id):

    contract = get_object_or_404(Contract, pk=contract_id)

    contract.contract_status = 'failed'
    contract.save()  
    return JsonResponse({'success': f'Contract {contract_id} status updated to failed.'})

def update_signed_status(request, contract_id):

    contract = get_object_or_404(Contract, pk=contract_id)

    contract.contract_status = 'signed'
    contract.save()  
    return JsonResponse({'success': f'Contract {contract_id} status updated to signed.'})

class ContractListView(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer



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