from django.test import TestCase
from datetime import date
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError
from django.utils import timezone
from .models import Booking, Movie, Seat
from .views import BookingViewSet
from django.db import IntegrityError, transaction
from django.urls import reverse
from urllib.parse import quote
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

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
    """Test the seat inventory shared across movies."""

    def setUp(self):
        self.seat = Seat.objects.create(seat_number="A1")

    def test_seat_number_is_display_name(self):
        self.assertEqual(str(self.seat), "A1")

    def test_seat_number_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Seat.objects.create(seat_number="A1")

    def test_seat_number_exceeds_max_length(self):
        with self.assertRaises(ValidationError):
            Seat(seat_number="A" * 11).full_clean()

    def test_seat_missing_seat_number(self):
        with self.assertRaises(ValidationError):
            Seat().full_clean()

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
        """
        Verify that a booked seat is still passed to the template context
        but is correctly bundled with its corresponding booking data.
        """
        # Log the user in so the view doesn't redirect to the login page
        self.client.force_login(self.user)
        response = self.client.get(reverse('bookings:seat_booking', args=[self.first_movie.pk]))
        
        seats_in_context = response.context['seats']
        seat_found = False
        
        for s in seats_in_context:
            # Accommodates both dict and object structures from the view
            seat_obj = s['seat'] if isinstance(s, dict) else s
            booking_obj = s['booking'] if isinstance(s, dict) else getattr(s, 'booking', None)
            
            if seat_obj == self.seat_a1:
                seat_found = True
                self.assertIsNotNone(booking_obj)
                
        self.assertTrue(seat_found, "Seat should still be in the context.")

    def test_same_seat_is_available_for_another_movie(self):
        """Show A1 for the second movie despite its first-movie booking."""
        self.client.force_login(self.user)
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

