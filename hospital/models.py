from django.db import models
from django.utils import timezone
from random import randrange
from user.models import User

def generate():
    FROM = '0123456789'
    LENGTH = 10
    pat_id = ""
    for i in range(LENGTH):
        pat_id += FROM[randrange(0, len(FROM))]

    return f"PT{pat_id}-{timezone.now().year}"

class Patient(models.Model):
    patient_id = models.CharField(default=generate, unique=True, editable=False, max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=100,blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    notes = models.ManyToManyField('Note', related_name='patient_notes', blank=True)
    is_first_time = models.BooleanField(default=True)
    is_discharged = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='patients', blank=True, null=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'patient'
        ordering = ['-first_name']

class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name='patient_diagnosis', blank=True, null=True)
    complaints = models.CharField(max_length=1000, blank=True, null=True)
    symptoms = models.CharField(max_length=2000, blank=True, null=True)
    diagnosis = models.CharField(max_length=100,blank=True, null=True)
    attendance = models.ForeignKey('Attendance', blank=True, null=True, on_delete=models.CASCADE, related_name="diagnosis_attendance")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='diagnosis', blank=True, null=True)

    def __str__(self):
        return self.diagnosis

    class Meta:
        db_table= 'medical diagnosis'
        ordering = ('-created_at',)

class Note(models.Model):
    note = models.TextField(max_length=3000, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name='note_patient', blank=True, null=True)
    attendance = models.ForeignKey('Attendance', blank=True, null=True, on_delete=models.CASCADE, related_name="note_attendance")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='notes', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.note)

    class Meta:
        db_table = 'note'
        ordering = ('-created_at',)

class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True, related_name='vital_sign_patient')
    time = models.TimeField(default=timezone.now)
    weight = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True)
    diastolic = models.IntegerField( blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    systolic = models.IntegerField( blank=True, null=True)
    respiration = models.IntegerField( blank=True, null=True)
    temperature = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True)
    attendance = models.ForeignKey('Attendance', blank=True, null=True, on_delete=models.CASCADE, related_name="vitals_attendance")
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='vital_signs')

    class Meta:
        db_table = 'vital_sign'
        ordering = ('-time',)

    def __str__(self):
        return f"{self.patient.patient_id}-{self.time}"


class Attendance(models.Model):
    patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.CASCADE, related_name="attendance")
    branch = models.CharField(max_length=100, blank=True, null=True)
    is_recorded = models.BooleanField(default=False)
    is_walk_in = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="patient_attendance")

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

    class Meta:
        db_table = 'attendance'
        ordering = ('-created_by',)
