#=====================
# blood_bank/models.py
#=====================
from django.db import models
from datetime import date, timedelta
import choices
from user_info.models import UserInformation, Hall  # Explicit imports

class Donor(models.Model):
    full_name = models.CharField(max_length=255, help_text='Full name of the donor')
    
    # Optional: If email/phone are already in UserInformation, remove these
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    blood_group = models.CharField(max_length=30, choices=choices.BLOOD_GROUP_CHOICES)
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True)
    
    user_role = models.CharField(max_length=100, choices=choices.USER_ROLE, default='student')

    department = models.CharField(max_length=100, blank=True, null=True, help_text='Only for Provost Body and Student')
    
    provost_body_role = models.CharField(
        max_length=100,
        choices=choices.PROVOST_BODY_ROLE,
        blank=True, null=True,
        help_text='Only for Provost Body'
    )
    
    department_role = models.CharField(
        max_length=100,
        choices=choices.DEPARTMENT_ROLE,
        blank=True, null=True,
        help_text='Only for Provost Body'
    )
    
    official_role = models.CharField(
        max_length=100,
        choices=choices.OFFICE_PERSON_ROLE,
        default='assistant_register',
        blank=True, null=True,
        help_text='Only for Official Person or Dining/Shop/Canteen'
    )

    last_donation_date = models.DateField(null=True, blank=True)
    willing_to_donate = models.BooleanField(default=True, editable=False)

    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

    def save(self, *args, **kwargs):
        # Automatically set willing_to_donate
        if self.last_donation_date:
            days_since_last_donation = (date.today() - self.last_donation_date).days
            self.willing_to_donate = days_since_last_donation >= 120
        else:
            # Never donated → willing by default
            self.willing_to_donate = True

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-last_donation_date']
