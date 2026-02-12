"""
Middleware to log 500 errors with full traceback (for debugging on Render).
Remove or disable in production if not needed.
"""
import logging
import traceback

logger = logging.getLogger("django")


class Log500Middleware:
    """Log 500 errors with full traceback to help debug deployment issues."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(
            "Unhandled exception: %s\n%s",
            exception,
            traceback.format_exc(),
            exc_info=True,
        )
        return None
