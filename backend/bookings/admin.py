from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "full_name", "email", "preferred_date", "preferred_time", "status", "created_at")
    list_filter = ("status", "preferred_date")
    search_fields = ("full_name", "email", "phone", "property__title")
    ordering = ("-created_at",)
    list_editable = ("status",)
    list_per_page = 25
    date_hierarchy = "preferred_date"
    fieldsets = (
        ("Visitor", {"fields": ("property", "full_name", "email", "phone", "message")}),
        ("Visit schedule", {"fields": ("preferred_date", "preferred_time")}),
        ("Status", {"fields": ("status",)}),
    )
