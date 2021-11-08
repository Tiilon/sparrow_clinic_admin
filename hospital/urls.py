from django.urls import path
from .views import *

app_name = 'hospital'

urlpatterns = [
    path('patients/',patient),
    path('patient/<patient_id>/',patient_details),
    path('patient/vitals/<patient_id>/',vital_signs),
    path('attendance/<patient_id>/',attendance),
    path('clinic-stats/', clinic_day_stats)
]