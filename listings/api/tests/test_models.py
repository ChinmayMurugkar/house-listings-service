from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import House

class HouseModelTest(TestCase):
    def setUp(self):
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

    def test_create_house(self):
        """Test creating a house with valid data."""
        house = House.objects.create(**self.house_data)
        self.assertEqual(house.address, self.house_data['address'])
        self.assertEqual(house.price, self.house_data['price'])
        self.assertEqual(house.bedrooms, self.house_data['bedrooms'])

    def test_negative_price(self):
        """Test that negative price is not allowed."""
        self.house_data['price'] = -100000.00
        with self.assertRaises(ValidationError):
            house = House(**self.house_data)
            house.full_clean()

    def test_negative_bedrooms(self):
        """Test that negative bedrooms is not allowed."""
        self.house_data['bedrooms'] = -1
        with self.assertRaises(ValidationError):
            house = House(**self.house_data)
            house.full_clean()

    def test_negative_bathrooms(self):
        """Test that negative bathrooms is not allowed."""
        self.house_data['bathrooms'] = -1.0
        with self.assertRaises(ValidationError):
            house = House(**self.house_data)
            house.full_clean()

    def test_negative_home_size(self):
        """Test that negative home size is not allowed."""
        self.house_data['home_size'] = -100
        with self.assertRaises(ValidationError):
            house = House(**self.house_data)
            house.full_clean() 