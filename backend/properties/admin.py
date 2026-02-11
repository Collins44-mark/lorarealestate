from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Property, PropertyImage
from .services import upload_property_media


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0
    fields = ("preview", "url", "sort_order")
    readonly_fields = ("preview",)

    def preview(self, obj: PropertyImage):
        if not obj.url:
            return "-"
        return format_html(
            '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:8px;" />',
            obj.url,
        )


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PropertyAdminForm(forms.ModelForm):
    main_image_upload = forms.ImageField(required=False, help_text="Upload main image (jpg/jpeg/png/webp).")
    gallery_uploads = forms.FileField(
        required=False,
        widget=MultiFileInput(attrs={"multiple": True}),
        help_text="Upload multiple gallery images (jpg/jpeg/png/webp).",
    )
    video_upload = forms.FileField(required=False, help_text="Upload video (mp4).")

    class Meta:
        model = Property
        fields = "__all__"


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    inlines = (PropertyImageInline,)

    list_display = ("thumbnail", "title", "listing_type", "property_type", "price", "currency", "location", "featured", "published", "created_at")
    list_filter = ("listing_type", "property_type", "featured", "published", "location__city")
    search_fields = ("title", "location__name", "location__city")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("Listing", {"fields": ("property_type", "listing_type", "price", "currency", "location")}),
        ("Details", {"fields": ("bedrooms", "bathrooms", "area_size")}),
        ("Visibility", {"fields": ("featured", "published")}),
        ("Contact", {"fields": ("contact_phone", "contact_whatsapp")}),
        ("Media (Cloudinary)", {"fields": ("main_image", "video_url", "main_image_upload", "gallery_uploads", "video_upload")}),
    )

    readonly_fields = ("main_image", "video_url")

    def thumbnail(self, obj: Property):
        if not obj.main_image:
            return "-"
        return format_html(
            '<img src="{}" style="width:56px;height:56px;object-fit:cover;border-radius:12px;" />',
            obj.main_image,
        )

    def save_model(self, request, obj: Property, form: PropertyAdminForm, change: bool):
        super().save_model(request, obj, form, change)

        main_image_file = form.cleaned_data.get("main_image_upload")
        video_file = form.cleaned_data.get("video_upload")
        gallery_files = request.FILES.getlist("gallery_uploads") if request.FILES else None

        # Only replace gallery if field was present in POST (prevents clearing on edit)
        if "gallery_uploads" not in request.FILES and "gallery_uploads" not in request.POST:
            gallery_files = None

        upload_property_media(
            obj,
            main_image_file=main_image_file,
            gallery_files=gallery_files,
            video_file=video_file,
        )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "sort_order", "url")
