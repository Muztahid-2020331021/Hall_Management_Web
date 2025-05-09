from django.db import models
from django.core.exceptions import ValidationError

class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(max_length=100)
    total_room = models.PositiveIntegerField()
    total_number_of_seat = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hall_images/')

    def __str__(self):
        return self.hall_name

    @property
    def vacant_seats(self):
        return self.total_number_of_seat - self.admitted_students

    def clean(self):
        if self.admitted_students > self.total_number_of_seat:
            raise ValidationError("Admitted students cannot exceed total number of seats.")


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {self.room_number} in {self.hall.hall_name}"

    @property
    def vacancy(self):
        return self.capacity - self.admitted_students

    def clean(self):
        if self.admitted_students > self.capacity:
            raise ValidationError("Admitted students cannot exceed room capacity.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is called before saving
        super().save(*args, **kwargs)



from django.db import models
from django.core.exceptions import ValidationError

class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    hall_name = models.CharField(max_length=100)
    total_room = models.PositiveIntegerField()
    total_number_of_seat = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hall_images/')

    def __str__(self):
        return self.hall_name

    @property
    def vacant_seats(self):
        return self.total_number_of_seat - self.admitted_students

    def clean(self):
        if self.admitted_students > self.total_number_of_seat:
            raise ValidationError("Admitted students cannot exceed total number of seats.")


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=10)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {self.room_number} in {self.hall.hall_name}"

    @property
    def vacancy(self):
        return self.capacity - self.admitted_students

    def clean(self):
        if self.admitted_students > self.capacity:
            raise ValidationError("Admitted students cannot exceed room capacity.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is called before saving
        super().save(*args, **kwargs)


class Application(models.Model):
    STUDY_PROGRAM_CHOICES = [
        ('honors', 'Honors'),
        ('masters', 'Masters'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    HALL_CHOICES = [
        ('a', 'Shahparan Hall'),
        ('b', 'Bangabandhu Hall'),
        ('c', 'Syed Mujtaba Ali Hall'),
    ]
    
    SESSION_CHOICES = [
        ('2019-2020', 2019),
        ('2020-2021', 2020),
        ('2021-2022', 2021),
        ('2023-2024', 2023),
        ('2024-2025', 2024),
    ]
    
    SEMESTER_CHOICES = [
        ('1/1', '1/1'),
        ('1/2', '1/2'),
        ('2/1', '2/1'),
        ('2/2', '2/2'),
        ('3/1', '3/1'),
        ('3/2', '3/2'),
        ('4/1', '4/1'),
        ('M/1', 'M/1'),
        ('M/2', 'M/2'),
        ('M/3', 'M/3'),
    ]

    registration_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    department_code = models.CharField(max_length=10)
    study_program = models.CharField(max_length=10, choices=STUDY_PROGRAM_CHOICES)
    session = models.CharField(max_length=10, choices=SESSION_CHOICES)  # like 20-21
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    present_address = models.TextField()
    distance_from_sust_km = models.FloatField(verbose_name="SUST Distance (in Km)")
    monthly_income = models.PositiveIntegerField()
    special_reason_for_hall_seat = models.TextField(blank=True, null=True)
    total_credits_offered = models.FloatField()
    total_credits_completed = models.FloatField()
    cgpa = models.FloatField()
    last_semester_gpa = models.FloatField()
    attached_hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    is_resident = models.BooleanField()
    resident_months = models.PositiveIntegerField(blank=True, null=True)
    convicted = models.BooleanField(help_text="Have you ever been convicted for violation of any rule?")

    def __str__(self):
        return f"{self.registration_number} - {self.name}"



# source django_env/bin/activate
# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver
