from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Property, PropertyImage
from .services import upload_property_media


class PropertyImageInlineForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ("url", "public_id", "sort_order", "visible")
        widgets = {
            "url": forms.HiddenInput(),
            "public_id": forms.HiddenInput(),
        }


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    form = PropertyImageInlineForm
    template = "admin/properties/propertyimage_inline.html"
    extra = 0
    fields = ("preview", "url", "public_id", "sort_order", "visible")
    readonly_fields = ("preview",)
    ordering = ("sort_order", "id")
    verbose_name = "Gallery image"
    verbose_name_plural = "Gallery images"
    can_delete = True

    def preview(self, obj: PropertyImage):
        if not obj or not obj.url:
            return "-"
        return format_html(
            '<img src="{}" alt="" style="width:100px;height:70px;object-fit:cover;border-radius:8px;border:1px solid #e5e7eb;" />',
            obj.url,
        )


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class OptionalMultiFileField(forms.FileField):
    """FileField that never raises 'No file was submitted' - files come from request.FILES in save_model."""

    def clean(self, data, initial=None):
        return None


class PropertyAdminForm(forms.ModelForm):
    main_image_upload = forms.ImageField(required=False, help_text="Upload main image (jpg/jpeg/png/webp).")
    gallery_uploads = OptionalMultiFileField(
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

    list_display = ("thumbnail", "title", "listing_type", "property_type", "price_display", "location", "featured", "published", "created_at")
    list_filter = ("listing_type", "property_type", "featured", "published", "location__city")
    list_editable = ("featured", "published")
    search_fields = ("title", "location__name", "location__city")
    ordering = ("-created_at",)
    list_per_page = 20
    list_display_links = ("title", "thumbnail")
    actions = ["make_published", "make_unpublished", "make_featured", "make_unfeatured"]

    fieldsets = (
        ("1. Category", {"fields": ("listing_type", "property_type")}),
        ("2. Basic", {"fields": ("title", "description")}),
        ("3. Price & location", {"fields": ("price", "currency", "location")}),
        ("4. Details", {"fields": ("bedrooms", "bathrooms", "area_size")}),
        ("5. Images & video", {"fields": ("main_image", "video_url", "main_image_upload", "gallery_uploads", "video_upload")}),
        ("6. Contact", {"fields": ("contact_phone", "contact_whatsapp")}),
        ("7. Visibility", {"fields": ("featured", "published", "availability")}),
    )

    readonly_fields = ("main_image", "video_url")

    def price_display(self, obj: Property):
        return f"{obj.currency} {obj.price:,.0f}" if obj.price else "-"

    price_display.short_description = "Price"

    def thumbnail(self, obj: Property):
        if not obj.main_image:
            return "-"
        return format_html(
            '<img src="{}" style="width:56px;height:56px;object-fit:cover;border-radius:12px;" />',
            obj.main_image,
        )

    @admin.action(description=_("Publish selected"))
    def make_published(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, _("%(count)d property(ies) published.") % {"count": updated})

    @admin.action(description=_("Unpublish selected"))
    def make_unpublished(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, _("%(count)d property(ies) unpublished.") % {"count": updated})

    @admin.action(description=_("Feature selected"))
    def make_featured(self, request, queryset):
        updated = queryset.update(featured=True)
        self.message_user(request, _("%(count)d property(ies) featured.") % {"count": updated})

    @admin.action(description=_("Remove from featured"))
    def make_unfeatured(self, request, queryset):
        updated = queryset.update(featured=False)
        self.message_user(request, _("%(count)d property(ies) removed from featured.") % {"count": updated})

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


