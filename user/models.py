from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from management.models import Branch

class UserManager(BaseUserManager):
    def create_user(self,email, first_name,last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return user

    
    def create_superuser(self,email,first_name,last_name,password):
        user = self.create_user(email=email,first_name=first_name,last_name=last_name,password=password)

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.username = first_name
        user.save(using=self.db)

        return user

ROLE = {
    ('ADMIN','ADMIN'),
    ('CEO','CEO'),
    ('NURSE','NURSE'),
    ('DOCTOR','DOCTOR'),
    ('HR','HR'),
    ('MARKETING','MARKETING'),
}

GENDER = {
    ('MALE','MALE'),
    ('FEMALE','FEMALE'),
}

Contacts = {
    ('0500009652','0500009652'),
    ('0200009652','0200009652'),
}

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    contact = models.CharField(max_length=255, blank=True, null=True, choices=Contacts)
    gender = models.CharField(max_length=255, blank=True, null=True, choices=GENDER)
    staff_id = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True, choices=ROLE)
    profile = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, blank=True, null=True)
    branch_code = models.CharField(max_length=255, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, related_name='user_branch', blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'user'
        ordering = ('-first_name',)

    def __str__(self):
        return f"{self.get_full_name()}"


class Schedule(models.Model):
    description= models.CharField(max_length=255,blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    # end_date = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="schedule")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'schedule'