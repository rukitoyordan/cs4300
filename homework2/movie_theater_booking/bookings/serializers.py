from rest_framework import serializers
from .models import Movie, Seat, Booking


class MovieSerializer(serializers.ModelSerializer):
    """Convert Movie objects to and from API data."""

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]

class SeatSerializer(serializers.ModelSerializer):
    """Convert Seat objects to API data."""

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]
        read_only_fields = ["id", "is_booked"]