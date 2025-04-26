from .base import *
SECRET_KEY = 'django-insecure-wo_+-^0^@x30n$5q^eb05nr0f^i+^efx-7s3k_u%i^f!90voi5'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# SMTP Debugging
try:
    import smtplib
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("SMTP connection successful!")
    server.quit()
except Exception as e:
    print(f"SMTP connection failed: {e}")