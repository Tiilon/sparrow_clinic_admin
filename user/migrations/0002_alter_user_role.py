# Generated by Django 3.2.6 on 2021-09-07 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('HR', 'HR'), ('MARKETING', 'MARKETING'), ('NURSE', 'NURSE'), ('ADMIN', 'ADMIN'), ('CEO', 'CEO'), ('DOCTOR', 'DOCTOR')], max_length=255, null=True),
        ),
    ]
