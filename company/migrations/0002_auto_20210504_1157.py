# Generated by Django 3.2 on 2021-05-04 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companydetail',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='companydetail',
            name='github_username',
        ),
        migrations.RemoveField(
            model_name='companydetail',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='companydetail',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='companydetail',
            name='qualification',
        ),
    ]
