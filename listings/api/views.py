from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import House
from .serializers import HouseSerializer
from .middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware, RateLimitMiddleware
from django.conf import settings

# TODO: Create your views here.

class HouseFilter(FilterSet):
    """
    Custom filter set for House model with price range filtering.
    """
    min_price = NumberFilter(field_name="price", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')
    min_bedrooms = NumberFilter(field_name="bedrooms", lookup_expr='gte')
    max_bedrooms = NumberFilter(field_name="bedrooms", lookup_expr='lte')
    min_bathrooms = NumberFilter(field_name="bathrooms", lookup_expr='gte')
    max_bathrooms = NumberFilter(field_name="bathrooms", lookup_expr='lte')
    min_home_size = NumberFilter(field_name="home_size", lookup_expr='gte')
    max_home_size = NumberFilter(field_name="home_size", lookup_expr='lte')
    home_type = NumberFilter(field_name="home_type", lookup_expr='iexact')
    city = NumberFilter(field_name="city", lookup_expr='iexact')
    state = NumberFilter(field_name="state", lookup_expr='iexact')
    zipcode = NumberFilter(field_name="zipcode", lookup_expr='exact')

    class Meta:
        model = House
        fields = [
            'min_price',
            'max_price',
            'min_bedrooms',
            'max_bedrooms',
            'min_bathrooms',
            'max_bathrooms',
            'min_home_size',
            'max_home_size',
            'home_type',
            'city',
            'state',
            'zipcode'
        ]

class HouseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling house listings with filtering, pagination, and field selection.
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HouseFilter
    search_fields = ['address', 'city', 'state', 'zipcode']
    ordering_fields = ['price', 'bedrooms', 'bathrooms', 'home_size', 'year_built']
    ordering = ['-price']  # Default ordering
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read operations without auth

    def get_queryset(self):
        """
        Override to handle field selection and additional filtering.
        """
        queryset = super().get_queryset()
        
        # Handle field selection
        fields = self.request.query_params.get('fields', None)
        if fields:
            fields = fields.split(',')
            self.serializer_class.Meta.fields = fields
        
        return queryset

    @action(detail=False, methods=['get'])
    def reset_rate_limit(self, request):
        """Reset the rate limit counter for testing purposes."""
        if not settings.DEBUG:
            return Response(
                {"error": "This endpoint is only available in debug mode"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Reset the rate limit counter
        RateLimitMiddleware.reset_counter()
        return Response({"message": "Rate limit counter reset successfully"})
