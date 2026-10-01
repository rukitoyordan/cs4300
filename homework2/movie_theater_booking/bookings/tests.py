from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from .models import Booking, Movie, Seat
from django.db import IntegrityError, transaction
from django.urls import reverse

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
        
    def test_movie_duration_must_be_positive(self):
        """Verify that movie validation rejects zero and negative durations."""
        for duration in (0, -1):
            with self.subTest(duration=duration):
                invalid_movie = Movie(
                    title="Invalid Duration",
                    description="This should not validate.",
                    release_date=date(2026, 1, 1),
                    duration=duration,
                )
                with self.assertRaises(ValidationError):
                    invalid_movie.full_clean()

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

class SeatModelTests(TestCase):
    """Test suite for the Seat model in the movie theater booking application."""
    def setUp(self):
        # Establish a baseline seat using the correct 'seat_number' field
        self.seat = Seat.objects.create(
            seat_number="A1"
        )
    
    def test_seat_is_available_by_default_and_has_a_display_name(self):
        """Check that new seats default to unbooked status and use their seat number for display."""
        # Reference the seat created in setUp rather than creating a new one
        self.assertFalse(self.seat.is_booked)
        self.assertEqual(str(self.seat), "A1")
        
    def test_seat_number_must_be_unique(self):
        """Verify that the database prevents duplicate seat numbers from being created."""
        # "A1" was already created in setUp, so creating it again should trigger the error
        with self.assertRaises(IntegrityError):
            Seat.objects.create(seat_number="A1")
        
    def test_seat_can_be_explicitly_booked(self):
        """Assert that a seat can be successfully created with a booked status."""
        # Use a different seat number ("A2") to avoid hitting the unique constraint from setUp
        booked_seat = Seat.objects.create(seat_number="A2", is_booked=True)
        self.assertTrue(booked_seat.is_booked)
        
    def test_seat_number_exceeds_max_length(self):
        """Validation rejects a seat number exceeding the 10 character limit."""
        # Pass the 11-character string directly into the correct seat_number field
        long_seat = Seat(seat_number="A" * 11)
        with self.assertRaises(ValidationError):
            long_seat.full_clean()
            
    def test_seat_missing_seat_number(self):
        """Omitting the required seat_number field triggers a validation error."""
        empty_seat = Seat(is_booked=False)
        with self.assertRaises(ValidationError):
            empty_seat.full_clean()

class BookingModelTests(TestCase):
    """Test suite for validating the relationships and constraints of the Booking model."""
    def setUp(self):
        """Create baseline data needed for foreign key relationships."""
        self.user = get_user_model().objects.create_user(
            username="booking_user", password="safe-test-password"
        )
        self.movie = Movie.objects.create(
            title="Booking Test Movie",
            description="A movie used to test bookings.",
            release_date=date(2026, 2, 1),
            duration=95,
        )
        self.seat = Seat.objects.create(seat_number="B2")
        self.booking = Booking.objects.create(
            movie=self.movie, seat=self.seat, user=self.user
        )

    def test_booking_connects_foreign_keys_and_auto_adds_timestamp(self):
        """Check if booking successfully links all external models and generates a date."""
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)
        self.assertEqual(self.booking.user, self.user)
        self.assertIsNotNone(self.booking.booking_date)
        self.assertLessEqual(self.booking.booking_date, timezone.now())

    def test_cascading_delete_removes_booking_if_seat_is_deleted(self):
        """Deleting a referenced Seat automatically deletes the attached Booking."""
        booking_id = self.booking.id
        self.seat.delete()
        self.assertFalse(Booking.objects.filter(pk=booking_id).exists())

    def test_booking_missing_movie(self):
        """Ensure that a booking cannot be created without a referenced movie."""
        incomplete_booking = Booking(seat=self.seat, user=self.user)
        with self.assertRaises(ValidationError):
            incomplete_booking.full_clean()

    def test_booking_missing_seat(self):
        """Verify that a booking cannot be created without a referenced seat."""
        incomplete_booking = Booking(movie=self.movie, user=self.user)
        with self.assertRaises(ValidationError):
            incomplete_booking.full_clean()
    
    def test_booking_missing_user(self):
        """Checks that users are present when booking is made."""
        incomplete_booking = Booking(movie=self.movie, seat=self.seat)

        with self.assertRaises(ValidationError):
            incomplete_booking.full_clean()
        
    def test_same_seat_cannot_be_booked_twice_for_same_movie(self):
        """Prevent another user from booking the same seat for this movie."""
        another_user = get_user_model().objects.create_user(
            username="another_booking_user",
            password="safe-test-password",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Booking.objects.create(
                    movie=self.movie,
                    seat=self.seat,
                    user=another_user,
                )

    def test_same_seat_can_be_booked_for_another_movie(self):
        """Allow a seat number to be reused for a different movie."""
        another_movie = Movie.objects.create(
            title="Another Movie",
            description="A different movie.",
            release_date=date(2026, 3, 1),
            duration=100,
        )

        Booking.objects.create(
            movie=another_movie,
            seat=self.seat,
            user=self.user,
        )

        self.assertEqual(Booking.objects.filter(seat=self.seat).count(), 2)

class SeatAvailabilityViewTests(TestCase):
    """Test movie-specific seat availability on the seat-booking page."""
    def setUp(self):
        """Create two movies and book A1 for only the first movie."""
        self.user = get_user_model().objects.create_user(
            username="seat_view_user",
            password="safe-test-password",
        )
        self.first_movie = Movie.objects.create(
            title="First Movie",
            description="The first movie.",
            release_date=date(2026, 1, 1),
            duration=90,
        )
        self.second_movie = Movie.objects.create(
            title="Second Movie",
            description="The second movie.",
            release_date=date(2026, 2, 1),
            duration=100,
        )
        self.seat_a1 = Seat.objects.create(seat_number="A1")
        self.seat_a2 = Seat.objects.create(seat_number="A2")

        Booking.objects.create(
            movie=self.first_movie,
            seat=self.seat_a1,
            user=self.user,
        )

    def test_booked_seat_is_hidden_for_its_movie(self):
        """Exclude A1 from the first movie while keeping A2 available."""
        response = self.client.get(
            reverse("bookings:seat_booking", args=[self.first_movie.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.seat_a1, response.context["seats"])
        self.assertIn(self.seat_a2, response.context["seats"])

    def test_same_seat_is_available_for_another_movie(self):
        """Show A1 for the second movie despite its first-movie booking."""
        response = self.client.get(
            reverse("bookings:seat_booking", args=[self.second_movie.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.seat_a1, response.context["seats"])
        self.assertIn(self.seat_a2, response.context["seats"])

class LoginViewTests(TestCase):
    """Test that users can reach and use the sign-in page."""
    def setUp(self):
        """Create a user whose credentials can be tested."""
        self.user = get_user_model().objects.create_user(
            username="login_user",
            password="safe-test-password",
        )

    def test_login_page_loads(self):
        """Show the sign-in form to a visitor."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in")

    def test_valid_login_redirects_to_movie_list(self):
        """Send a signed-in user to the movie list by default."""
        response = self.client.post(
            reverse("login"),
            {
                "username": "login_user",
                "password": "safe-test-password",
            },
        )
        self.assertRedirects(response, reverse("bookings:movie_list"))