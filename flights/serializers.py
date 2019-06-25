# pylint: disable=E1101
from rest_framework import serializers
from django.contrib.auth.models import User

from flights.models import Flight, Seat, Reservation
from authentication.models import Profile


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['number']


class FlightSerializer(serializers.ModelSerializer):
    available_seats = SeatSerializer(many=True)

    class Meta:
        model = Flight
        fields = [
            'id',
            'number',
            'departure_time',
            'arrival_time',
            'origin',
            'destination',
            'status',
            'duration',
            'available_seats',
        ]


class ReservedFlight(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'number',
            'departure_time',
            'arrival_time',
            'origin',
            'destination',
            'duration',
        ]


class PassengerProfile(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['passport_number', 'passport_photo']


class PassengerSerializer(serializers.ModelSerializer):
    profile = PassengerProfile(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile']


class FlightReservationSerializer(serializers.ModelSerializer):
    flight_number = serializers.CharField(required=True, write_only=True)
    seat_number = serializers.CharField(required=True, write_only=True)
    flight = ReservedFlight(read_only=True)
    seat = SeatSerializer(read_only=True)
    user = PassengerSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['flight_number', 'seat_number',
                  'flight', 'seat', 'user', 'created']

    def get_flight(self, flight_number):
        flight = Flight.objects.filter(number=flight_number).first()
        return flight

    def get_seat(self, seat_number):
        return Seat.objects.filter(number=seat_number).first()

    def validate_flight_number(self, flight_number):
        flight = self.get_flight(flight_number)
        if not flight:
            raise serializers.ValidationError(
                'Flight with number: {flight_number} does not exist'.format(flight_number=flight_number))
        return flight_number

    def validate_seat_number(self, seat_number):
        seat = self.get_seat(seat_number)
        if not seat:
            raise serializers.ValidationError(
                'Seat with number: {seat_number} does not exist'.format(seat_number=seat_number))
        elif not seat.is_available:
            raise serializers.ValidationError(
                'Seat with number: {seat_number} is not available'.format(seat_number=seat_number))
        return seat_number

    def create(self, validated_data):
        flight_number = validated_data.get('flight_number')
        seat_number = validated_data.get('seat_number')
        user = validated_data.get('user')
        seat = self.get_seat(seat_number)
        seat.is_available = False
        seat.save()

        reservation = Reservation(
            user=user,
            flight=self.get_flight(flight_number),
            seat=seat
        )
        reservation.save()
        reservation.refresh_from_db()
        return {
            'user': user,
            'flight': reservation.flight,
            'seat': reservation.seat,
        }


class QueryReservationSerializer(serializers.Serializer):
    flight_number = serializers.CharField()
    date = serializers.DateField()

    def validate_flight_number(self, flight_number):
        flight = Flight.objects.filter(number=flight_number).first()
        if not flight:
            raise serializers.ValidationError(
                'Flight with number: {flight_number} does not exist'.format(
                    flight_number=flight_number))
        return flight_number
