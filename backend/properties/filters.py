import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    listing_type = django_filters.CharFilter(field_name="listing_type")
    featured = django_filters.BooleanFilter(field_name="featured")
    property_type = django_filters.CharFilter(field_name="property_type")
    location = django_filters.CharFilter(method="filter_location")
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ("listing_type", "featured", "property_type", "location", "min_price", "max_price")

    def filter_location(self, qs, name, value):
        v = (value or "").strip()
        if not v:
            return qs
        return qs.filter(location__city__icontains=v) | qs.filter(location__name__icontains=v)

