from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'blood_group', 'hall', 'last_donation_date', 'willing_to_donate', 'user_role')
    list_filter = ('blood_group', 'hall', 'user_role', 'willing_to_donate')
    search_fields = ('blood_group','full_name__name', 'email', 'phone')
    ordering = ('-last_donation_date',)
