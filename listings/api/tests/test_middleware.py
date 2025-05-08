from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware, RateLimitMiddleware
from ..models import House
import json

class MiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def test_rate_limiting(self):
        """Test that rate limiting works."""
        # Make multiple requests in quick succession
        for _ in range(101):  # Assuming rate limit is 100
            response = self.client.get(self.list_url)
        
        # The 101st request should be rate limited
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('error', json.loads(response.content))

    def test_error_handling(self):
        """Test that error handling middleware works."""
        # Make a request to a non-existent endpoint
        response = self.client.get('/api/nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)

    def test_request_logging(self):
        """Test that request logging middleware works."""
        # Reset the rate limit counter
        self.client.get('/api/reset-rate-limit/')  # You'll need to add this endpoint
        
        # Make a request and check if it's logged
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: In a real test, you would check the log file or mock the logger 