# Generated by Django 3.2.7 on 2021-09-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210910_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('DOCTOR', 'DOCTOR'), ('CEO', 'CEO'), ('NURSE', 'NURSE'), ('MARKETING', 'MARKETING'), ('HR', 'HR'), ('ADMIN', 'ADMIN')], max_length=255, null=True),
        ),
    ]
