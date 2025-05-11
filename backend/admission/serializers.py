# serializers.py
from rest_framework import serializers
from .models import *

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        # Extract necessary data from Application
        registration_number = validated_data.get('registration_number')
        hall_name = validated_data.get('attached_hall')
        room_number = validated_data.get('room_number')

        # Perform creation of the Admission, UserInformation, and Student objects via signals or after save.
        # This avoids manually handling the creation within the serializer and adheres to Django best practices.
        
        return validated_data


