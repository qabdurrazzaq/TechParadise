# Generated by Django 3.2 on 2021-05-04 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_rename_quarters_quarter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quarter',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.companydetail'),
        ),
    ]
