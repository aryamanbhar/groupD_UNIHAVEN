from django.test import TestCase

# Create your tests here.

from django.test import TestCase, Client
from django.urls import reverse
from .models import Accommodation

class AccommodationListViewTests(TestCase):
    def setUp(self):
        # Create test accommodations
        Accommodation.objects.create(
            property_id="1",
            name="Belcher's Hill",
            type="House",
            availability_start="2025-04-01",
            availability_end="2025-12-31",
            number_of_beds=2,
            number_of_bedrooms=1,
            price=1000.00,
        )
        Accommodation.objects.create(
            property_id="2",
            name="Novum West",
            type="Apartment",
            availability_start="2025-05-01",
            availability_end="2025-10-31",
            number_of_beds=3,
            number_of_bedrooms=2,
            price=1500.00,
        )
        Accommodation.objects.create(
            property_id="3",
            name="Wing Cheung Court",
            type="Apartment",
            availability_start="2025-06-01",
            availability_end="2025-09-30",
            number_of_beds=1,
            number_of_bedrooms=1,
            price=800.00,
            distance=12.0,
        )

        self.client = Client()

    def test_filter_by_type(self):
        response = self.client.get(reverse('accommodation_list'), {'type': 'Apartment'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 2)

    def test_filter_by_availability(self):
        response = self.client.get(reverse('accommodation_list'), {
            'availability_start': '2025-05-01',
            'availability_end': '2025-09-30',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 2)

    def test_filter_by_number_of_beds(self):
        response = self.client.get(reverse('accommodation_list'), {'number_of_beds': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 2)

    def test_filter_by_price_range(self):
        response = self.client.get(reverse('accommodation_list'), {
            'price_min': 900,
            'price_max': 1200,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 1)

    def test_filter_by_distance(self):
        response = self.client.get(reverse('accommodation_list'), {'distance_max': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 2)

    def test_combined_filters(self):
        response = self.client.get(reverse('accommodation_list'), {
            'type': 'Apartment',
            'availability_start': '2025-04-01',
            'availability_end': '2025-12-31',
            'number_of_beds': 2,
            'price_min': 500,
            'price_max': 1500,
            'distance_max': 10,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['accommodations']), 1)
