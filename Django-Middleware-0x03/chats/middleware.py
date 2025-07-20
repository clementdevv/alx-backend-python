# messaging_app/chats/middleware.py

import logging
from datetime import datetime, timedelta
import os
from django.http import HttpResponseForbidden
from collections import deque
from django.contrib.auth.models import (
    AnonymousUser,
)  # Import AnonymousUser for type checking

# --- Existing RequestLoggingMiddleware and its logger setup ---
LOG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requests.log"
)

request_logger = logging.getLogger("request_logger")
request_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)

if not request_logger.handlers:
    request_logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = datetime.now()
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        path = request.path
        log_message = f"{timestamp} - User: {user} - Path: {path}"
        request_logger.info(log_message)
        response = self.get_response(request)
        return response


# --- Existing RestrictAccessByTimeMiddleware ---
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start_hour = 18
        allowed_end_hour = 21

        if (
            current_time.hour < allowed_start_hour
            or current_time.hour >= allowed_end_hour
        ):
            return HttpResponseForbidden(
                "Access to the messaging app is only allowed between 6 PM and 9 PM server time."
            )

        response = self.get_response(request)
        return response


# --- Existing OffensiveLanguageMiddleware (Rate Limiting) ---
class OffensiveLanguageMiddleware:
    IP_REQUEST_HISTORY = {}
    RATE_LIMIT_MESSAGES = 5
    RATE_LIMIT_WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
            if ip_address:
                ip_address = ip_address.split(",")[0].strip()
            else:
                ip_address = request.META.get("REMOTE_ADDR")

            if not ip_address:
                logging.warning(
                    "OffensiveLanguageMiddleware: Could not determine IP address for POST request."
                )
                return self.get_response(request)

            current_time = datetime.now()

            if ip_address not in self.IP_REQUEST_HISTORY:
                self.IP_REQUEST_HISTORY[ip_address] = deque()

            while self.IP_REQUEST_HISTORY[ip_address] and self.IP_REQUEST_HISTORY[
                ip_address
            ][0] < current_time - timedelta(seconds=self.RATE_LIMIT_WINDOW_SECONDS):
                self.IP_REQUEST_HISTORY[ip_address].popleft()

            if len(self.IP_REQUEST_HISTORY[ip_address]) >= self.RATE_LIMIT_MESSAGES:
                logging.warning(
                    f"OffensiveLanguageMiddleware: IP {ip_address} exceeded rate limit."
                )
                return HttpResponseForbidden(
                    f"Too many messages from your IP address. Limit is {self.RATE_LIMIT_MESSAGES} messages per {self.RATE_LIMIT_WINDOW_SECONDS} seconds."
                )

            self.IP_REQUEST_HISTORY[ip_address].append(current_time)

        response = self.get_response(request)
        return response


# --- New RolepermissionMiddleware ---
class RolepermissionMiddleware:  # This class exists and is defined
    """
    Middleware to enforce user role permissions.
    Only users with 'admin' or 'host' roles are allowed access to the chat app.
    'guest' users will be blocked.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware.
        `get_response` is a callable that represents the next middleware/view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Checks the user's role from the request and denies access if not authorized.
        """
        # We need to ensure the user is authenticated first.
        # This middleware should be placed AFTER AuthenticationMiddleware in settings.py.

        # If the user is not authenticated, they are an AnonymousUser.
        # Anonymous users typically don't have roles defined, or their role is implicitly 'guest'.
        # We'll block them if they are not authenticated.
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "Authentication required to access the messaging app."
            )

        # Check the user's role. Your User model has 'role' field.
        # Allowed roles are 'admin' and 'host' based on your models.py,
        # and the instruction mentions 'admin' or 'moderator'.
        # Assuming 'moderator' is a conceptual role, or 'host' is used for it.
        # Let's explicitly allow 'admin' and 'host' as per your model.
        # If the instruction strictly means 'admin' or 'moderator' and 'moderator' isn't in your model,
        # you might need to adjust your User model or clarify the role mapping.

        # For this implementation, we will allow 'admin' and 'host' roles.
        # Any other role (like 'guest') will be denied access.
        allowed_roles = [
            "admin",
            "host",
        ]  # Adjust this list as per your project's definition of privileged roles

        if request.user.role not in allowed_roles:
            return HttpResponseForbidden(
                f"Your role ({request.user.role}) does not have permission to access this resource."
            )

        # If the user is authenticated and has an allowed role, proceed
        response = self.get_response(request)
        return response
