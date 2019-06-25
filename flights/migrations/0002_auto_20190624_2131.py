# Generated by Django 2.2.2 on 2019-06-24 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='flight',
            name='duration',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AddField(
            model_name='reservation',
            name='flight',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.Flight'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.Seat'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]