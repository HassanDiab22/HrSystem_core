# Generated by Django 4.2.5 on 2023-10-16 11:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_employee_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdate', models.DateField(default=datetime.date.today)),
                ('enddate', models.DateField(default=datetime.datetime(2023, 10, 23, 14, 47, 26, 560654))),
                ('total_hours', models.FloatField(default=0.0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('duration', models.FloatField(default=0)),
                ('timesheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.timesheet')),
            ],
        ),
    ]
