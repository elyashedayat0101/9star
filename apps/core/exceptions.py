from typing import Any

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


class ApplicationError(Exception):
    """Raised from services/selectors for expected business rule violations."""

    def __init__(self, message: str, extra: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Normalize error responses to:

        {
            "message": "...",
            "extra": {}
        }
    """

    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(detail=as_serializer_error(exc))
    elif isinstance(exc, Http404):
        exc = NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = DRFPermissionDenied()

    if isinstance(exc, ApplicationError):
        return Response(
            {"message": exc.message, "extra": exc.extra},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and set(response.data.keys()) == {"detail"}:
            response.data = {
                "message": str(response.data["detail"]),
                "extra": {},
            }
        else:
            response.data = {
                "message": "Validation error",
                "extra": {"fields": response.data},
            }

    return response
