"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from config.views import admin_debug
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bookings.views import BookingViewSet
from inquiries.views import InquiryViewSet
from locations.views import LocationViewSet
from properties.views import PropertyViewSet


admin.site.site_header = "Lora Real Estate Admin"
admin.site.site_title = "Lora Real Estate Admin"
admin.site.index_title = "Dashboard"
admin.site.index_template = "admin/index_lora.html"


def health(request):
    return JsonResponse(
        {
            "status": "ok",
            "admin": "/admin/",
            "admin_debug": "/admin-debug/",
            "api": "/api/",
        }
    )


router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"inquiries", InquiryViewSet, basename="inquiry")
router.register(r"locations", LocationViewSet, basename="location")

urlpatterns = [
    path("", health),
    path("admin-debug/", admin_debug),
    path("admin-debug", admin_debug),  # no trailing slash
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
