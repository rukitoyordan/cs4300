from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Convert Movie objects to and from API data."""

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]