from django.contrib import admin
from .models import Booking, Movie, Seat


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration")
    search_fields = ("title",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number",)
    search_fields = ("seat_number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("movie", "seat", "user", "booking_date")
    list_select_related = ("movie", "seat", "user")
