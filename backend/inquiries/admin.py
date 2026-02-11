from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "full_name", "email", "created_at")
    search_fields = ("full_name", "email", "phone", "message", "property__title")
    ordering = ("-created_at",)
