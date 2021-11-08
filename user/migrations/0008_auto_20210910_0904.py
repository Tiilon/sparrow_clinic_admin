# Generated by Django 3.2.7 on 2021-09-10 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210909_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='branch',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('CEO', 'CEO'), ('DOCTOR', 'DOCTOR'), ('ADMIN', 'ADMIN'), ('HR', 'HR'), ('MARKETING', 'MARKETING'), ('NURSE', 'NURSE')], max_length=255, null=True),
        ),
    ]
