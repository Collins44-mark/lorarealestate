from rest_framework import serializers

from .models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "property",
            "full_name",
            "email",
            "phone",
            "preferred_date",
            "preferred_time",
            "message",
        )


class BookingAdminSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "property",
            "property_title",
            "full_name",
            "email",
            "phone",
            "preferred_date",
            "preferred_time",
            "message",
            "status",
            "created_at",
        )

