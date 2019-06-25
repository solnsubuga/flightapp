from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from faker import Faker
from autofixture import AutoFixture
from django.utils import timezone

from flights.models import Flight, Seat
from tests.base_test import BaseTestCase


class FlightsListAPIViewTestCase(BaseTestCase):
    '''Test Module for signing up a user'''
    # pylint: disable=E1101

    def setUp(self):
        super().setUp()
        self.flights_url = reverse('flights:list')
        self.flights_count = 5
        self.flights = AutoFixture(Flight).create(self.flights_count)

    def test_fetch_all_flights(self):
        response = self.get(self.flights_url)
        self.assertEqual(len(response.data), self.flights_count)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReserveFlightAPIViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.reserve_url = reverse('flights:reservations')
        self.flights = AutoFixture(Flight).create(2)
        self.flight = self.flights[0]
        self.seat = AutoFixture(Seat, field_values={
            'flight': self.flight
        }).create(1)[0]

    def reserve_flight(self):
        response = self.post(self.reserve_url, {
            'flight_number': self.flight.number,
            'seat_number': self.seat.number
        })
        return response

    def test_reserve_flight(self):
        response = self.reserve_flight()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['flight']['number'], self.flight.number)
        self.assertEqual(response.data['seat']['number'], self.seat.number)

    def test_get_reserved_flights(self):
        response = self.get(self.reserve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_flight_reservation_count_on_date(self):
        # reserve one flight
        self.reserve_flight()
        response = self.post(reverse('flights:reservations_count'), {
            'flight_number': self.flight.number,
            'date': timezone.now().date()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['reservations'] >= 0)
