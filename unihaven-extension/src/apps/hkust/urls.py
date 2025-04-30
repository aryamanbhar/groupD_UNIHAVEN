from django.urls import path
from .views2 import (
 AccommodationDetail, AccommodationSearch, AccommodationUpload, AccommodationsViewAll, 
 ReservationCreateView, ReservationCedarsListView, ReservationStudentViewOrCancel, StudentCreateView, CedarsSpecialistCreateView, 
 CedarsSpecialistListView, update_failed_status, update_signed_status, create_contract, ContractListView,
 StudentListView, AccommodationRateView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('accommodations/', AccommodationsViewAll.as_view(), name='all-accommodations'),

    path('accommodations/upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('accommodations/search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('accommodations/search/<str:name>/', AccommodationDetail.as_view(), name='accommodation-detail'),
    path('accommodations/<int:property_id>/rate/', AccommodationRateView.as_view(), name='accommodation-rate'),

    #cedars
    path("reservations/", ReservationCedarsListView.as_view(), name="reservation-list"),
    path('contracts/<int:reservation_id>/create/', create_contract, name='create_contract'),
    path('contracts/<int:contract_id>/failed-status/', update_failed_status, name='update_failed_status'),
    path('contracts/<int:contract_id>/signed-status/', update_signed_status, name='update_signed_status'),
    path('contracts/', ContractListView.as_view(), name='contract-list'),

    #students
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<int:student_id>/", ReservationStudentViewOrCancel.as_view(), name="reservation-student-view"),


    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path('students/', StudentListView.as_view(), name='student-list'),
    path("cedars_specialists/create/", CedarsSpecialistCreateView.as_view(), name="cedars-specialist-create"),
    path("cedars_specialists/", CedarsSpecialistListView.as_view(), name="cedars-specialist-list"),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'))
]