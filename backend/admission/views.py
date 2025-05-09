from rest_framework import viewsets
from .models import Hall, Room, Application
from .serializers import *
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Hall Management System!")

class HallViewSet(viewsets.ModelViewSet):
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
