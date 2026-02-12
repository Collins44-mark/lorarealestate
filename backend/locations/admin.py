from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "properties_count", "created_at")
    search_fields = ("name", "city")
    list_filter = ("city",)
    ordering = ("city", "name")
    list_per_page = 25

    def properties_count(self, obj):
        return obj.properties.count()

    properties_count.short_description = "Properties"
