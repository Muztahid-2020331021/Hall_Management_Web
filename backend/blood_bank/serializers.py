from rest_framework import serializers
from .models import Donor
from user_info.serializers import UserInformationSerializer  # If you want nested info

class DonorSerializer(serializers.ModelSerializer):
    # Optional: nested serialization for full_name (UserInformation)
    full_name = serializers.StringRelatedField()  # Just the string representation (name)
    # Or for full nested object:
    # full_name = UserInformationSerializer(read_only=True)

    class Meta:
        model = Donor
        fields = '__all__'
