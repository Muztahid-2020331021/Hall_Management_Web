from django.db import models

# Create your models here.
from django.db import models

class Hall(models.Model):
    hall_name = models.CharField(max_length=100)
    total_room = models.PositiveIntegerField()
    total_number_of_seat = models.PositiveIntegerField()
    admitted_students = models.PositiveIntegerField()
    vacant_seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hall_images/')

    def __str__(self):
        return self.hall_name


# python3 manage.py makemigrations
# python3 manage.py migrate
# python3 manage.py runserver
