# Generated by Django 3.2.7 on 2021-10-10 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_auto_20211010_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('FEMALE', 'FEMALE'), ('MALE', 'MALE')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('NURSE', 'NURSE'), ('ADMIN', 'ADMIN'), ('HR', 'HR'), ('CEO', 'CEO'), ('MARKETING', 'MARKETING'), ('DOCTOR', 'DOCTOR')], max_length=255, null=True),
        ),
    ]
