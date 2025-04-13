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
    return HttpResponse(""""
        <html>
            <head>
                <title>UniHaven API</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding-top: 50px;
                    }
                    .button {
                        display: inline-block;
                        padding: 15px 30px;
                        margin: 10px;
                        font-size: 16px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        text-decoration: none;
                        cursor: pointer;
                        transition: background-color 0.3s ease;
                    }
                    .button:hover {
                        background-color: #45a049;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to UniHaven API</h1>
                <p>Choose one of the following:</p>
                <a href="/accommodations/" class="button">Accommodations</a>
                <a href="/reservations/" class="button">Reservations</a>
            </body>
        </html>
    """)

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('accommodations/', include('accommodation_system.urls')),  # Make sure this matches your app name
]