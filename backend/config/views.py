"""
Debug view to capture admin 500 errors (remove after fixing).
Visit /admin-debug/ after logging in to see the actual error.
"""
import traceback

from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_debug(request):
    """Try to render admin index and return any exception with traceback."""
    try:
        response = admin.site.index(request)
        return HttpResponse(
            f"<p>Admin index rendered successfully (status {response.status_code}).</p>"
            f"<p><a href='/admin/'>Go to admin</a></p>"
        )
    except Exception:
        tb = traceback.format_exc()
        return HttpResponse(
            f"<h2>Admin Error</h2><pre>{tb}</pre>",
            content_type="text/html",
            status=500,
        )
