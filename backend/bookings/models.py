from django.db import models


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)

    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Booking #{self.id} ({self.status})"
