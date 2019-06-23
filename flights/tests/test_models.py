from unittest import TestCase
from autofixture import AutoFixture
from faker import Faker
from django.contrib.auth.models import User
from autofixture import AutoFixture

from flights.models import Flight, Seat, Ticket


class TestModelsTestCase(TestCase):
    def setUp(self):
        self.faker = Faker()
        self.flight_fixture = AutoFixture(Flight)
        self.seat_fixture = AutoFixture(Seat)
        self.ticket_fixture = AutoFixture(Ticket)

    def test_can_create_flight(self):
        flight = self.flight_fixture.create(1)
        self.assertIsNotNone(flight)

    def test_can_create_seat(self):
        flight = self.flight_fixture.create(1)
        seat = self.seat_fixture.create(1, field_values={
            'flight': flight
        })[0]
        self.assertIsNone(seat)

    def test_can_create_ticket(self):
        flight = self.flight_fixture.create(1)
        ticket = self.ticket_fixture.create(1, field_values={
            'flight': flight
        })[0]
        self.assertIsNone(ticket)
