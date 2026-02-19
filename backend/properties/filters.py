import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    listing_type = django_filters.CharFilter(field_name="listing_type")
    featured = django_filters.BooleanFilter(field_name="featured")
    property_type = django_filters.CharFilter(field_name="property_type")
    location = django_filters.CharFilter(method="filter_location")
    currency = django_filters.CharFilter(field_name="currency")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    availability = django_filters.CharFilter(method="filter_availability")

    def filter_availability(self, qs, name, value):
        v = (value or "").strip().lower()
        if v == "available":
            return qs.filter(availability="available")
        if v == "occupied":
            return qs.filter(availability__in=["occupied", "booked"])
        return qs

    class Meta:
        model = Property
        fields = ("listing_type", "featured", "property_type", "location", "currency", "min_price", "max_price", "availability")

    def filter_location(self, qs, name, value):
        v = (value or "").strip()
        if not v:
            return qs
        return qs.filter(location__city__icontains=v) | qs.filter(location__name__icontains=v)

