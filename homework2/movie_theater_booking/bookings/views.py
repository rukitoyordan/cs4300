from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Booking, Movie, Seat


def movie_list(request):
    movies = Movie.objects.all().order_by("title")
    return render(request, "bookings/movie_list.html", {"movies": movies})


def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    booked_seat_ids = Booking.objects.filter(movie=movie).values_list(
        "seat_id", flat=True
    )
    seats = Seat.objects.exclude(pk__in=booked_seat_ids).order_by("seat_number")

    return render(
        request,
        "bookings/seat_booking.html",
        {"movie": movie, "seats": seats},
    )


def booking_history(request):
    if request.user.is_authenticated:
        bookings = (
            Booking.objects.filter(user=request.user)
            .select_related("movie", "seat")
            .order_by("-booking_date")
        )
    else:
        bookings = Booking.objects.none()

    return render(
        request,
        "bookings/booking_history.html",
        {
            "bookings": bookings,
            "is_authenticated": request.user.is_authenticated,
        },
    )
