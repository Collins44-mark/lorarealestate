"""
Custom Lora Real Estate Admin Dashboard - Modern SaaS-style admin.
Replaces default Django admin UI with custom views and templates.
"""
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from bookings.models import Booking
from inquiries.models import Inquiry
from locations.models import Location


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ["name", "city"]
        widgets = {
            "name": TextInput(attrs={"class": "form-input", "placeholder": "e.g. Oyster Bay"}),
            "city": TextInput(attrs={"class": "form-input", "placeholder": "e.g. Dar es Salaam"}),
        }


from properties.models import Property, PropertyImage
from properties.services import delete_property_media, destroy_cloudinary_asset, upload_property_media


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("lora_admin:login"))
        if not request.user.is_staff:
            return redirect(reverse("lora_admin:login"))
        return view_func(request, *args, **kwargs)

    return wrapper


# --- Forms ---


class PropertyForm(ModelForm):
    # main_image_upload, gallery_uploads, video_upload handled via request.FILES in view
    # (avoids "No file was submitted" validation errors with dynamic file inputs)

    class Meta:
        model = Property
        fields = [
            "listing_type",
            "property_type",
            "title",
            "description",
            "price",
            "currency",
            "location",
            "contact_phone",
            "contact_whatsapp",
            "bedrooms",
            "bathrooms",
            "area_size",
            "featured",
            "published",
            "availability",
        ]
        widgets = {
            "listing_type": forms.Select(attrs={"class": "form-input form-select"}),
            "property_type": forms.Select(attrs={"class": "form-input form-select"}),
            "location": forms.Select(attrs={"class": "form-input form-select"}),
            "title": TextInput(attrs={"class": "form-input", "placeholder": "Property title"}),
            "description": Textarea(attrs={"class": "form-input", "rows": 5, "placeholder": "Full description"}),
            "price": TextInput(attrs={"class": "form-input", "placeholder": "0"}),
            "currency": TextInput(attrs={"class": "form-input", "placeholder": "TZS"}),
            "contact_phone": TextInput(attrs={"class": "form-input", "placeholder": "+255..."}),
            "contact_whatsapp": TextInput(attrs={"class": "form-input", "placeholder": "+255..."}),
            "bedrooms": TextInput(attrs={"class": "form-input", "placeholder": "0"}),
            "bathrooms": TextInput(attrs={"class": "form-input", "placeholder": "0"}),
            "area_size": TextInput(attrs={"class": "form-input", "placeholder": "0"}),
            "availability": forms.Select(attrs={"class": "form-input form-select"}),
        }


# --- Mixin ---


class AdminMixin:
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["site_url"] = "/"
        ctx["page_title"] = getattr(self, "page_title", "Admin")
        return ctx

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("lora_admin:login"))
        if not request.user.is_staff:
            return redirect(reverse("lora_admin:login"))
        return super().dispatch(request, *args, **kwargs)


# --- Views ---


def admin_logout(request):
    logout(request)
    return redirect(reverse("lora_admin:login"))


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(reverse("lora_admin:dashboard"))
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or ""
            # Only allow relative URLs to prevent open redirect
            if not next_url or not next_url.startswith("/") or next_url.startswith("//"):
                next_url = reverse("lora_admin:dashboard")
            return redirect(next_url)
        error = "Invalid username or password."
    return render(request, "lora_admin/login.html", {"error": error})


@staff_required
def dashboard(request):
    rental = Property.objects.filter(listing_type="rent").select_related("location").order_by("-created_at")[:20]
    buy = Property.objects.filter(listing_type="sale").select_related("location").order_by("-created_at")[:20]
    return render(
        request,
        "lora_admin/dashboard.html",
        {
            "rental_properties": rental,
            "buy_properties": buy,
            "page_title": "Dashboard",
        },
    )


@staff_required
def property_list(request):
    properties = Property.objects.select_related("location").order_by("-created_at")
    listing_type = request.GET.get("type")
    if listing_type == "rent":
        properties = properties.filter(listing_type="rent")
    elif listing_type == "sale":
        properties = properties.filter(listing_type="sale")
    return render(
        request,
        "lora_admin/property_list.html",
        {"properties": properties, "page_title": "Properties"},
    )


@staff_required
def property_add(request):
    form = PropertyForm(request.POST or None, request.FILES or None, initial={"published": True})
    if request.method == "POST" and form.is_valid():
        prop = form.save()
        main_image_file = request.FILES.get("main_image_upload") if request.FILES else None
        video_file = request.FILES.get("video_upload") if request.FILES else None
        gallery_files = request.FILES.getlist("gallery_uploads") if request.FILES else []
        try:
            upload_property_media(
                prop,
                main_image_file=main_image_file,
                gallery_files=gallery_files if gallery_files else None,
                video_file=video_file,
            )
        except ValueError as e:
            from django.contrib import messages
            messages.warning(request, f"Property saved, but media upload failed: {e}")
        return redirect(reverse("lora_admin:property_detail", args=[prop.pk]))
    from locations.models import Location
    has_locations = Location.objects.exists()
    return render(
        request,
        "lora_admin/property_form.html",
        {"form": form, "page_title": "Add Property", "property": None, "has_locations": has_locations},
    )


@staff_required
def property_detail(request, pk):
    prop = get_object_or_404(Property.objects.select_related("location").prefetch_related("gallery_images"), pk=pk)
    return render(
        request,
        "lora_admin/property_detail.html",
        {"property": prop, "page_title": prop.title},
    )


