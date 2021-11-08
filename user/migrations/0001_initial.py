# Generated by Django 3.2.6 on 2021-09-07 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], max_length=255, null=True)),
                ('staff_id', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.CharField(blank=True, choices=[('ADMIN', 'ADMIN'), ('NURSE', 'NURSE'), ('CEO', 'CEO'), ('HR', 'HR'), ('DOCTOR', 'DOCTOR'), ('MARKETING', 'MARKETING')], max_length=255, null=True)),
                ('profile', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('is_staff', models.BooleanField(blank=True, default=True, null=True)),
                ('is_superuser', models.BooleanField(blank=True, default=False, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staffs', to='management.branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'ordering': ('-first_name',),
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schedule', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
