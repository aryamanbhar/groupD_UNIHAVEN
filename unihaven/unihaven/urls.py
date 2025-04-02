"""
URL configuration for unihaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('accommodation_system.urls')),  # Points to your app's URLs
# ]

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Welcome to UniHaven API</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/api/accommodations/">Accommodations</a></li>
            <li><a href="/api/students/">Students</a></li>
            <li><a href="/api/reservations/">Reservations</a></li>
            <li><a href="/api/ratings/">Ratings</a></li>
            <li><a href="/api/specialists/">Specialists</a></li>
            <li><a href="/api/notifications/">Notifications</a></li>
            <li><a href="/admin/">Admin</a></li>
        </ul>
    """)

urlpatterns = [
    path('', home, name='home'),  # This handles the root URL
    path('admin/', admin.site.urls),
    path('api/', include('accommodation_system.urls')),  # Make sure this matches your app name
]