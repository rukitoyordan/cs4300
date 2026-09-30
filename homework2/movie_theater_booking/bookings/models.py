# Models for booking app
from django.db import models
from django.conf import settings

# Movie Model: title, description, release date, duration.
class Movie(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration (Mins)")

    def __str__(self):
        return self.title

# Seat Model: seat number, booking status.
class Seat(models.Model):
    seat_number = models.CharField(max_length=10, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number

# Booking Model: movie, seat, user, booking date.
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)