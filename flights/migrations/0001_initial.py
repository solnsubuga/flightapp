# Generated by Django 2.2.2 on 2019-06-23 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('origin', models.CharField(max_length=150)),
                ('destination', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('SCHEDULED', 'SCHEDULED'), ('DELAYED', 'DELAYED'), ('ON_TIME', 'ON TIME'), ('ARRIVED', 'ARRIVED'), ('LATE', 'LATE')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('is_available', models.BooleanField(default=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='flights.Flight')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_class', models.CharField(choices=[('ECONOMY', 'ECONOMY'), ('BUSINESS', 'BUSINESS'), ('FIRST', 'FIRST')], max_length=100)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.Flight')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.Seat')),
            ],
        ),
    ]
