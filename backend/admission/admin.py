from django.contrib import admin
from .models import Hall, Room, Application, Admission, UserInformation, Student

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

# Register the UserInformation admin
@admin.register(UserInformation)
class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'role', 'hall')
    search_fields = ['email', 'name', 'phone_number', 'role', 'hall__hall_name']
    list_filter = ('role',)

# Register the Hall admin
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    inlines = [RoomInline]
    list_display = ('hall_name', 'total_room', 'total_number_of_seat', 'admitted_students', 'vacant_seats_display')

    search_fields = ['hall_name']

    def vacant_seats_display(self, obj):
        return obj.vacant_seats
    vacant_seats_display.short_description = 'Vacant Seats'

# Register the Room admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hall', 'capacity', 'admitted_students', 'vacancy_display','student_list')
    search_fields = ['room_number', 'hall__hall_name','student_list']  # Adjusted to search by hall name

    def vacancy_display(self, obj):
        return obj.vacancy
    vacancy_display.short_description = 'Vacancy'

# Register the Application admin
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'name', 'department_code', 'study_program',
        'session', 'semester', 'cgpa', 'last_semester_gpa', 'attached_hall',
        'is_resident_in_any_hall', 'home_distance_from_SUST_in_km'
    )
    search_fields = ['registration_number', 'name', 'department_code', 'attached_hall__hall_name']
    list_filter = ['study_program', 'gender', 'is_resident', 'attached_hall', 'session']
    list_per_page = 25

    def is_resident_in_any_hall(self, obj):
        return "Yes" if obj.is_resident else "No"
    is_resident_in_any_hall.short_description = 'Is Resident in Any Hall'

# Register the Admission model
admin.site.register(Admission)

# Register the Student admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'email', 'department', 'semester', 'room_number')
    search_fields = ('registration_number', 'email', 'department', 'semester', 'room_number')
    list_filter = ('department', 'semester')
