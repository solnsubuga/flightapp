# Generated by Django 2.2.2 on 2019-06-19 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='passport_photo',
            field=models.ImageField(blank=True, upload_to='flights'),
        ),
    ]
