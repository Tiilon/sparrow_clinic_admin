# Generated by Django 3.2.7 on 2021-09-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20210910_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('DOCTOR', 'DOCTOR'), ('CEO', 'CEO'), ('NURSE', 'NURSE'), ('MARKETING', 'MARKETING'), ('ADMIN', 'ADMIN'), ('HR', 'HR')], max_length=255, null=True),
        ),
    ]
