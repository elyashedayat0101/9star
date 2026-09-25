from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="Enter a valid Iranian mobile number (e.g. 09123456789).",
)
