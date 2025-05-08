import time
import logging
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log all API requests and their response times.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timer
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log the request
        logger.info(
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.2f}s"
        )

        return response

class ErrorHandlingMiddleware:
    """
    Middleware to handle exceptions and return standardized error responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if response.status_code >= 400:
            error_message = {
                404: 'Not found',
                400: 'Bad request',
                401: 'Unauthorized',
                403: 'Forbidden',
                405: 'Method not allowed',
                500: 'Internal server error'
            }.get(response.status_code, 'An error occurred')
            
            return JsonResponse({
                'error': error_message,
                'status_code': response.status_code,
                'path': request.path
            }, status=response.status_code)
        
        return response

class RateLimitMiddleware:
    """
    Middleware to implement rate limiting on API endpoints.
    """
    _request_count = 0
    _last_reset = time.time()
    _rate_limit = getattr(settings, 'API_RATE_LIMIT', 100)  # Default to 100 requests per minute
    _window = 60  # 1 minute window

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip rate limiting for non-API requests
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        current_time = time.time()
        
        # Reset counter if window has passed
        if current_time - self._last_reset >= self._window:
            self._request_count = 0
            self._last_reset = current_time
        
        # Increment counter
        self._request_count += 1
        
        # Check if rate limit exceeded
        if self._request_count > self._rate_limit:
            return JsonResponse({
                'error': 'Rate limit exceeded',
                'detail': f'Too many requests. Limit is {self._rate_limit} requests per minute.'
            }, status=429)
        
        return self.get_response(request)

    @classmethod
    def reset_counter(cls):
        """Reset the rate limit counter."""
        cls._request_count = 0
        cls._last_reset = time.time()

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 