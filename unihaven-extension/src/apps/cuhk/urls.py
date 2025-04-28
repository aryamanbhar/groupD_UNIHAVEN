from django.urls import path
from .views2 import (
 AccommodationDetail, AccommodationSearch, AccommodationUpload, AccommodationsViewAll, ReservationCancelView, 
 ReservationCreateView, ReservationCedarsListView, ReservationStudentView, ReservationCedarsCancelView, StudentCreateView, CedarsSpecialistCreateView, CedarsSpecialistListView, RatingCreateView, update_contract_status,
 StudentListView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('accommodations/', AccommodationsViewAll.as_view(), name='all-accommodations'),

    path('accommodations/upload/', AccommodationUpload.as_view(), name='accommodation-list'),  
    path('accommodations/search/', AccommodationSearch.as_view(), name='accommodation-search'),
    path('accommodations/search/<str:name>/', AccommodationDetail.as_view(), name='accommodation-detail'),
    path('accommodations/rate/', RatingCreateView.as_view(), name='accommodation-rate'),

    #cedars
    path("reservations/", ReservationCedarsListView.as_view(), name="reservation-list"),
    path("reservations/cancel/", ReservationCedarsCancelView.as_view(), name="reservation-specialist-cancel"),

    #students
    path("reservations/create/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<int:student_id>/", ReservationStudentView.as_view(), name="reservation-student-view"),
    path("reservations/<int:student_id>/cancel/", ReservationCancelView.as_view(), name="reservation-student-cancel"),



    path("students/create/", StudentCreateView.as_view(), name="student-create"),
    path('students/', StudentListView.as_view(), name='student-list'),
    path("cedars_specialists/create/", CedarsSpecialistCreateView.as_view(), name="cedars-specialist-create"),
    path("cedars_specialists/", CedarsSpecialistListView.as_view(), name="cedars-specialist-list"),
    path('contracts/<int:contract_id>/update-status/', update_contract_status, name='update_contract_status'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'))
]