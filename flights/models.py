from django.db import models


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
    duration = models.DurationField()
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    status = models.CharField(choices=STATUSES, max_length=100)


class Seat(models.Model):
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='seats')
    number = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)


class Ticket(models.Model):
    TICKET_CLASSES = (
        ('ECONOMY', 'ECONOMY'),
        ('BUSINESS', 'BUSINESS'),
        ('FIRST', 'FIRST'),
    )
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    ticket_class = models.CharField(max_length=100, choices=TICKET_CLASSES)
