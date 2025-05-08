from django.contrib import admin
from .models import Hall

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('hall_name', 'total_room', 'total_number_of_seat', 'admitted_students', 'vacant_seats')