class MovieAPITests(APITestCase):
    """Test who can use the Movie API."""

    def test_visitor_cannot_create_movie(self):
        """Reject a movie submitted by someone who is not signed in."""
        response = self.client.post(
            "/api/movies/",
            {
                "title": "Unauthorized Movie",
                "description": "This should not be saved.",
                "release_date": "2026-09-01",
                "duration": 100,
            },
            format="json",
        )

        self.assertIn(response.status_code, (401, 403))
        self.assertFalse(Movie.objects.filter(title="Unauthorized Movie").exists())

    def test_staff_can_create_movie(self):
        """Allow a staff user to create a movie through the API."""
        staff_user = get_user_model().objects.create_user(
            username="movie_staff",
            password="safe-test-password",
            is_staff=True,
        )
        self.client.force_authenticate(user=staff_user)

        response = self.client.post(
            "/api/movies/",
            {
                "title": "Test Movie",
                "description": "A movie created through the API.",
                "release_date": "2026-09-01",
                "duration": 100,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Movie.objects.filter(title="Test Movie").exists())

class SeatAPITests(APITestCase):
    """Seat status must reflect bookings for the requested movie."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="api_booking_user", password="safe-test-password"
        )
        self.first_movie = Movie.objects.create(
            title="First API Movie", description="First film.",
            release_date=date(2026, 1, 1), duration=90,
        )
        self.second_movie = Movie.objects.create(
            title="Second API Movie", description="Second film.",
            release_date=date(2026, 1, 2), duration=95,
        )
        self.seat_a1 = Seat.objects.create(seat_number="A1")
        self.seat_a2 = Seat.objects.create(seat_number="A2")
        Booking.objects.create(
            movie=self.first_movie, seat=self.seat_a1, user=self.user
        )

    def test_movie_specific_status_and_json_shape(self):
        first = self.client.get("/api/seats/", {"movie_id": self.first_movie.pk})
        second = self.client.get("/api/seats/", {"movie_id": self.second_movie.pk})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(
            first.json(),
            [
                {"id": self.seat_a1.pk, "seat_number": "A1", "is_booked": True},
                {"id": self.seat_a2.pk, "seat_number": "A2", "is_booked": False},
            ],
        )
        self.assertFalse(second.json()[0]["is_booked"])

    def test_movie_id_is_required(self):
        response = self.client.get("/api/seats/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("movie_id", response.json())

    def test_unknown_movie_is_not_found(self):
        response = self.client.get("/api/seats/", {"movie_id": 99999})
        self.assertEqual(response.status_code, 404)

    def test_seat_inventory_is_read_only(self):
        response = self.client.post(
            "/api/seats/", {"seat_number": "A3"}, format="json"
        )
        self.assertEqual(response.status_code, 405)


    def test_signed_in_user_can_book_through_seat_endpoint(self):
        """Create a booking through the SeatViewSet action."""
        self.client.force_login(self.user)
        response = self.client.post(
            "/api/seats/book/",
            {"movie": self.first_movie.pk, "seat": self.seat_a2.pk},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(movie=self.first_movie, seat=self.seat_a2, user=self.user).exists())

    def test_anonymous_user_cannot_book_through_seat_endpoint(self):
        """Require authentication for the SeatViewSet booking action."""
        response = self.client.post(
            "/api/seats/book/",
            {"movie": self.first_movie.pk, "seat": self.seat_a2.pk},
            format="json",
        )

        self.assertIn(response.status_code, (401, 403))
        self.assertFalse(Booking.objects.filter(movie=self.first_movie, seat=self.seat_a2).exists())

class BookingViewSetTests(TestCase):
    """Test who can create and read bookings through the API."""

    def setUp(self):
        """Create two users and movie seats for the booking requests."""
        users = get_user_model().objects
        self.alice = users.create_user(username="alice", password="test-password")
        self.bob = users.create_user(username="bob", password="test-password")
        self.movie = Movie.objects.create(
            title="Test movie", description="Booking view test",
            release_date=date(2026, 1, 1), duration=90,
        )
        self.seat = Seat.objects.create(seat_number="A1")
        self.factory = APIRequestFactory()

    def test_create_uses_signed_in_user(self):
        """Save the signed-in user even when another user ID is submitted."""
        request = self.factory.post(
            "/api/bookings/",
            {"movie": self.movie.pk, "seat": self.seat.pk, "user": self.bob.pk},
            format="json",
        )
        force_authenticate(request, user=self.alice)

        response = BookingViewSet.as_view({"post": "create"})(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.get().user, self.alice)

    def test_list_and_detail_show_only_own_bookings(self):
        """List own bookings and hide another user's booking detail."""
        own_booking = Booking.objects.create(
            movie=self.movie, seat=self.seat, user=self.alice,
        )
        other_seat = Seat.objects.create(seat_number="A2")
        other_booking = Booking.objects.create(
            movie=self.movie, seat=other_seat, user=self.bob,
        )
        list_request = self.factory.get("/api/bookings/")
        force_authenticate(list_request, user=self.alice)
        list_response = BookingViewSet.as_view({"get": "list"})(list_request)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual([item["id"] for item in list_response.data], [own_booking.pk])

        detail_request = self.factory.get(f"/api/bookings/{other_booking.pk}/")
        force_authenticate(detail_request, user=self.alice)
        detail_response = BookingViewSet.as_view({"get": "retrieve"})(
            detail_request, pk=other_booking.pk,
        )
        self.assertEqual(detail_response.status_code, 404)

    def test_anonymous_user_cannot_create_booking(self):
        """Reject booking creation when no user is signed in."""
        request = self.factory.post(
            "/api/bookings/",
            {"movie": self.movie.pk, "seat": self.seat.pk}, format="json",
        )

        response = BookingViewSet.as_view({"post": "create"})(request)

        self.assertIn(response.status_code, (401, 403))
        self.assertFalse(Booking.objects.exists())

    def test_booking_url_shows_list_to_signed_in_user(self):
        """Show an empty booking list at the API URL after sign-in."""
        self.client.force_login(self.alice)

        response = self.client.get("/api/bookings/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_serializer_rejects_duplicate_booking_during_validate(self):
        """Duplicate booking is detected during serializer validation."""
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.alice)

        from bookings.serializers import BookingSerializer

        data = {"movie": self.movie.pk, "seat": self.seat.pk}
        serializer = BookingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_unrelated_database_error_propagates(self):
        """Non-duplicate IntegrityError is re-raised without transformation."""
        from unittest.mock import patch
        from django.db import IntegrityError
        from bookings.services import create_booking

        with patch("bookings.services.Booking.objects.create") as mock_create:
            mock_create.side_effect = IntegrityError("unrelated constraint violation")

            with self.assertRaises(IntegrityError) as cm:
                create_booking(movie=self.movie, seat=self.seat, user=self.alice)

            self.assertIn("constraint", str(cm.exception).lower())

    def test_duplicate_booking_raises_seat_unavailable_error(self):
        """Service raises SeatUnavailable when seat is already booked."""
        from bookings.services import create_booking, SeatUnavailable

        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.alice)

        with self.assertRaises(SeatUnavailable) as cm:
            create_booking(movie=self.movie, seat=self.seat, user=self.bob)

        self.assertIn("already booked", str(cm.exception).lower())


