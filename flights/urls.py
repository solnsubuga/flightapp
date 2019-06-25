from django.urls import path

from flights import views

app_name = 'flights'

urlpatterns = [
    path('', views.FlightsListAPIView.as_view(), name='list'),
    path('reservations', views.ReserveFlightAPIView.as_view(), name='reservations'),
    path('reservations/count', views.QueryReservationAPIView.as_view(),
         name='reservations_count'),
]
