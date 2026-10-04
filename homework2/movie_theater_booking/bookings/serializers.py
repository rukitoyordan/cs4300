from rest_framework import serializers
from .models import Booking, Movie, Seat
from .services import SeatUnavailable, create_booking


class MovieSerializer(serializers.ModelSerializer):
    """Convert Movie objects to and from API data."""

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration", "poster_url"]


class SeatSerializer(serializers.ModelSerializer):
    """Show whether a seat is booked for the requested movie."""

    is_booked = serializers.BooleanField(source="booked_for_movie", read_only=True)

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "is_booked"]


class BookingSerializer(serializers.ModelSerializer):
    """Create a booking for the signed-in user and show its details."""

    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "booking_date"]
        read_only_fields = ["id", "user", "booking_date"]

    def validate(self, attrs):
        if Booking.objects.filter(movie=attrs["movie"], seat=attrs["seat"]).exists():
            raise serializers.ValidationError(
                {"seat": "This seat is already booked for this movie."}
            )
        return attrs

    def create(self, validated_data):
        try:
            return create_booking(
                movie=validated_data["movie"],
                seat=validated_data["seat"],
                user=self.context["request"].user,
            )
        except SeatUnavailable as error:
            raise serializers.ValidationError({"seat": str(error)}) from error
