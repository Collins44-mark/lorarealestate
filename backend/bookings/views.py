from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Booking
from .serializers import BookingAdminSerializer, BookingCreateSerializer


class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.select_related("property").all()
    filterset_fields = ("status", "property")
    search_fields = ("full_name", "email", "phone", "property__title")
    ordering_fields = ("created_at", "preferred_date", "status")
    ordering = ("-created_at",)

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "list":
            return BookingAdminSerializer
        return BookingCreateSerializer
