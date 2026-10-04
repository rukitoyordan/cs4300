"""Create a small, repeatable demo catalog for a fresh deployment."""

from datetime import date

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat


class Command(BaseCommand):
    help = "Create a demo movie and seats if they do not already exist"

    def handle(self, *args, **options):
        if not Movie.objects.exists():
            Movie.objects.create(
                title="Demo Movie",
                description="A sample screening for trying the booking app.",
                release_date=date(2026, 1, 1),
                duration=90,
            )
        for row in "ABC":
            for number in range(1, 6):
                Seat.objects.get_or_create(seat_number=f"{row}{number}")
        self.stdout.write(self.style.SUCCESS("Demo catalog is ready."))
