# Generated by Django 3.2.7 on 2021-09-13 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='best_staff',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='how_did_you_hear_abt_rabito',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='opinion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
