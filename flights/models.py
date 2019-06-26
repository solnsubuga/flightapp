from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    STATUSES = (
        ('SCHEDULED', 'SCHEDULED'),
        ('DELAYED', 'DELAYED'),
        ('ON_TIME', 'ON TIME'),
        ('ARRIVED', 'ARRIVED'),
        ('LATE', 'LATE')
    )
    number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    status = models.CharField(choices=STATUSES, max_length=100)

    @property
    def duration(self):
        timespan = self.arrival_time - self.departure_time
        days, seconds = timespan.days, timespan.seconds
        return days * 24 + seconds // 3600  # return hours

    @property
    def available_seats(self):
        return self.seats.filter(is_available=True).all()

    def __str__(self):
        return self.number


class Seat(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='seats')
    number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.number


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_notified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
