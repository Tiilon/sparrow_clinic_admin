# Generated by Django 3.2.7 on 2021-09-10 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_branch_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='code',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
