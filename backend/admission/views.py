
# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Hall, Room, Application, Admission, UserInformation, Student
from .serializers import HallSerializer, RoomSerializer, ApplicationSerializer

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

    @action(detail=True, methods=['post'])
    def admit_student(self, request, pk=None):
        application = self.get_object()

        registration_number = application.registration_number
        hall_name = application.attached_hall
        room_number = application.room_number

        try:
            # Check if the room and hall are available
            hall = Hall.objects.get(hall_name=hall_name)
            room = Room.objects.get(room_number=room_number, hall=hall)

            if room.admitted_students >= room.capacity:
                return Response({"error": "Room is already full"}, status=status.HTTP_400_BAD_REQUEST)
            if hall.admitted_students >= hall.total_number_of_seat:
                return Response({"error": "Hall is already full"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the Admission object
            admission = Admission.objects.create(
                registration_number=application.registration_number,
                room_number=room,
                hall=hall,
                password='defaultpassword'  # Set a default password or implement dynamic password logic
            )

            # Create the UserInformation object
            user_information = UserInformation.objects.create(
                email=application.email,
                name=application.name,
                image=None,  # If image handling is needed, modify this
                phone_number=application.phone_number,
                role='student',  # Default role is 'student'
                blood_group=application.blood_group,
                hall=hall,
            )

            # Create the Student object
            student = Student.objects.create(
                registration_number=application.registration_number,
                email=application.email,
                department=application.department_code,
                semester=application.semester,
                room_number=room_number,
            )

            # Update the admitted student count in Hall and Room
            hall.admitted_students += 1
            room.admitted_students += 1

            hall.save()
            room.save()

            # Return a success response
            return Response({
                "status": "success",
                "message": "Student admitted successfully."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
