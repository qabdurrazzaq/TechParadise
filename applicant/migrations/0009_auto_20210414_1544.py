# Generated by Django 3.2 on 2021-04-14 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0008_auto_20210413_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantdetail',
            name='about',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='applicantdetail',
            name='achievements',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='applicantdetail',
            name='first_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='applicantdetail',
            name='interest',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='applicantdetail',
            name='last_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='applicantdetail',
            name='qualification',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]