# Generated by Django 3.2 on 2021-04-13 11:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120)),
                ('last_name', models.CharField(max_length=120)),
                ('qualification', models.CharField(max_length=200)),
                ('achievements', models.CharField(max_length=200)),
                ('interest', models.CharField(max_length=200)),
                ('about', models.TextField(max_length=250)),
                ('timestamp', models.DateTimeField(verbose_name=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name=django.utils.timezone.now)),
            ],
        ),
    ]