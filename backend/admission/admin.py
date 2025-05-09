from django.contrib import admin
from .models import *

# Register your models here
class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

class HallAdmin(admin.ModelAdmin):
    inlines = [RoomInline]  # Shows Room inline in Hall admin page
    list_display = ('hall_name', 'total_room', 'total_number_of_seat', 'admitted_students', 'vacant_seats')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hall', 'capacity', 'admitted_students', 'vacancy')

class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'name', 'department_code', 'study_program',
        'session', 'semester', 'cgpa', 'last_semester_gpa', 'attached_hall',
        'is_resident_in_any_hall', 'distance_from_sust_km'
    )
    search_fields = ['registration_number', 'name', 'department_code', 'attached_hall']
    list_filter = ['study_program', 'gender', 'is_resident', 'attached_hall', 'session']
    readonly_fields = []
    list_per_page = 25

    # Use fields to specify the order and fields to display in the form
    fields = (
        'registration_number', 'name', 'phone_number', 'blood_group', 'father_name', 'mother_name',
        'gender', 'department_code', 'study_program', 'session', 'semester', 'present_address',
        'distance_from_sust_km', 'monthly_income', 'special_reason_for_hall_seat', 'total_credits_offered',
        'total_credits_completed', 'cgpa', 'last_semester_gpa', 'resident_months', 
        'attached_hall', 'is_resident', 'convicted'
    )

    # Custom method to display 'Is Resident in Any Hall'
    def is_resident_in_any_hall(self, obj):
        return "Yes" if obj.is_resident else "No"
    is_resident_in_any_hall.short_description = 'Is Resident in Any Hall'  # Custom column title

admin.site.register(Hall, HallAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Application, ApplicationAdmin)
