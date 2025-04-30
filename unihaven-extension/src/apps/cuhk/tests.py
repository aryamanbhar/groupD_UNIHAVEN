from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.cuhk.models import Accommodation, Reservation, Contract, Student

class TestAccommodation(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.accommodation = Accommodation.objects.create(
            property_id=1,
            property_name="HKUST Test Property",
            status="available"
        )

    def test_list_accommodations(self):
        response = self.client.get(reverse("all-accommodations"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_modify_accommodation(self):
        url = reverse("modify-accommodation", kwargs={"pk": self.accommodation.id})
        updated_data = {
            "property_name": "HKUST Updated Property",
            "status": "unavailable"
        }

        response = self.client.put(url, updated_data, format="json")
        
        # Ensure update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.accommodation.refresh_from_db()
        self.assertEqual(self.accommodation.property_name, updated_data["property_name"])
        self.assertEqual(self.accommodation.status, updated_data["status"])

class TestReservation(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(student_id="CUHK123", name="Test Student", contact="123456789")
        self.accommodation = Accommodation.objects.create(property_id=2, property_name="CUHK Property", status="available")

    def test_create_reservation(self):
        reservation_data = {
            "student_id": self.student.student_id,
            "accommodation": self.accommodation.id,
            "start_date": "2025-05-01",
            "end_date": "2025-05-15"
        }
        response = self.client.post(reverse("reservation-create"), reservation_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
