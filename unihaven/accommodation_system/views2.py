from rest_framework import generics, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    User, CedarsSpecialist, Accommodation, Reservation,
    Contract, Rating, Notification
)
from .serializers import (
    UserSerializer, CedarsSpecialistSerializer, AccommodationSerializer, StudentSerializer,
    ReservationSerializer, ContractSerializer, RatingSerializer, NotificationSerializer, AccommodationSerializer
)

class AccommodationUpload(generics.ListCreateAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer


class AccommodationSearch(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name", "type"]
    ordering_fields = ["distance"]

    # def get_queryset(self):
    #     queryset = Accommodation.objects.all()
    #     user_lat = self.request.query_params.get('lattitude')
    #     user_lng = self.request.query_params.get('longtitude')

    #     if user_lat and user_lng:
    #         # Annotate each accommodation with dynamic distance
    #         for acc in queryset:
    #             acc.distance = acc.calculate_distance(float(user_lat), float(user_lng))
            
    #         # Sort if requested (?ordering=distance)
    #         if self.request.query_params.get('ordering') == 'distance':
    #             queryset = sorted(queryset, key=lambda x: x.distance)

    #     return queryset



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

class AccommodationViewAll(generics.ListAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class AccommodationDetail(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    lookup_field = 'property_id'
    
class AccommodationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer







class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
