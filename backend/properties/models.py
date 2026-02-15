from django.core.validators import MinValueValidator
from django.db import models


class Property(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        HOUSE = "house", "House"
        LAND = "land", "Land"
        COMMERCIAL = "commercial", "Commercial"

    class ListingType(models.TextChoices):
        SALE = "sale", "For Sale"
        RENT = "rent", "For Rent"

    class Availability(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        BOOKED = "booked", "Booked"

    title = models.CharField(max_length=255)
    description = models.TextField()

    property_type = models.CharField(max_length=20, choices=PropertyType.choices)
    listing_type = models.CharField(max_length=10, choices=ListingType.choices)

    price = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=12, default="TZS")

    location = models.ForeignKey("locations.Location", on_delete=models.PROTECT, related_name="properties")

    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    area_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    availability = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE,
    )

    # Media URLs only (stored from Cloudinary secure_url)
    main_image = models.URLField(max_length=1000, blank=True)
    main_image_public_id = models.CharField(max_length=255, blank=True)

    video_url = models.URLField(max_length=1000, blank=True)
    video_public_id = models.CharField(max_length=255, blank=True)

    contact_phone = models.CharField(max_length=40, blank=True)
    contact_whatsapp = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title

    @property
    def gallery_urls(self) -> list[str]:
        return [img.url for img in self.gallery_images.filter(visible=True).order_by("sort_order", "id")]


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="gallery_images")
    url = models.URLField(max_length=1000)
    public_id = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self) -> str:
        return f"Image for {self.property_id}"
