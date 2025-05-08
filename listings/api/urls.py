from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import HouseViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'houses', HouseViewSet, basename='house')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
