from __future__ import annotations

from typing import Iterable

import cloudinary
import cloudinary.uploader
from django.db import transaction

from .models import Property, PropertyImage

ALLOWED_IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def _cloudinary_configured() -> bool:
    config = cloudinary.config()
    return bool(config.cloud_name and config.api_key and config.api_secret)


def _validate_image_file(f) -> None:
    name = (getattr(f, "name", "") or "").lower()
    if not name.endswith(ALLOWED_IMAGE_EXTS):
        raise ValueError("Image must be jpg, jpeg, png, or webp.")


def _validate_video_file(f) -> None:
    name = (getattr(f, "name", "") or "").lower()
    if not name.endswith(".mp4"):
        raise ValueError("Video must be an mp4 file.")


def destroy_cloudinary_asset(public_id: str, resource_type: str) -> None:
    if not public_id:
        return
    try:
        cloudinary.uploader.destroy(public_id, resource_type=resource_type, invalidate=True)
    except Exception:
        # Avoid breaking deletes/updates if Cloudinary cleanup fails.
        pass


@transaction.atomic
def upload_property_media(
    prop: Property,
    *,
    main_image_file=None,
    gallery_files: Iterable | None = None,
    video_file=None,
    append_gallery: bool = False,
) -> None:
    """
    Upload media to Cloudinary and store ONLY secure URLs in DB.
    Also stores Cloudinary public_id for later deletion.

    - main_image_file: replaces existing main image if provided
    - gallery_files: if provided, replaces gallery (or appends when append_gallery=True)
    - video_file: replaces existing video if provided
    """

    if main_image_file:
        if not _cloudinary_configured():
            raise ValueError("Cloudinary not configured. Set CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME, API_KEY, API_SECRET.")
        _validate_image_file(main_image_file)
        destroy_cloudinary_asset(prop.main_image_public_id, "image")
        res = cloudinary.uploader.upload(main_image_file, resource_type="image", folder="lora/properties")
        prop.main_image = res.get("secure_url", "")
        prop.main_image_public_id = res.get("public_id", "")
        prop.save(update_fields=["main_image", "main_image_public_id", "updated_at"])

    if gallery_files is not None:
        if gallery_files and not _cloudinary_configured():
            raise ValueError("Cloudinary not configured. Set CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME, API_KEY, API_SECRET.")
        if not append_gallery:
            for img in prop.gallery_images.all():
                destroy_cloudinary_asset(img.public_id, "image")
            prop.gallery_images.all().delete()
        start_order = prop.gallery_images.count() if append_gallery else 0

        for i, f in enumerate(gallery_files):
            _validate_image_file(f)
            res = cloudinary.uploader.upload(f, resource_type="image", folder="lora/properties/gallery")
            PropertyImage.objects.create(
                property=prop,
                url=res.get("secure_url", ""),
                public_id=res.get("public_id", ""),
                sort_order=start_order + i,
            )

    if video_file:
        if not _cloudinary_configured():
            raise ValueError("Cloudinary not configured. Set CLOUDINARY_URL or CLOUDINARY_CLOUD_NAME, API_KEY, API_SECRET.")
        _validate_video_file(video_file)
        destroy_cloudinary_asset(prop.video_public_id, "video")
        res = cloudinary.uploader.upload(video_file, resource_type="video", folder="lora/properties/videos")
        prop.video_url = res.get("secure_url", "")
        prop.video_public_id = res.get("public_id", "")
        prop.save(update_fields=["video_url", "video_public_id", "updated_at"])


@transaction.atomic
def delete_property_media(prop: Property) -> None:
    """
    Called when a Property is deleted: destroy associated Cloudinary assets.
    """

    destroy_cloudinary_asset(prop.main_image_public_id, "image")
    destroy_cloudinary_asset(prop.video_public_id, "video")
    for img in prop.gallery_images.all():
        destroy_cloudinary_asset(img.public_id, "image")

