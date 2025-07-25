# =====================
# user_info/serializers.py
# =====================
from rest_framework import serializers
from .models import UserInformation, Hall
from student_admission.models import Student
from official.models import ProvostBody, OfficialPerson, Dining_Shop_Canteen

# ================
# USER SERIALIZER
# ================
class UserInformationSerializer(serializers.ModelSerializer):
    hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all(), allow_null=True)

    class Meta:
        model = UserInformation
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserInformation(**validated_data)
        if password:
            from django.contrib.auth.hashers import make_password
            user.password = make_password(password)
        user.save()
        return user

# =================
# OTHER SERIALIZERS
# =================
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ProvostBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvostBody
        fields = '__all__'

class OfficialPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialPerson
        fields = '__all__'

class DiningShopCanteenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dining_Shop_Canteen
        fields = '__all__'
