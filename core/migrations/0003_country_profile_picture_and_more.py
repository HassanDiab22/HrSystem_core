# Generated by Django 4.2.5 on 2023-10-12 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_date_leaves_end_date_remove_leaves_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='profile_picture',
            field=models.ImageField(blank=True, default='uploads/defaultProfielPicture.jpg', null=True, upload_to='core/uploads/'),
        ),
        migrations.AddField(
            model_name='country',
            name='profile_picture_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='role',
            name='profile_picture',
            field=models.ImageField(blank=True, default='uploads/defaultProfielPicture.jpg', null=True, upload_to='core/uploads/'),
        ),
        migrations.AddField(
            model_name='role',
            name='profile_picture_title',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]