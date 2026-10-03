from datetime import date

from behave import given, then, when
from django.contrib.auth import get_user_model
from django.urls import reverse

from bookings.models import Booking, Movie, Seat


@given("a movie has an available seat")
def movie_has_available_seat(context):
    """Create a movie and an unbooked seat for this scenario."""
    context.movie = Movie.objects.create(
        title="Example Movie",
        description="A movie for the booking scenario.",
        release_date=date(2026, 1, 1),
        duration=90,
    )
    context.seat = Seat.objects.create(seat_number="A1")


@given("I am signed in as a customer")
def signed_in_customer(context):
    """Log a customer into Django's test client."""
    context.user = get_user_model().objects.create_user(
        username="moviegoer", password="test-password-123"
    )
    context.test.client.force_login(context.user)


@when("I book that seat")
def book_seat(context):
    """Submit the same seat booking form as the HTML page."""
    context.response = context.test.client.post(
        reverse("bookings:seat_booking", args=[context.movie.pk]),
        {"seat_id": context.seat.pk},
    )


@then("I am redirected to my booking history")
def redirected_to_history(context):
    """Confirm the form completes with the expected redirect."""
    assert context.response.status_code == 302
    assert context.response["Location"] == reverse("bookings:booking_history")


@then("my booking history shows the movie and seat")
def history_shows_booking(context):
    """Confirm the reservation exists and appears on the history page."""
    assert Booking.objects.filter(
        movie=context.movie, seat=context.seat, user=context.user
    ).exists()
    response = context.test.client.get(reverse("bookings:booking_history"))
    context.test.assertContains(response, context.movie.title)
    context.test.assertContains(response, context.seat.seat_number)
