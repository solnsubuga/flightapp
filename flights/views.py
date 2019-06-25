# pylint: disable=E1101
from flights.serializers import FlightSerializer, FlightReservationSerializer, QueryReservationSerializer
from flights.models import Flight, Reservation
from rest_framework import generics
from rest_framework import exceptions
from rest_framework.views import APIView, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class FlightsListAPIView(generics.ListAPIView):
    '''List all flights'''
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()


class ReserveFlightAPIView(APIView):
    ''' Flight reservation view'''
    serializer_class = FlightReservationSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Reservation.objects.all()

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={201: serializer_class, 400: 'Bad Request'})
    def post(self, request):
        '''Make a flight reservation '''
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        ''' Get all your flight reservation '''
        reservations = Reservation.objects.filter(user=request.user).all()
        serializer = self.serializer_class(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QueryReservationAPIView(APIView):
    '''Query reservation API '''
    serializer_class = QueryReservationSerializer
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_body=serializer_class,
        responses={200: 'Ok', 400: 'Bad Request'}
    )
    def post(self, request):
        '''Queries reservations for a flight on a given day'''
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        flight_number = request.data.get('flight_number')
        date = request.data.get('date')
        reservations_count = Reservation.objects.filter(
            flight__number=flight_number, created__date=date).count()
        return Response({
            'reservations': reservations_count
        })


class CheckFlightStatusAPIView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: 'Ok', 404: 'Flight not found'}
    )
    def get(self, request, flight_number):
        flight = Flight.objects.filter(number=flight_number).first()
        if not flight:
            raise exceptions.NotFound(
                'Flight with number {flight_number} is not found'.format(flight_number=flight_number))
        return Response({
            'status': flight.status,
            'info': {
                'flight_number': flight.number,
                'origin': flight.origin,
                'destination': flight.destination,
                'departure_time': flight.departure_time,
                'arrival_time': flight.arrival_time
            }
        }, status=status.HTTP_200_OK)
