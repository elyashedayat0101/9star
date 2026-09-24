from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ApiAuthMixin:
    """
    Mixin for APIs that require an authenticated user.

    `DEFAULT_PERMISSION_CLASSES` already includes `IsAuthenticated`
    project-wide (see REST_FRAMEWORK settings), so this mixin exists
    mostly for readability - it makes the requirement explicit on the
    API class itself, and gives us a single place to extend later
    (e.g. swap in a stricter permission class for a specific API).
    """

    authentication_classes = APIView.authentication_classes
    permission_classes = [IsAuthenticated]
