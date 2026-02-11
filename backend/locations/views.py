from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (AllowAny,)
