from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "full_name", "preferred_date", "preferred_time", "status", "created_at")
    list_filter = ("status", "preferred_date")
    search_fields = ("full_name", "email", "phone", "property__title")
    ordering = ("-created_at",)
