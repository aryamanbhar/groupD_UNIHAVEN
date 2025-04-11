from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    User, CedarsSpecialist, Accommodation, Reservation,
    Contract, Rating, Notification
)
from .serializers import (
    UserSerializer, CedarsSpecialistSerializer, AccommodationSerializer, StudentSerializer,
    ReservationSerializer, ContractSerializer, RatingSerializer, NotificationSerializer, AccommodationSerializer
)


class AccommodationSearchAPI(generics.ListAPIView):
    def get(self, request):
        accommodations = Accommodation.objects.all()

        # Get query params
        property_type = request.GET.get('type')
        beds = request.GET.get('number_of_beds')
        bedrooms = request.GET.get('number_of_bedrooms')
        max_price = request.GET.get('price')
        available_from = request.GET.get('availability_start')
        available_to = request.GET.get('availability_end')

            # Filter queryset dynamically
        if property_type:
            accommodations = accommodations.filter(type__iexact=property_type)
        if beds:
            accommodations = accommodations.filter(number_of_beds__gte=int(beds))
        if bedrooms:
            accommodations = accommodations.filter(number_of_bedrooms__gte=int(bedrooms))
        if max_price:
            accommodations = accommodations.filter(price__lte=float(max_price))
        if available_from:
            accommodations = accommodations.filter(availability_start__lte=available_from)
        if available_to:
            accommodations = accommodations.filter(availability_end__gte=available_to)

        serializer = AccommodationSerializer(accommodations, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK)


    # serializer_class = AccommodationSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = {
    #     'price': ['lte', 'gte'],       # Supports minPrice/maxPrice
    #     'distance': ['lte'],           # Supports maxDistance
    #     'number_of_bedrooms': ['exact'], 
    #     'status': ['exact'],           # Filter by availability
    # }

    # def get_queryset(self):
    #     queryset = Accommodation.objects.all()
    #     # Custom filters (e.g., availability date range)
    #     availability_start = self.request.query_params.get('availability_start')
    #     availability_end = self.request.query_params.get('availability_end')
    #     if availability_start and availability_end:
    #         queryset = queryset.filter(
    #             availability_start__gte=availability_start,
    #             availability_end__lte=availability_end
    #         )
    #     return queryset



class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccommodationListCreateView(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    
class AccommodationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

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

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["score", "student", "accommodation"]



class AccommodationDetailAPI(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'  # Use property_id instead of default PK
