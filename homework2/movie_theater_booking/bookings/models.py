# Models for booking app
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

# Movie Model: title, description, release date, duration.
class Movie(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(
    help_text="Duration (minutes)",
    # PositiveIntegerField permits zero, so require at least one minute.(https://docs.djangoproject.com/en/6.1/ref/validators/)
    validators=[MinValueValidator(1)],)

    def __str__(self):
        return self.title

# Seat Model: seat number; booking status depends on the movie.
class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.seat_number

# Booking Model: movie, seat, user, booking date.
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "seat"],
                name="unique_seat_per_movie",
            ),
        ]
    # https://docs.djangoproject.com/en/6.1/ref/models/constraints/