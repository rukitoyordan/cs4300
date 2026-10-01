from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path(
        "movies/<int:movie_id>/seats/",
        views.seat_booking,
        name="seat_booking",
    ),
    path("bookings/history/", views.booking_history, name="booking_history"),
]