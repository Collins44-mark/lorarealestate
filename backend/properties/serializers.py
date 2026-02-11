from rest_framework import serializers

from locations.models import Location
from locations.serializers import LocationSerializer

from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ("id", "url", "sort_order")


class PropertyListSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    main_image = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "listing_type",
            "property_type",
            "price",
            "currency",
            "location",
            "bedrooms",
            "bathrooms",
            "area_size",
            "featured",
            "published",
            "main_image",
            "video_url",
            "created_at",
            "updated_at",
        )


class PropertyDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source="location", queryset=Location.objects.all(), write_only=True
    )
    gallery_images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "description",
            "property_type",
            "listing_type",
            "price",
            "currency",
            "location",
            "location_id",
            "bedrooms",
            "bathrooms",
            "area_size",
            "featured",
            "published",
            "main_image",
            "video_url",
            "gallery_images",
            "contact_phone",
            "contact_whatsapp",
            "created_at",
            "updated_at",
        )


class PropertyWriteSerializer(serializers.ModelSerializer):
    """
    Admin write serializer.
    Media is uploaded to Cloudinary via device file inputs:
    - main_image_file: single image
    - gallery_files: multiple images
    - video_file: mp4 video

    Only secure URLs (and Cloudinary public_id for cleanup) are stored.
    """

    location_id = serializers.PrimaryKeyRelatedField(source="location", queryset=Location.objects.all())
    main_image_file = serializers.ImageField(write_only=True, required=False, allow_null=True)
    gallery_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False, allow_empty=True
    )
    video_file = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "description",
            "property_type",
            "listing_type",
            "price",
            "currency",
            "location_id",
            "bedrooms",
            "bathrooms",
            "area_size",
            "featured",
            "published",
            "contact_phone",
            "contact_whatsapp",
            "main_image_file",
            "gallery_files",
            "video_file",
        )

    def validate_video_file(self, f):
        if f is None:
            return f
        name = (getattr(f, "name", "") or "").lower()
        if not name.endswith(".mp4"):
            raise serializers.ValidationError("Video must be an mp4 file.")
        return f

    def create(self, validated_data):
        from .services import upload_property_media

        main_image_file = validated_data.pop("main_image_file", None)
        gallery_files = validated_data.pop("gallery_files", [])
        video_file = validated_data.pop("video_file", None)

        prop = Property.objects.create(**validated_data)
        upload_property_media(prop, main_image_file=main_image_file, gallery_files=gallery_files, video_file=video_file)
        return prop

    def update(self, instance, validated_data):
        from .services import upload_property_media

        main_image_file = validated_data.pop("main_image_file", None)
        gallery_files = validated_data.pop("gallery_files", None)
        video_file = validated_data.pop("video_file", None)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()

        upload_property_media(instance, main_image_file=main_image_file, gallery_files=gallery_files, video_file=video_file)
        return instance

