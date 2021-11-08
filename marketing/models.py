from management.models import Branch
from hospital.models import Patient
from django.db import models
from hospital.models import Patient, Attendance
from django.utils import timezone
from user.models import User


class Feedback(models.Model):
    attendance = models.OneToOneField(Attendance, related_name="feedback", on_delete=models.CASCADE, null=True, blank=True)
    reception = models.IntegerField(default=0, blank=True, null=True)
    nurse = models.IntegerField(default=0, blank=True, null=True)
    doctor = models.IntegerField(default=0, blank=True, null=True)
    lab = models.IntegerField(default=0, blank=True, null=True)
    pharmacy = models.IntegerField(default=0, blank=True, null=True)
    cashier = models.IntegerField(default=0, blank=True, null=True)
    house_keeper = models.IntegerField(default=0, blank=True, null=True)
    overall = models.IntegerField(default=0, blank=True, null=True)
    opinion = models.TextField(null=True, blank=True)
    best_staff = models.CharField(max_length=255, blank=True, null=True)
    how_did_you_hear_abt_rabito = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='feedback_user', blank=True, null=True)

    def __str__(self):
        return self.attendance.patient.full_name()
