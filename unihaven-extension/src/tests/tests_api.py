from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from apps.hku.models import Accommodation, Reservation, Contract, Student
from apps.cuhk.models import Accommodation as CUHKAccommodation, Reservation as CUHKReservation, Contract as CUHKContract, Student as CUHKStudent
from apps.hkust.models import Accommodation as HKUSTAccommodation, Reservation as HKUSTReservation, Contract as HKUSTContract, Student as HKUSTStudent


class BaseTestSetup(APITestCase):
    """Common setup for all tests"""
    def setUp(self):
        self.client = APIClient()
        self.universities = {
            "hku": {"model": Accommodation, "student_model": Student, "reservation_model": Reservation, "contract_model": Contract},
            "cuhk": {"model": CUHKAccommodation, "student_model": CUHKStudent, "reservation_model": CUHKReservation, "contract_model": CUHKContract},
            "hkust": {"model": HKUSTAccommodation, "student_model": HKUSTStudent, "reservation_model": HKUSTReservation, "contract_model": HKUSTContract},
        }

    def create_test_accommodation(self, uni, property_id=1):
        return self.universities[uni]["model"].objects.create(property_id=property_id, property_name=f"{uni.upper()} Test Property", status="available")

    def create_test_student(self, uni, student_id="12345"):
        return self.universities[uni]["student_model"].objects.create(student_id=student_id, name="Test Student", contact="123456789")

class AccommodationTests(BaseTestSetup):
    def test_list_accommodations(self):
        for uni in self.universities:
            self.create_test_accommodation(uni)
            response = self.client.get(reverse("all-accommodations"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_accommodation(self):
        for uni in self.universities:
            self.create_test_accommodation(uni)
            response = self.client.get(reverse("accommodation-search"), {"type": "apartment"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReservationTests(BaseTestSetup):
    def test_create_reservation(self):
        for uni in self.universities:
            student = self.create_test_student(uni)
            accommodation = self.create_test_accommodation(uni)
            reservation_data = {
                "student_id": student.student_id,
                "accommodation": accommodation.id,
                "start_date": "2025-05-01",
                "end_date": "2025-05-15"
            }
            response = self.client.post(reverse("reservation-create"), reservation_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cancel_reservation(self):
        for uni in self.universities:
            student = self.create_test_student(uni)
            accommodation = self.create_test_accommodation(uni)
            reservation = self.universities[uni]["reservation_model"].objects.create(student=student, accommodation=accommodation, status="reserved")
            response = self.client.delete(reverse("reservation-student-view", kwargs={"student_id": student.student_id}))
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ContractTests(BaseTestSetup):
    def test_create_contract(self):
        for uni in self.universities:
            student = self.create_test_student(uni)
            accommodation = self.create_test_accommodation(uni)
            reservation = self.universities[uni]["reservation_model"].objects.create(student=student, accommodation=accommodation, status="reserved")

            response = self.client.post(reverse("create_contract", kwargs={"reservation_id": reservation.reservation_id}))
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_contract_status(self):
        for uni in self.universities:
            student = self.create_test_student(uni)
            accommodation = self.create_test_accommodation(uni)
            reservation = self.universities[uni]["reservation_model"].objects.create(student=student, accommodation=accommodation, status="reserved")
            contract = self.universities[uni]["contract_model"].objects.create(reservation=reservation, contract_status="unsigned")

            response = self.client.post(reverse("update_signed_status", kwargs={"contract_id": contract.contract_id}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
