from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import House

class HouseViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.house_data = {
            'area_unit': 'SqFt',
            'bathrooms': 2.0,
            'bedrooms': 3,
            'home_size': 2000,
            'home_type': 'Single Family',
            'link': 'https://example.com/house',
            'price': 300000.00,
            'zillow_id': '123456',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'TS',
            'zipcode': '12345'
        }
        self.house = House.objects.create(**self.house_data)
        self.list_url = reverse('house-list')
        self.detail_url = reverse('house-detail', kwargs={'pk': self.house.pk})

    def test_list_houses(self):
        """Test listing all houses."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_house(self):
        """Test retrieving a single house."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['address'], self.house_data['address'])

    def test_filter_by_price(self):
        """Test filtering houses by price range."""
        response = self.client.get(f"{self.list_url}?min_price=200000&max_price=400000")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_bedrooms(self):
        """Test filtering houses by number of bedrooms."""
        response = self.client.get(f"{self.list_url}?min_bedrooms=2&max_bedrooms=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search(self):
        """Test searching houses."""
        response = self.client.get(f"{self.list_url}?search=Test City")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering(self):
        """Test ordering houses."""
        # Create another house with higher price
        house2_data = self.house_data.copy()
        house2_data['price'] = 400000.00
        house2_data['zillow_id'] = '123457'  # Unique zillow_id
        House.objects.create(**house2_data)

        # Test ascending order
        response = self.client.get(f"{self.list_url}?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['results'][0]['price']), 300000.00)

        # Test descending order
        response = self.client.get(f"{self.list_url}?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['results'][0]['price']), 400000.00)

    def test_field_selection(self):
        """Test selecting specific fields."""
        response = self.client.get(f"{self.list_url}?fields=id,address,price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('address', response.data['results'][0])
        self.assertIn('price', response.data['results'][0])
        self.assertNotIn('bedrooms', response.data['results'][0]) 