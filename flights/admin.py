from django.contrib import admin
from flights.models import Flight, Seat, Reservation


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'number',
        'departure_time',
        'arrival_time',
        'duration',
        'origin',
        'destination',
        'status',
    ]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['number', 'is_available']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'flight', 'seat']
