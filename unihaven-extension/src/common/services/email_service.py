from django.core.mail import send_mail
from django.conf import settings

class EmailService:
    @staticmethod
    def send_reservation_notification(email, accommodation_name, reservation_details):
        subject = f"Reservation Confirmation for {accommodation_name}"
        message = f"Dear User,\n\nYour reservation for {accommodation_name} has been confirmed.\n\nDetails:\n{reservation_details}\n\nThank you for using our service!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

    @staticmethod
    def send_cancellation_notification(email, accommodation_name):
        subject = f"Reservation Cancellation for {accommodation_name}"
        message = f"Dear User,\n\nYour reservation for {accommodation_name} has been cancelled.\n\nIf you have any questions, please contact us.\n\nThank you!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])