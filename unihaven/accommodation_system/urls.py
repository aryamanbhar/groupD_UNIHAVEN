from django.urls import path
from .views2 import (
    UserListCreateView, UserRetrieveUpdateDeleteView,
    AccommodationListCreateView, AccommodationRetrieveUpdateDeleteView,
    ReservationListCreateView, ReservationRetrieveUpdateDeleteView,
    RatingListCreateView, RatingRetrieveUpdateDeleteView, AccommodationSearchAPI, AccommodationDetailAPI
)

urlpatterns = [


    path('', AccommodationListCreateView.as_view(), name='accommodation-list'),  # Handles /api/accommodations/
    path('search/', AccommodationSearchAPI.as_view(), name='search'),
    path('<str:property_id>/', AccommodationDetailAPI.as_view(), name='detail'),

    # path("api/users/", UserListCreateView.as_view(), name="user-list-create"),
    # path("api/users/<int:pk>/", UserRetrieveUpdateDeleteView.as_view(), name="user-detail"),
    # path("api/accommodations/", AccommodationListCreateView.as_view(), name="accommodation-list-create"),
    # path("api/accommodations/<int:pk>/", AccommodationRetrieveUpdateDeleteView.as_view(), name="accommodation-detail"),

    # path("api/reservations/", ReservationListCreateView.as_view(), name="reservation-list-create"),
    # path("api/reservations/<int:pk>/", ReservationRetrieveUpdateDeleteView.as_view(), name="reservation-detail"),

    # path("api/ratings/", RatingListCreateView.as_view(), name="rating-list-create"),
    # path("api/ratings/<int:pk>/", RatingRetrieveUpdateDeleteView.as_view(), name="rating-detail"),
]
