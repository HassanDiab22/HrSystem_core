# Generated by Django 4.2.5 on 2023-10-09 11:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaves',
            old_name='date',
            new_name='end_date',
        ),
        migrations.RemoveField(
            model_name='leaves',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='leaves',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='leaves',
            name='leaving_days',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='leaves',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
