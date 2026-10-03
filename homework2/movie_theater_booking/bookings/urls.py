from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "bookings"

router = DefaultRouter()
router.register("movies", views.MovieViewSet, basename="movie")
router.register("seats", views.SeatViewSet, basename="seat")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.movie_list, name="movie_list"),
    path(
        "movies/<int:movie_id>/seats/",
        views.seat_booking,
        name="seat_booking",
    ),
    path("bookings/history/", views.booking_history, name="booking_history"),
]