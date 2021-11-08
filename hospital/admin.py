from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Attendance)
admin.site.register(Diagnosis)
admin.site.register(Note)
admin.site.register(VitalSign)
