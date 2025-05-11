from django.db import models
from django.core.exceptions import ValidationError


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(max_length=100)
    total_room = models.PositiveIntegerField()
    total_number_of_seat = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='hall_images/')

    def __str__(self):
        return self.hall_name

    @property
    def vacant_seats(self):
        return self.total_number_of_seat - self.admitted_students

    def clean(self):
        if self.admitted_students > self.total_number_of_seat:
            raise ValidationError("Admitted students cannot exceed total number of seats.")

    def admit_student(self):
        if self.admitted_students >= self.total_number_of_seat:
            raise ValidationError("No vacant seat available in the hall.")
        self.admitted_students += 1
        self.save()


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField(default=0)
    student_list = models.JSONField(default=list, blank=True)  # To store registration numbers

    def __str__(self):
        return self.room_number

    @property
    def vacancy(self):
        return self.capacity - self.admitted_students

    def clean(self):
        if self.admitted_students > self.capacity:
            raise ValidationError("Admitted students cannot exceed room capacity.")

    def admit_student(self, registration_number):
        if self.admitted_students >= self.capacity:
            raise ValidationError(f"Room {self.room_number} is full.")
        if registration_number in self.student_list:
            raise ValidationError(f"Student {registration_number} already in room.")
        self.admitted_students += 1
        self.student_list.append(registration_number)
        self.save()


class Application(models.Model):
    STUDY_PROGRAM_CHOICES = [('honors', 'Honors'), ('masters', 'Masters')]
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    SESSION_CHOICES = [('2019', '2019-2020'), ('2020', '2020-2021'), ('2021', '2021-2022'), ('2023', '2023-2024'), ('2024', '2024-2025')]
    SEMESTER_CHOICES = [('1/1', '1/1'), ('1/2', '1/2'), ('2/1', '2/1'), ('2/2', '2/2'), ('3/1', '3/1'), ('3/2', '3/2'), ('4/1', '4/1'), ('M/1', 'M/1'), ('M/2', 'M/2'), ('M/3', 'M/3')]

    registration_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    blood_group = models.CharField(max_length=10)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department_code = models.CharField(max_length=10)
    study_program = models.CharField(max_length=10, choices=STUDY_PROGRAM_CHOICES)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    premanent_address = models.TextField()
    home_distance_from_SUST_in_km = models.FloatField()
    monthly_income = models.PositiveIntegerField()
    special_reason_for_hall_seat = models.TextField(blank=True, null=True)
    total_credits_offered = models.FloatField()
    total_credits_completed = models.FloatField()
    cgpa = models.FloatField()
    last_semester_gpa = models.FloatField()
    attached_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    is_resident = models.BooleanField()
    resident_months_in_university_hall = models.PositiveIntegerField(blank=True, null=True)
    convicted = models.BooleanField()
    profile_picture = models.ImageField(upload_to='student_profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.registration_number


class UserInformation(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)  # ✅ Added password field
    role = models.CharField(max_length=20, default='student')
    blood_group = models.CharField(max_length=5)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.email


class Student(models.Model):
    registration_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    department = models.CharField(max_length=100, default='Default Department')  # Set a default here
    semester = models.CharField(max_length=20)
    room_number = models.CharField(max_length=10)

    def __str__(self):
        return self.registration_number

class Admission(models.Model):
    registration_number = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        to_field='registration_number',
        primary_key=True
    )
    registration_number_str = models.CharField(max_length=15, editable=False, blank=True, null=True)
    password = models.CharField(max_length=100)
    room_number = models.ForeignKey(Room, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        application = self.registration_number  # Application instance

        # Store registration number as string for __str__ use
        self.registration_number_str = application.registration_number

        try:
            room = Room.objects.get(room_number=self.room_number.room_number, hall=self.hall)
        except Room.DoesNotExist:
            raise ValidationError(f"Room {self.room_number} in {self.hall.hall_name} not found.")

        room.admit_student(application.registration_number)
        self.hall.admit_student()

        super().save(*args, **kwargs)

        # Add or update UserInformation
        UserInformation.objects.update_or_create(
            email=application.email,
            defaults={
                'name': application.name,
                'image': application.profile_picture,
                'phone_number': application.phone_number,
                'password': self.password,
                'blood_group': application.blood_group,
                'hall': self.hall
            }
        )

        # Add or update Student
        Student.objects.update_or_create(
            registration_number=application.registration_number,
            defaults={
                'email': application.email,
                'department': application.department_code,
                'semester': application.semester,
                'room_number': self.room_number.room_number
            }
        )

        # Delete the application after admission
        application.delete()

    def __str__(self):
        return self.registration_number_str or "Admission"