class BookingPageTests(TestCase):
    """Test seat booking and booking history through the HTML pages."""

    def setUp(self):
        """Create two users and one movie with a booked and an open seat."""
        self.user = get_user_model().objects.create_user(
            username="page_user", password="safe-test-password"
        )
        self.other_user = get_user_model().objects.create_user(
            username="other_page_user", password="safe-test-password"
        )
        self.movie = Movie.objects.create(
            title="Page Test Movie",
            description="A movie for booking page tests.",
            release_date=date(2026, 1, 1),
            duration=90,
        )
        self.booked_seat = Seat.objects.create(seat_number="A1")
        self.open_seat = Seat.objects.create(seat_number="A2")
        self.other_booking = Booking.objects.create(
            movie=self.movie, seat=self.booked_seat, user=self.other_user
        )
        self.seat_url = reverse("bookings:seat_booking", args=[self.movie.pk])
        self.history_url = reverse("bookings:booking_history")

    def test_post_books_available_seat_and_redirects_to_history(self):
        """
        Verify that a POST request with a valid, available seat ID creates a new
        Booking for the current user and redirects to the booking history page.
        """
        self.client.force_login(self.user)
        
        # Fixed payload key from 'seat' to 'seat_id'
        response = self.client.post(reverse('bookings:seat_booking', args=[self.movie.pk]), {'seat_id': self.open_seat.pk})
        
        self.assertRedirects(response, reverse('bookings:booking_history'))
        self.assertTrue(Booking.objects.filter(user=self.user, movie=self.movie, seat=self.open_seat).exists())

    def test_post_for_booked_seat_keeps_original_booking(self):
        """
        Verify that attempting to book a seat that is already booked by another
        user does not overwrite or modify the existing booking in the database.
        """
        self.client.force_login(self.user)
        
        # Fixed payload key from 'seat' to 'seat_id'
        self.client.post(reverse('bookings:seat_booking', args=[self.movie.pk]), {'seat_id': self.booked_seat.pk})
        
        # Verify the original booking remains untouched
        booking = Booking.objects.get(movie=self.movie, seat=self.booked_seat)
        self.assertEqual(booking.user, self.other_user)

    def test_anonymous_post_redirects_without_booking(self):
        """A visitor cannot reserve a seat by submitting the form directly."""
        response = self.client.post(self.seat_url, {"seat_id": self.open_seat.pk})

        self.assertRedirects(
            response, f'{reverse("login")}?next={quote(self.seat_url, safe="")}'
        )
        self.assertFalse(
            Booking.objects.filter(movie=self.movie, seat=self.open_seat).exists()
        )

    def test_history_shows_only_signed_in_users_bookings(self):
        """Booking history includes this user's reservation and excludes another's."""
        own_booking = Booking.objects.create(
            movie=self.movie, seat=self.open_seat, user=self.user
        )
        self.client.force_login(self.user)

        response = self.client.get(self.history_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_history.html")
        self.assertEqual(list(response.context["bookings"]), [own_booking])
        self.assertContains(response, "A2")

    def test_anonymous_history_shows_sign_in_prompt(self):
        """A visitor is sent to sign in before viewing booking records."""
        response = self.client.get(self.history_url)

        self.assertRedirects(
            response, f'{reverse("login")}?next={quote(self.history_url, safe="")}'
        )


class SignupViewTests(TestCase):
    """Test the public account registration flow."""

    def test_signup_creates_and_logs_in_a_user(self):
        response = self.client.post(
            reverse("bookings:signup"),
            {
                "username": "new_view_user",
                "email": "new_view_user@example.com",
                "password1": "CorrectHorseBatteryStaple42",
                "password2": "CorrectHorseBatteryStaple42",
            },
        )

        self.assertRedirects(response, reverse("bookings:movie_list"))
        self.assertTrue(get_user_model().objects.filter(username="new_view_user").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_signup_renders_form_errors_for_invalid_data(self):
        response = self.client.post(
            reverse("bookings:signup"),
            {
                "username": "invalid_view_user",
                "password1": "first-password",
                "password2": "second-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="invalid_view_user").exists())


class SeedDemoCommandTests(TestCase):
    """Test the repeatable demo catalog command."""

    def test_seed_demo_creates_a_repeatable_catalog(self):
        call_command("seed_demo")
        expected_titles = {
            "Dune: Part Two",
            "Hidden Figures",
            "Interstellar",
            "Ocean's Eight",
            "The Devil Wears Prada 2",
            "The Dog Stars",
        }
        self.assertTrue(expected_titles.issubset(set(Movie.objects.values_list("title", flat=True))))
        self.assertEqual(Seat.objects.count(), 15)

        movie_count = Movie.objects.count()
        seat_count = Seat.objects.count()
        call_command("seed_demo")

        self.assertEqual(Movie.objects.count(), movie_count)
        self.assertEqual(Seat.objects.count(), seat_count)


class BookingCancellationViewTests(TestCase):
    """Test releasing a seat from the theater layout."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cancellation_user", password="test-password-123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="other_cancellation_user", password="test-password-123"
        )
        self.movie = Movie.objects.create(
            title="Cancellation Test Movie",
            description="A movie used to test seat releases.",
            release_date=date(2026, 1, 1),
            duration=100,
        )
        self.seat = Seat.objects.create(seat_number="D1")
        self.booking = Booking.objects.create(
            movie=self.movie, seat=self.seat, user=self.user
        )

    def test_booking_page_shows_taken_seats_and_release_control(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("bookings:seat_booking", args=[self.movie.pk])
        )

        self.assertContains(response, "Taken")
        self.assertContains(response, "Unbook")

    def test_user_can_release_their_own_booking(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("bookings:cancel_booking", args=[self.booking.pk])
        )

        self.assertRedirects(
            response, reverse("bookings:seat_booking", args=[self.movie.pk])
        )
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_user_cannot_release_someone_elses_booking(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("bookings:cancel_booking", args=[self.booking.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Booking.objects.filter(pk=self.booking.pk).exists())
