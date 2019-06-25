from unittest import TestCase
from autofixture import AutoFixture
from faker import Faker
from django.contrib.auth.models import User
from autofixture import AutoFixture
from datetime import timedelta
from django.utils import timezone

from flights.models import Flight, Seat, Reservation


class FlightsModelsTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.flight_fixture = AutoFixture(Flight)

    def test_can_create_flight(self):
        flight = self.flight_fixture.create(1)[0]
        self.assertIsNotNone(flight)
        self.assertEqual(flight.number, str(flight))

    def test_can_create_seat(self):
        flight = self.flight_fixture.create(1)[0]
        seat = AutoFixture(Seat, field_values={
            'flight': flight
        }).create(1)[0]
        self.assertIsNotNone(seat)
        self.assertEqual(seat.number, str(seat))

    def test_can_create_reservation(self):
        user = User(username='test2', password='test2')
        user.save()
        flight = self.flight_fixture.create(1)[0]
        seat = AutoFixture(Seat, field_values={
            'flight': flight
        }).create(1)[0]
        reservation = AutoFixture(Reservation, field_values={
            'flight': flight,
            'user': user,
            'seat': seat,
        }).create(1)[0]
        self.assertIsNotNone(reservation)

    def test_flight_duration(self):
        duration = 6
        departure_time = timezone.now()
        arrival_time = departure_time + timedelta(hours=duration)
        flight = Flight(
            number='KL0506',
            departure_time=departure_time,
            arrival_time=arrival_time,
            origin='EBB',
            destination='AMS',
            status='DELAYED'
        )
        self.assertEqual(flight.duration, duration)
