from django.http import HttpResponse
from rest_framework import generics
from .models import Donor
from .serializers import DonorSerializer

# Simple index view (optional)
def index(request):
    return HttpResponse("Welcome to the Blood Bank!")

# API views for Donor

class DonorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

class DonorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer

