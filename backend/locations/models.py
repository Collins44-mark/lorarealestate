from django.db import models


class Location(models.Model):
    """
    A simple location model that matches the existing frontend style:
    - name: area/neighborhood (e.g. "Oyster Bay")
    - city: city name (e.g. "Dar es Salaam")
    """

    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120, default="Dar es Salaam")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "city")
        ordering = ("city", "name")

    def __str__(self) -> str:
        return f"{self.name}, {self.city}"
