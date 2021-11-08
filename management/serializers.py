from rest_framework import serializers
from user.serializers import UserSerializer
from .models import *
from user.models import User


class BranchSerializer(serializers.ModelSerializer):
    staffs = serializers.SerializerMethodField(method_name='get_staffNumber')
    class Meta:
        model = Branch
        fields = ['id','name', 'code', 'staffs']

    def get_staffNumber(self,instance):
        staffs = User.objects.filter(branch_code=instance.code)
        return staffs.count()



class AddBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','name', 'code']
