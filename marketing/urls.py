from django.urls import path
from .views import *

app_name = 'marketing'

urlpatterns = [
    path('feedback/',attendances_feedback),
    path('feedback/<id>/',feedback),
    path('analyses/',analyses),
    path('reports/',feedback_reports),
    path('dashboard/',dashboard),
]