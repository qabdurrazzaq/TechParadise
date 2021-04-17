# Generated by Django 3.2 on 2021-04-13 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0004_applicantdetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantdetails',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='applicantdetails',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
