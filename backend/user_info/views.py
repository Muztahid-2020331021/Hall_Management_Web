# =====================
# user_info/views.py
# =====================

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from user_info.models import UserInformation
from student_admission.models import Student
from official.models import ProvostBody, OfficialPerson, Dining_Shop_Canteen
from user_info.serializers import (
    UserInformationSerializer,
    StudentSerializer,
    ProvostBodySerializer,
    OfficialPersonSerializer,
    DiningShopCanteenSerializer,
)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()

        if not email or not password:
            return Response(
                {'detail': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserInformation.objects.get(email=email)

            # Plain text password check (not secure, only for demo/testing)
            if password != user.password:
                return Response(
                    {'detail': 'Invalid credentials.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            serializer = UserInformationSerializer(user)
            return Response({
                "message": "Login successful",
                "user": serializer.data
            })

        except UserInformation.DoesNotExist:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class UserDetailsByEmail(APIView):
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserInformation.objects.get(email=email)
        except UserInformation.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user_info_data = UserInformationSerializer(user).data
        role = user.user_role
        extra_data = {}

        if role == "student":
            student = Student.objects.filter(email=user).first()
            if student:
                extra_data = StudentSerializer(student).data

        elif role == "provost_body":
            provost = ProvostBody.objects.filter(email=user).first()
            if provost:
                extra_data = ProvostBodySerializer(provost).data

        elif role == "official_person":
            official = OfficialPerson.objects.filter(email=user).first()
            if official:
                extra_data = OfficialPersonSerializer(official).data

        elif role == "dining_canteen_shop":
            dining = Dining_Shop_Canteen.objects.filter(email=user).first()
            if dining:
                extra_data = DiningShopCanteenSerializer(dining).data

        return Response({
            "user_info": user_info_data,
            "extra_info": extra_data,
            "user_role": role
        })

class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = UserInformation.objects.all()
    serializer_class = UserInformationSerializer
