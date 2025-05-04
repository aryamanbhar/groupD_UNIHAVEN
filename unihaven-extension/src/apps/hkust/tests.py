from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.hkust.models import Accommodation, Reservation, Contract, Student


class FullEndpointTest(APITestCase):
    def setUp(self):
        CedarsSpecialist.objects.create(email='cedars@example.com')
        # Create a student object
        self.student = Student.objects.create(student_id="10", name="John Doe", contact=5339555)
        # Create an accommodation and a reservation for the student
        self.accommodation = Accommodation.objects.create(property_id=99, property_name="CUHK Property", status="available", latitude=22.3964, longitude=114.1095, geo_address="9 Lung Wah St Kennedy Town")
        self.reservation = Reservation.objects.create(student=self.student, accommodation=self.accommodation, start_date="2025-05-01", end_date="2025-05-15", status="reserved")
        self.contract = Contract.objects.create(reservation=self.reservation, contract_status="unsigned")


#ACCOMMODATIONS

    def test_get_all_accommodations(self):
        response = self.client.get(reverse("all-accommodations"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_upload_accommodation(self):
        data = {
            "property_id": 100,
            "property_name": "New HKUST Property",
            "status": "available", 
            "latitude": 22.3964, 
            "longitude": 114.1095, 
            "geo_address": "109 Wan Chai Road"
        }
        response = self.client.post(reverse("accommodation-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_accommodation(self):
        response = self.client.get(reverse("accommodation-search"), {
            "property_name": "CUHK Property", 
            "status": "available", 
            "price": 10000             
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_accommodation(self):
        # self.accommodation.geo_address = "9 Lung Wah St Kennedy Town"
        # self.accommodation.save()
        response = self.client.get(reverse("accommodation-detail", kwargs={"property_name": "CUHK Property"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_student_reservation(self):
        # Make sure the reservation exists
        response = self.client.get(reverse("reservation-student-view", kwargs={"student_id": self.student.student_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_rate_accommodation(self):
        data = {"rating": 4}
        response = self.client.post(reverse("accommodation-rate", kwargs={"property_id": self.accommodation.property_id}), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("new_average_rating", response.data)


#RESERVATIONS

    def test_get_all_reservations_cedars(self):
        response = self.client.get(reverse("reservation-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_reservation(self):
        data = {
            "student_id": self.student.student_id,
            "contact": self.student.contact,
            "accommodation": self.accommodation.property_id,
            "start_date": "2025-06-01",
            "end_date": "2025-06-15"
        }
        response = self.client.post(reverse("reservation-create"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_student_reservation(self):
        response = self.client.get(reverse("reservation-student-view", kwargs={"student_id": self.student.student_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_student_reservation(self):
        response = self.client.delete(reverse("reservation-student-view", kwargs={"student_id": self.student.student_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_create_contract(self):
        # Delete the original one to test creation
        self.contract.delete()
        response = self.client.post(reverse("create_contract", kwargs={"reservation_id": self.reservation.reservation_id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_failed_status(self):
        response = self.client.post(reverse("update_failed_status", kwargs={"contract_id": self.contract.contract_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_signed_status(self):
        response = self.client.post(reverse("update_signed_status", kwargs={"contract_id": self.contract.contract_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_contracts(self):
        response = self.client.get(reverse("contract-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

