from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.hku.models import Accommodation, Reservation, Contract, Student
from unittest.mock import patch


class TestAccommodation(APITestCase):
    @patch("apps.hku.models.GeoCodingService.get_coordinates", return_value={"Latitude": 22.3, "Longitude": 114.2})
    def setUp(self, mock_geo):
        self.client = APIClient()
        self.accommodation = Accommodation.objects.create( property_id=1, property_name="HKU Test Property", 
                                                          geo_address="Test Location", status="available")

    def test_list_accommodations(self):
        response = self.client.get(reverse("all-accommodations"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestReservation(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(student_id="HKU123", name="Test Student", contact="123456789")
        self.accommodation = Accommodation.objects.create(property_id=2, property_name="HKU Property", status="available")

    def test_create_reservation(self):
        reservation_data = {
            "student_id": self.student.student_id,
            "accommodation": self.accommodation.id,
            "start_date": "2025-05-01",
            "end_date": "2025-05-15"
        }
        response = self.client.post(reverse("reservation-create"), reservation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
