from django.urls import path
from . import views

urlpatterns = [
    # Optional index route
    path('', views.index, name='blood_bank_index'),

    # Donor API endpoints
    path('donors/', views.DonorListCreateAPIView.as_view(), name='donor-list-create'),
    path('donors/<int:pk>/', views.DonorRetrieveUpdateDestroyAPIView.as_view(), name='donor-detail'),
]
