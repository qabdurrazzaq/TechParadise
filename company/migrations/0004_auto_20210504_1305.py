# Generated by Django 3.2 on 2021-05-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_quarters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quarters',
            name='headquarter',
        ),
        migrations.AddField(
            model_name='companydetail',
            name='headquarter',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]