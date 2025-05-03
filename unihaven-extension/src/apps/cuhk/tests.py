from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from apps.cuhk.models import Accommodation, Reservation, Student, Contract

class FullEndpointTest(APITestCase):
    def setUp(self):
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
            "property_name": "New CUHK Property",
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


#     def setUp(self):
#         self.geocode_patcher = patch('apps.cuhk.models.GeoCodingService.get_coordinates')
#         self.mock_get_coordinates = self.geocode_patcher.start()
#         self.addCleanup(self.geocode_patcher.stop)
#         self.mock_get_coordinates.return_value = {
#             'latitude': 22.3964,
#             'longitude': 114.1095
#         }

#         self.client = APIClient()
#         self.student = Student.objects.create(student_id='1', name="Test Student", contact=123456789, university="CUHK" )
#         self.accommodation = Accommodation.objects.create(property_id=99, property_name="CUHK Property", status="available")
#         self.reservation = Reservation.objects.create(
#             student=self.student,
#             accommodation=self.accommodation,
#             start_date="2025-05-01",
#             end_date="2025-05-15",
#             status="reserved"
#         )
#         self.contract = Contract.objects.create(reservation=self.reservation, contract_status="unsigned")

#     # --------------------
#     # ACCOMMODATIONS
#     # --------------------
#     def test_get_all_accommodations(self):
#         response = self.client.get(reverse("all-accommodations"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_upload_accommodation(self):
#         data = {
#             "property_id": 100,
#             "property_name": "New Property",
#             "status": "available"
#         }
#         response = self.client.post(reverse("accommodation-list"), data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_search_accommodation(self):
#         response = self.client.get(reverse("accommodation-search"), {"price": 1000})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_detail_accommodation(self):
#         # Assume geo_address is same as property_name for now
#         self.accommodation.geo_address = "CUHK Property"
#         self.accommodation.save()
#         response = self.client.get(reverse("accommodation-detail", kwargs={"name": "CUHK Property"}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_rate_accommodation(self):
#         data = {"rating": 4}
#         response = self.client.post(reverse("accommodation-rate", kwargs={"property_id": self.accommodation.property_id}), data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # --------------------
#     # RESERVATIONS
#     # --------------------
#     def test_get_all_reservations_cedars(self):
#         response = self.client.get(reverse("reservation-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_create_reservation(self):
#         data = {
#             "student_id": self.student.student_id,
#             "accommodation": self.accommodation.geo_address,
#             "start_date": "2025-06-01",
#             "end_date": "2025-06-15"
#         }
#         response = self.client.post(reverse("reservation-create"), data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_student_reservation(self):
#         response = self.client.get(reverse("reservation-student-view", kwargs={"student_id": self.student.student_id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_student_reservation(self):
#         response = self.client.delete(reverse("reservation-student-view", kwargs={"student_id": self.student.student_id}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     # --------------------
#     # CONTRACTS
#     # --------------------
#     def test_create_contract(self):
#         # Delete the original one to test creation
#         self.contract.delete()
#         response = self.client.post(reverse("create_contract", kwargs={"reservation_id": self.reservation.reservation_id}))
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_update_failed_status(self):
#         response = self.client.post(reverse("update_failed_status", kwargs={"contract_id": self.contract.contract_id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_signed_status(self):
#         response = self.client.post(reverse("update_signed_status", kwargs={"contract_id": self.contract.contract_id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_all_contracts(self):
#         response = self.client.get(reverse("contract-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # --------------------
#     # STUDENTS
#     # --------------------
#     def test_post_create_student(self):
#         data = {
#             "student_id": "CUHK456",
#             "name": "Another Student",
#             "contact": "987654321"
#         }
#         response = self.client.post(reverse("student-create"), data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_all_students(self):
#         response = self.client.get(reverse("student-list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)




# # from rest_framework.test import APITestCase, APIClient
# # from rest_framework import status
# # from django.urls import reverse
# # from apps.cuhk.models import Accommodation, Reservation, Contract, Student

# # class TestAccommodation(APITestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.accommodation = Accommodation.objects.create(
# #             property_id=1,
# #             property_name="HKUST Test Property",
# #             status="available"
# #         )

# #     def test_list_accommodations(self):
# #         response = self.client.get(reverse("all-accommodations"))
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)

# #     def test_modify_accommodation(self):
# #         url = reverse("modify-accommodation", kwargs={"pk": self.accommodation.id})
# #         updated_data = {
# #             "property_name": "HKUST Updated Property",
# #             "status": "unavailable"
# #         }

# #         response = self.client.put(url, updated_data, format="json")
        
# #         # Ensure update was successful
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #         self.accommodation.refresh_from_db()
# #         self.assertEqual(self.accommodation.property_name, updated_data["property_name"])
# #         self.assertEqual(self.accommodation.status, updated_data["status"])

# # class TestReservation(APITestCase):
# #     def setUp(self):
# #         self.client = APIClient()
# #         self.student = Student.objects.create(student_id="CUHK123", name="Test Student", contact="123456789")
# #         self.accommodation = Accommodation.objects.create(property_id=2, property_name="CUHK Property", status="available")

# #     def test_create_reservation(self):
# #         reservation_data = {
# #             "student_id": self.student.student_id,
# #             "accommodation": self.accommodation.id,
# #             "start_date": "2025-05-01",
# #             "end_date": "2025-05-15"
# #         }
# #         response = self.client.post(reverse("reservation-create"), reservation_data, format="json")
# #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
