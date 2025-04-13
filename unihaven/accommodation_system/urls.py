from django.urls import path
from .views2 import (
 AccommodationDetail, AccommodationSearch, AccommodationUpload, AccommodationRetrieveUpdateDeleteView, ReservationViewAll, ReservationDetailView
)
  
urlpatterns = [
    # Handles /accommodations/{search}
    path('accommodations/upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('accommodations/search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('accommodations/search/<str:property_id>/', AccommodationDetail.as_view(), name='accommodation-detail'),

    path('reservations/', ReservationViewAll.as_view(), name='reservation-list-create'),
    path('reservations/<int:id>/', ReservationDetailView.as_view(), name='reservation-detail')

]
