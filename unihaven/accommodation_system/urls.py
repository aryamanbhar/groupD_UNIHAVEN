from django.urls import path
from .views2 import (
    UserListCreateView, UserRetrieveUpdateDeleteView,
    ReservationListCreateView, ReservationRetrieveUpdateDeleteView,
    RatingListCreateView, RatingRetrieveUpdateDeleteView, AccommodationDetail, AccommodationSearch, AccommodationViewAll, AccommodationUpload, AccommodationRetrieveUpdateDeleteView,
)

urlpatterns = [
    # Handles /accommodations/{search}
    path('', AccommodationViewAll.as_view(), name='accommodations'),
    path('upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('search/<str:property_id>/', AccommodationDetail.as_view(), name='accommodation-detail'),
]
