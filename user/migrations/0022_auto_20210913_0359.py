# Generated by Django 3.2.7 on 2021-09-13 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('ADMIN', 'ADMIN'), ('NURSE', 'NURSE'), ('MARKETING', 'MARKETING'), ('CEO', 'CEO'), ('HR', 'HR'), ('DOCTOR', 'DOCTOR')], max_length=255, null=True),
        ),
    ]
