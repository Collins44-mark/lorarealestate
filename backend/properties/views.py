from rest_framework import viewsets

from accounts.permissions import IsAdminUserForUnsafeMethods

from .filters import PropertyFilter
from .models import Property
from .serializers import PropertyDetailSerializer, PropertyListSerializer, PropertyWriteSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    Public:
    - GET /api/properties/
    - GET /api/properties/{id}/

    Admin (JWT):
    - POST/PUT/PATCH/DELETE
    """

    filterset_class = PropertyFilter
    search_fields = ("title", "description", "location__name", "location__city")
    ordering_fields = ("created_at", "price", "featured")
    ordering = ("-created_at",)
    permission_classes = (IsAdminUserForUnsafeMethods,)

    def get_queryset(self):
        qs = Property.objects.select_related("location").prefetch_related("gallery_images")
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return qs.filter(published=True)
        return qs

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return PropertyWriteSerializer
        if self.action == "retrieve":
            return PropertyDetailSerializer
        return PropertyListSerializer
