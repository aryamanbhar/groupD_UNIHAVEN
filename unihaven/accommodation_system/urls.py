from django.urls import path
from .views2 import (
    UserListCreateView, UserRetrieveUpdateDeleteView,
    AccommodationUpload, AccommodationRetrieveUpdateDeleteView,
    ReservationListCreateView, ReservationRetrieveUpdateDeleteView,
    RatingListCreateView, RatingRetrieveUpdateDeleteView, AccommodationSearch
)

urlpatterns = [
    # Handles /accommodations/{search}
    path('upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('search/', AccommodationSearch.as_view(), name='accommodation-search')
    # path('search/<str:property_id>/', AccommodationDetailAPI.as_view(), name='detail'),
]
