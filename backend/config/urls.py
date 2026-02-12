"""
URL configuration for config project.
Admin: /admin/  Login: lora / lora@25
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bookings.views import BookingViewSet
from inquiries.views import InquiryViewSet
from locations.views import LocationViewSet
from properties.views import PropertyViewSet


admin.site.site_header = "Lora Real Estate Admin"
admin.site.site_title = "Lora Real Estate Admin"
admin.site.index_title = "Dashboard"


def health(request):
    return JsonResponse({"status": "ok", "admin": "/admin/", "api": "/api/"})


router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"inquiries", InquiryViewSet, basename="inquiry")
router.register(r"locations", LocationViewSet, basename="location")

urlpatterns = [
    path("", health),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path(
        "admin/",
        include([
            path(
                "password_reset/",
                auth_views.PasswordResetView.as_view(
                    template_name="admin/registration/password_reset_form.html",
                ),
                name="admin_password_reset",
            ),
            path("", admin.site.urls),
        ]),
    ),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
