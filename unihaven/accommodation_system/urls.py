from django.urls import path
from .views2 import (
 AccommodationDetail, AccommodationSearch, AccommodationUpload, AccommodationsViewAll, AccommodationRetrieveUpdateDeleteView, ReservationCancelView, 
 ReservationCreateView, ReservationListView, ReservationDetailView, StudentCreateView, CedarsSpecialistCreateView, CedarsSpecialistListView, RatingCreateView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('accommodations/', AccommodationsViewAll.as_view(), name='all-accommodations'),
    path('accommodations/upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('accommodations/search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('accommodations/search/<str:name>/', AccommodationDetail.as_view(), name='accommodation-detail'),
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<int:reservation_id>/cancel/", ReservationCancelView.as_view(), name="reservation-cancel"),
    path("reservations/<int:reservation_id>/", ReservationDetailView.as_view(), name="reservation-detail"),
    path("reservations/", ReservationListView.as_view(), name="reservation-list"),
    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path("cedars_specialists/create/", CedarsSpecialistCreateView.as_view(), name="cedars-specialist-create"),
    path("cedars_specialists/", CedarsSpecialistListView.as_view(), name="cedars-specialist-list"),
    path('accommodations/rate/', RatingCreateView.as_view(), name='accommodation-rate'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'))
]
