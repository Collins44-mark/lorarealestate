from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "full_name", "email", "phone", "created_at")
    list_filter = ("created_at",)
    search_fields = ("full_name", "email", "phone", "message", "property__title")
    ordering = ("-created_at",)
    readonly_fields = ("property", "full_name", "email", "phone", "message", "created_at")

    def has_add_permission(self, request):
        return False  # Inquiries come from the contact form
