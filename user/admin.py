from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (_('login'), {'fields': ('username', 'email', 'password')}),
        (_('Personal Info'), {'fields': ('staff_id','first_name', 'last_name', 'role', 'gender', 'profile', 'branch_code','branch')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('date_joined',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'role')

    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.register(Schedule)