from rest_framework import serializers
from .models import Movie, Seat


class MovieSerializer(serializers.ModelSerializer):
    """Convert Movie objects to and from API data."""

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]


class SeatSerializer(serializers.ModelSerializer):
    """Show whether a seat is booked for the requested movie."""

    is_booked = serializers.BooleanField(source="booked_for_movie", read_only=True)

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]
