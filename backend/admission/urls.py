from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

# Create a DefaultRouter instance and register Hall, Room, and Application ViewSets
router = DefaultRouter()
router.register('hall', HallViewSet, basename='hall')
router.register('room', RoomViewSet, basename='room')
router.register('application', ApplicationViewSet, basename='application')  

# URL patterns
urlpatterns = [
    path('home/', home, name='home'),  # Custom home view
    path('admission/', include(router.urls)),  # API endpoints handled by the router
]
