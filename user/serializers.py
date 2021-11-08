from rest_framework import serializers
from .models import Schedule, User
from management.models import Branch
# from management.serializers import *

class UserBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','name', 'code']

        
class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = User
        fields = ('staff_id', 'first_name', 'last_name', 'email', 'gender', 'date_joined', 'role', 'contact', 'profile','branch_code')

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('staff_id', 'first_name', 'last_name', 'email', 'gender', 'branch_code', 'role', 'contact', 'profile')

class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%d")
    # end_date = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = Schedule
        fields = ('description', 'date', 'start_time', 'end_time')


