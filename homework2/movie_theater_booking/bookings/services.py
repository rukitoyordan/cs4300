"""Shared booking operation for the API and HTML page."""
from django.db import IntegrityError, transaction
from .models import Booking


class SeatUnavailable(Exception):
    """The requested seat already has a booking for this movie."""


def create_booking(*, movie, seat, user):
    """Reserve a seat, relying on the database constraint to handle races."""
    try:
        with transaction.atomic():
            return Booking.objects.create(movie=movie, seat=seat, user=user)
    except IntegrityError as error:
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            raise SeatUnavailable("This seat is already booked for this movie.") from error
        raise
