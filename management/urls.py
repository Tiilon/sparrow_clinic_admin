from management.views import *
from django.urls import path
from .views import *

app_name = 'management'

urlpatterns = [
    path('user/',user),
    path('user/<staff_id>/', staff_details),
    path('branches/', branch),
    path('delete-branch/<id>/', delete_branch),
]