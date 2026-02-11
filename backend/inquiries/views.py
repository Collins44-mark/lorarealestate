from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Inquiry
from .serializers import InquiryCreateSerializer


class InquiryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Inquiry.objects.select_related("property").all()
    serializer_class = InquiryCreateSerializer
    permission_classes = (AllowAny,)