@staff_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=prop)
    if request.method == "POST" and form.is_valid():
        form.save()
        post = request.POST
        main_image_file = request.FILES.get("main_image_upload") if request.FILES else None
        video_file = request.FILES.get("video_upload") if request.FILES else None
        gallery_files = request.FILES.getlist("gallery_uploads") if request.FILES else []
        main_image_delete = post.get("main_image_delete") == "1"
        gallery_delete_ids = [x.strip() for x in (post.get("gallery_delete_ids") or "").split(",") if x.strip()]

        if main_image_delete:
            if prop.main_image_public_id:
                destroy_cloudinary_asset(prop.main_image_public_id, "image")
            prop.main_image = ""
            prop.main_image_public_id = ""
            prop.save(update_fields=["main_image", "main_image_public_id", "updated_at"])

        for img_id in gallery_delete_ids:
            try:
                img = PropertyImage.objects.get(pk=int(img_id), property=prop)
                if img.public_id:
                    destroy_cloudinary_asset(img.public_id, "image")
                img.delete()
            except (PropertyImage.DoesNotExist, ValueError):
                pass

        if main_image_file and not main_image_delete:
            try:
                upload_property_media(prop, main_image_file=main_image_file)
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, "lora_admin/property_form.html", {"form": form, "page_title": "Edit Property", "property": prop, "has_locations": True})

        if gallery_files:
            try:
                upload_property_media(
                    prop,
                    gallery_files=gallery_files,
                    append_gallery=True,
                )
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, "lora_admin/property_form.html", {"form": form, "page_title": "Edit Property", "property": prop, "has_locations": True})

        if video_file:
            try:
                upload_property_media(prop, video_file=video_file)
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, "lora_admin/property_form.html", {"form": form, "page_title": "Edit Property", "property": prop, "has_locations": True})

        for key, val in post.items():
            if key.startswith("gallery_order_") and key != "gallery_order_main":
                try:
                    img_id = key.replace("gallery_order_", "")
                    if img_id.startswith("new_"):
                        continue
                    img = PropertyImage.objects.get(pk=int(img_id), property=prop)
                    img.sort_order = int(val)
                    img.save()
                except (PropertyImage.DoesNotExist, ValueError):
                    pass
            if key.startswith("gallery_visible_"):
                try:
                    img_id = key.replace("gallery_visible_", "")
                    if img_id == "main":
                        continue
                    img = PropertyImage.objects.get(pk=int(img_id), property=prop)
                    img.visible = val == "on"
                    img.save()
                except (PropertyImage.DoesNotExist, ValueError):
                    pass

        return redirect(reverse("lora_admin:property_detail", args=[prop.pk]))
    return render(
        request,
        "lora_admin/property_form.html",
        {"form": form, "page_title": "Edit Property", "property": prop, "has_locations": True},
    )


@staff_required
def property_update_status(request, pk):
    """Update published status from property list view."""
    prop = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        published_val = request.POST.get("published", "")
        if published_val == "1":
            prop.published = True
        elif published_val == "0":
            prop.published = False
        else:
            return redirect(reverse("lora_admin:property_list") + ("?" + request.GET.urlencode() if request.GET else ""))
        prop.save()
        messages.success(request, f'"{prop.title}" is now {"published" if prop.published else "draft"}.')
        return redirect(reverse("lora_admin:property_list") + ("?" + request.GET.urlencode() if request.GET else ""))
    return redirect("lora_admin:property_list")


@staff_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == "POST":
        delete_property_media(prop)
        prop.delete()
        return redirect(reverse("lora_admin:dashboard"))
    return render(request, "lora_admin/property_confirm_delete.html", {"property": prop, "page_title": "Delete Property"})


@staff_required
def locations_list(request):
    locations = Location.objects.order_by("city", "name")
    locations_with_count = [(loc, loc.properties.count()) for loc in locations]
    form = LocationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("lora_admin:locations"))
    return render(
        request,
        "lora_admin/locations.html",
        {"locations_with_count": locations_with_count, "form": form, "page_title": "Locations"},
    )


@staff_required
def location_edit(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=loc)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("lora_admin:locations"))
    return render(request, "lora_admin/location_form.html", {"form": form, "location": loc, "page_title": "Edit Location"})


@staff_required
def location_delete(request, pk):
    loc = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        if loc.properties.exists():
            return render(request, "lora_admin/location_confirm_delete.html", {"location": loc, "page_title": "Cannot delete", "has_properties": True})
        loc.delete()
        return redirect(reverse("lora_admin:locations"))
    return render(request, "lora_admin/location_confirm_delete.html", {"location": loc, "page_title": "Delete Location", "has_properties": loc.properties.exists()})


@staff_required
def bookings_list(request):
    qs = Booking.objects.select_related("property").order_by("-created_at")
    status_filter = (request.GET.get("status") or "").strip()
    if status_filter and status_filter in dict(Booking.Status.choices):
        qs = qs.filter(status=status_filter)
    bookings = list(qs[:50])
    return render(
        request,
        "lora_admin/bookings.html",
        {
            "bookings": bookings,
            "page_title": "Bookings",
            "status_filter": status_filter,
            "status_choices": Booking.Status.choices,
        },
    )


@staff_required
def inquiries_list(request):
    inquiries = Inquiry.objects.select_related("property").order_by("-created_at")[:50]
    return render(
        request,
        "lora_admin/inquiries.html",
        {"inquiries": inquiries, "page_title": "Inquiries"},
    )


@staff_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related("property"), pk=pk)
    if request.method == "POST" and request.POST.get("action") == "update_status":
        new_status = request.POST.get("status", "").strip()
        if new_status in dict(Booking.Status.choices):
            booking.status = new_status
            booking.save()
            from django.contrib import messages
            messages.success(request, f"Booking status updated to {new_status}.")
            return redirect(reverse("lora_admin:booking_detail", args=[pk]))
    return render(
        request,
        "lora_admin/booking_detail.html",
        {"booking": booking, "page_title": f"Booking #{booking.id}"},
    )
