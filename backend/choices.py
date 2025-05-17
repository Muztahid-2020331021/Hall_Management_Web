from django.db import models, transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
# =====================
# Role 
# =====================
User_Role=[('Student', 'Student'),( 'Provost_Body', 'Provost Body'),('Official_Person', 'Official Person'),('Dining', 'Dining'),('Canteen', 'Canteen'),('Shop', 'Shop')]
Provost_Body_Role=[('Provost', 'Provost'),('Assistant_Provost', 'Assistant Provost')]
Department_Role=[( 'Professor', 'Professor'),('Associate_Professor', 'Associate Professor'),('Assistant_Professor', 'Assistant Professor'),('Lecturer', 'Lecturer')]
Office_Person_Role=[('ASSISTANT_Register', 'Assistant Register'),('Administrative_Officer', 'Administrative Officer'),('Accountant', 'Accountant'),('Cleaner', 'Cleaner'),('Electrician', 'Electrician'),('Plumber', 'Plumber'),('Swiper', 'Swiper'),('Gardener', 'Gardener'),('Office_Assistant', 'Office Assistant'),( 'Office_Attendant', 'Office Attendant'),('Guard', 'Guard'),('Senior_Assistant', 'Senior Assistant'),( 'Dining_Shopping_Canteen', 'Dining/Shopping/Canteen')]

Complain_tag=[('Water_Supply','Water Supply'),('Room_Clean','Room Clean'),('Toilet_Clean','Toilet_Clean'),('Bathroom','Bathroom'),('Electric','Electric'),('Dining','Dining'),('Shop','Shop'),('Canteen','Canteen'),('Wi_Fi','Wi-Fi'),('Reading_Room','Reading Room'),('Drainage_System','Drainage System'),('Bed','Bed'),('Locker','Locker'),('Window_Glass','Window Glass'),('Mosquito_Net_Stand','Mosquito Net Stand'),('Administrative','Administrative'),('Others','Others')]

STUDY_PROGRAM_CHOICES = [('UnderGraduate', 'UnderGraduate'), ('Graduate', 'Graduate')]
GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
SESSION_CHOICES = [('2019', '2019-2020'), ('2020', '2020-2021'), ('2021', '2021-2022'),
                   ('2023', '2023-2024'), ('2024', '2024-2025')]
SEMESTER_CHOICES = [('1/1', '1/1'), ('1/2', '1/2'), ('2/1', '2/1'), ('2/2', '2/2'),
                    ('3/1', '3/1'), ('3/2', '3/2'), ('4/1', '4/1'),('4/2','4/2'), ('M/1', 'M/1'),
                    ('M/2', 'M/2'), ('M/3', 'M/3')]