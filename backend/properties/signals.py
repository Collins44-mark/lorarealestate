from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Property
from .services import delete_property_media


@receiver(pre_delete, sender=Property)
def _property_pre_delete(sender, instance: Property, **kwargs):
    delete_property_media(instance)

