from django.urls import path, include
from django.contrib import admin
from common.views import LoginView, RegisterView

urlpatterns = [
    path('hku/', include('apps.hku.urls')),
    path('cuhk/', include('apps.cuhk.urls')),
    path('hkust/', include('apps.hkust.urls')),  # Ensure this line is correct
    path('login/', LoginView.as_view(), name='login'),  # Add the login URL here
    path('register/', RegisterView.as_view(), name='register'),
]
