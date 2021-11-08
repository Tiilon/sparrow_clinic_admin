# Generated by Django 3.2.6 on 2021-09-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('DOCTOR', 'DOCTOR'), ('NURSE', 'NURSE'), ('MARKETING', 'MARKETING'), ('HR', 'HR'), ('ADMIN', 'ADMIN'), ('CEO', 'CEO')], max_length=255, null=True),
        ),
        migrations.AlterModelTable(
            name='schedule',
            table='schedule',
        ),
    ]
