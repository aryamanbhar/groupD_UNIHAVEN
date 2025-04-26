from .base import *
import os
from django.core.exceptions import ImproperlyConfigured

DEBUG = True
ALLOWED_HOSTS = ['your-production-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Secret Key
SECRET_KEY = 'django-insecure-wo_+-^0^@x30n$5q^eb05nr0f^i+^efx-7s3k_u%i^f!90voi5'

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')