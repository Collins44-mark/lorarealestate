from rest_framework import serializers

from .models import Inquiry


class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ("id", "property", "full_name", "email", "phone", "message", "created_at")
        read_only_fields = ("created_at",)

