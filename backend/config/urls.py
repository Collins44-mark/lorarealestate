"""
URL configuration for config project.
Lora Admin: /admin/  Login: lora / lora@25
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.urls import include, path

from config.admin_views import (
    admin_login,
    admin_logout,
    booking_delete,
    booking_detail,
    booking_update_status,
    bookings_list,
    dashboard,
    inquiry_delete,
    inquiries_list,
    location_delete,
    location_edit,
    locations_list,
    property_add,
    property_delete,
    property_detail,
    property_edit,
    property_list,
    property_toggle_status,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bookings.views import BookingViewSet
from inquiries.views import InquiryViewSet
from locations.views import LocationViewSet
from properties.views import PropertyViewSet

# Unregister default admin models we don't need
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.site_header = "Lora Real Estate Admin"
admin.site.site_title = "Lora Real Estate Admin"
admin.site.index_title = "Dashboard"
admin.site.site_url = "/"


def health(request):
    return JsonResponse({"status": "ok", "admin": "/admin/", "api": "/api/"})


router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"inquiries", InquiryViewSet, basename="inquiry")
router.register(r"locations", LocationViewSet, basename="location")

lora_admin_urls = ([
    path("", dashboard, name="dashboard"),
    path("login/", admin_login, name="login"),
    path("logout/", admin_logout, name="logout"),
    path("properties/", property_list, name="property_list"),
    path("properties/add/", property_add, name="property_add"),
    path("properties/<int:pk>/toggle-status/", property_toggle_status, name="property_toggle_status"),
    path("properties/<int:pk>/edit/", property_edit, name="property_edit"),
    path("properties/<int:pk>/delete/", property_delete, name="property_delete"),
    path("properties/<int:pk>/", property_detail, name="property_detail"),
    path("locations/", locations_list, name="locations"),
    path("locations/<int:pk>/edit/", location_edit, name="location_edit"),
    path("locations/<int:pk>/delete/", location_delete, name="location_delete"),
    path("bookings/", bookings_list, name="bookings"),
    path("bookings/<int:pk>/status/", booking_update_status, name="booking_update_status"),
    path("bookings/<int:pk>/delete/", booking_delete, name="booking_delete"),
    path("bookings/<int:pk>/", booking_detail, name="booking_detail"),
    path("inquiries/", inquiries_list, name="inquiries"),
    path("inquiries/<int:pk>/delete/", inquiry_delete, name="inquiry_delete"),
], "lora_admin")

urlpatterns = [
    path("", health),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("django-admin/", admin.site.urls),
    path(
        "admin/",
        include([
            path("password_reset/", auth_views.PasswordResetView.as_view(template_name="admin/registration/password_reset_form.html"), name="admin_password_reset"),
            path("", include(lora_admin_urls)),
        ]),
    ),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
