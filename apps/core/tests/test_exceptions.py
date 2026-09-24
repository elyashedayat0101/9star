from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from django.test import RequestFactory, TestCase
from rest_framework import exceptions
from rest_framework.views import APIView

from apps.core.exceptions import ApplicationError, custom_exception_handler


class CustomExceptionHandlerTests(TestCase):
    def setUp(self):
        self.request = APIView().initialize_request(RequestFactory().get("/"))
        self.ctx = {"request": self.request}

    def test_application_error_is_normalized(self):
        exc = ApplicationError(message="Something is not correct", extra={"code": "random"})

        response = custom_exception_handler(exc, self.ctx)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {"message": "Something is not correct", "extra": {"code": "random"}},
        )

    def test_django_validation_error_is_normalized(self):
        exc = DjangoValidationError("Some error message")

        response = custom_exception_handler(exc, self.ctx)

        self.assertEqual(
            response.data,
            {
                "message": "Validation error",
                "extra": {"fields": {"non_field_errors": ["Some error message"]}},
            },
        )

    def test_http404_is_normalized_to_not_found(self):
        response = custom_exception_handler(Http404(), self.ctx)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {"message": "Not found.", "extra": {}})

    def test_permission_denied_is_normalized(self):
        response = custom_exception_handler(PermissionDenied(), self.ctx)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data,
            {"message": "You do not have permission to perform this action.", "extra": {}},
        )

    def test_drf_validation_error_is_normalized(self):
        exc = exceptions.ValidationError("Some error message")

        response = custom_exception_handler(exc, self.ctx)

        self.assertEqual(
            response.data,
            {"message": "Validation error", "extra": {"fields": ["Some error message"]}},
        )

    def test_unhandled_exception_falls_back_to_drf_default(self):
        response = custom_exception_handler(exceptions.Throttled(), self.ctx)

        self.assertEqual(response.data["message"], "Request was throttled.")
        self.assertEqual(response.data["extra"], {})
