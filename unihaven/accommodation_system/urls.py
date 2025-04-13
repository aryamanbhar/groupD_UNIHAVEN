from django.urls import path
from .views2 import (
 AccommodationDetail, AccommodationSearch, AccommodationUpload, AccommodationRetrieveUpdateDeleteView, ReservationCancelView, 
 ReservationCreateView, ReservationListView, ReservationViewAll, ReservationDetailView
)
  
urlpatterns = [
    path('accommodations/upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('accommodations/search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('accommodations/search/<str:property_id>/', AccommodationDetail.as_view(), name='accommodation-detail'),
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<str:reservation_id>/cancel/", ReservationCancelView.as_view(), name="reservation-cancel"),
    path("reservations/<str:reservation_id>/", ReservationDetailView.as_view(), name="reservation-detail"),
    path("reservations/", ReservationListView.as_view(), name="reservation-list"),
]
