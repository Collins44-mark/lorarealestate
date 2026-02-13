import re
from django import template

register = template.Library()


@register.filter
def phone_digits(value):
    """Extract digits only from phone string for WhatsApp links."""
    if not value:
        return ""
    return re.sub(r"\D", "", str(value))
