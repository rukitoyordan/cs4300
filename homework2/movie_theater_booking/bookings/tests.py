from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from .models import Booking, Movie, Seat

class MovieModelTests(TestCase):
    """Test suite for validating the data integrity and core behaviors of the Movie model."""
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            description="A movie used by the model tests.",
            release_date=date(2026, 1, 1),
            duration=120,
        )

    def test_movie_creation(self):
        """Check that the Movie model accurately saves all provided attributes to the database."""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.description, "A movie used by the model tests.")
        self.assertEqual(self.movie.release_date, date(2026, 1, 1))
        self.assertEqual(self.movie.duration, 120)
        
    def test_movie_stores_its_fields_and_uses_title_as_display_name(self):
        """Check that the Movie model accurately stores its fields and that the model's string representation returns the title for display purposes."""
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.duration, 120)
        self.assertEqual(str(self.movie), "Test Movie")
        self.assertEqual(self.movie.description, "A movie used by the model tests.")
        
    def test_movie_duration_must_be_non_negative(self):
        """Ensure that the Movie model validation catches and rejects negative duration values."""
        invalid_movie = Movie(
            title="Invalid Duration",
            description="This should not validate.",
            release_date=date(2026, 1, 1),
            duration=-1,
        )
        with self.assertRaises(ValidationError):
            invalid_movie.full_clean()
            
    def test_movie_duration_can_be_zero(self):
        """Analyze a movie duration of exactly 0 minutes and if it is valid."""
        zero_duration_movie = Movie.objects.create(
            title="Short Film",
            description="A movie with no runtime.",
            release_date=date(2026, 1, 1),
            duration=0,
        )
        self.assertEqual(zero_duration_movie.duration, 0)

    def test_movie_missing_required_fields(self):
        """Ensure that omitting a required field like release_date triggers a validation error."""
        incomplete_movie = Movie(
            title="No Release Date",
            description="Missing date.",
            # release_date omitted
            duration=120,
        )
        with self.assertRaises(ValidationError):
            incomplete_movie.full_clean()     

    def test_movie_title_exceeds_max_length(self):
        """Reject a title exceeding the maximum character limit."""
        long_title_movie = Movie(
            title="A" * 501,  # Based on max_length of 500
            description="This title is too long.",
            release_date=date(2026, 1, 1),
            duration=120,
        )
        with self.assertRaises(ValidationError):
            long_title_movie.full_clean()

