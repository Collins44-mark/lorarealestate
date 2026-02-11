from rest_framework.permissions import BasePermission


class IsAdminUserForUnsafeMethods(BasePermission):
    """
    Public can read (safe methods).
    Admin-only for write (POST/PUT/PATCH/DELETE).
    """

    def has_permission(self, request, view) -> bool:
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and user.is_staff)

