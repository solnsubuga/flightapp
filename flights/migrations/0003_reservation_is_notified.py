# Generated by Django 2.2.2 on 2019-06-26 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_auto_20190624_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_notified',
            field=models.BooleanField(default=False),
        ),
    ]
