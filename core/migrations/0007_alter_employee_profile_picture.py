# Generated by Django 4.2.5 on 2023-10-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_employee_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile_picture',
            field=models.ImageField(blank=True, default='media/defaultProfielPicture.jpg', null=True, upload_to='media/'),
        ),
    ]