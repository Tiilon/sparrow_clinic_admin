# Generated by Django 3.2.7 on 2021-09-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210910_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('DOCTOR', 'DOCTOR'), ('HR', 'HR'), ('NURSE', 'NURSE'), ('MARKETING', 'MARKETING'), ('ADMIN', 'ADMIN'), ('CEO', 'CEO')], max_length=255, null=True),
        ),
    ]
