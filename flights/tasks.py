# pylint: disable=E1101
from datetime import timedelta

from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

import traceback

logger = get_task_logger(__name__)

SUBJECT = 'FlightApp Travel Reminder'

EMAIL_BODY = '''
Hi {username}, 

We would like to remind that your flight({flight_number}) to {destination} will depart from {origin} 
at {departure_time}.

Regards,
FlightApp team.
'''


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="travel_reminder",
    max_retries=5,
    ignore_result=False
)
def remind_traveler():
    from flights.models import Reservation
    current_date = timezone.now().today()
    upper_bound = current_date + timedelta(days=2)
    reservations = Reservation.objects.filter(
        flight__departure_time__date__gt=current_date,
        flight__departure_time__date__lt=upper_bound,
        is_notified=False
    ).all()

    for reservation in reservations:
        email_kwargs = {
            'username': reservation.user.username,
            'flight_number': reservation.flight.number,
            'destination': reservation.flight.destination,
            'origin': reservation.flight.origin,
            'departure_time': reservation.flight.departure_time
        }
        body = EMAIL_BODY.format(**email_kwargs)
        send_mail(subject=SUBJECT, message=body, from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[reservation.user.email])
        reservation.is_notified = True
        reservation.save()
        logger.info('Successfully sent mail to {email}'.format(
            email=reservation.user.email))
