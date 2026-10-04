"""Create a small, repeatable demo catalog for a fresh deployment."""

from datetime import date

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat


TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w780"
SAMPLE_MOVIES = (
    (
        "Ocean's Eight",
        "Debbie Ocean assembles a team for a daring heist at the Met Gala.",
        date(2018, 6, 8),
        111,
        f"{TMDB_POSTER_BASE}/MvYpKcwCR1mN6bN2K1H9PGBWk5m.jpg",
    ),
    (
        "Dune: Part Two",
        "Paul Atreides joins the Fremen and faces a choice that could shape the universe.",
        date(2024, 3, 1),
        167,
        f"{TMDB_POSTER_BASE}/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg",
    ),
    (
        "Hidden Figures",
        "Three brilliant NASA mathematicians help make a historic space mission possible.",
        date(2016, 12, 25),
        127,
        f"{TMDB_POSTER_BASE}/62HCnUTziyWcpZ1pXFcdjN04vW1.jpg",
    ),
    (
        "Interstellar",
        "Explorers travel through a wormhole in search of a future for humanity.",
        date(2014, 11, 5),
        169,
        f"{TMDB_POSTER_BASE}/gEU2QniE6E77NI6lCU6MvrIdMVD.jpg",
    ),
    (
        "The Dog Stars",
        "A pilot follows a mysterious radio signal toward hope after a devastating flu.",
        date(2026, 8, 28),
        118,
        "https://lumiere-a.akamaihd.net/v1/images/image_12_9e811276.jpeg?region=0%2C0%2C560%2C800",
    ),
    (
        "The Devil Wears Prada 2",
        "Miranda Priestly returns to Runway as the fashion magazine world changes around her.",
        date(2026, 5, 1),
        119,
        "https://lumiere-a.akamaihd.net/v1/images/tdwp2_teaser_poster_united_kingdom_6a72f273.jpeg?region=0%2C0%2C743%2C1100",
    ),
)


class Command(BaseCommand):
    help = "Create sample movies and seats without duplicating existing records"

    def handle(self, *args, **options):

        for title, description, release_date, duration, poster_url in SAMPLE_MOVIES:
            movie, created = Movie.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "release_date": release_date,
                    "duration": duration,
                    "poster_url": poster_url,
                },
            )
            if not created and not movie.poster_url:
                movie.poster_url = poster_url
                movie.save(update_fields=["poster_url"])

        for row in "ABC":
            for number in range(1, 6):
                Seat.objects.get_or_create(seat_number=f"{row}{number}")

        self.stdout.write(self.style.SUCCESS("Demo catalog is ready."))
