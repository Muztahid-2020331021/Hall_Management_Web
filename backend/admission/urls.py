from django.urls import path, include
from .views import HallViewSet, RoomViewSet, ApplicationViewSet, home
from rest_framework.routers import DefaultRouter

# Create a DefaultRouter instance and register the viewsets
router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')
router.register('room', RoomViewSet, basename='room')
router.register('application', ApplicationViewSet, basename='application')  

# URL patterns
urlpatterns = [
    path('home/', home, name='home'),
    path('', include(router.urls)),  # Use '' instead of 'admission/' since this is already under 'admission/' in backend/urls.py
]
