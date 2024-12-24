from django.core.validators import RegexValidator

EGYPT_PHONE_REGEX: RegexValidator = RegexValidator(
    regex=r"^\+20(10|11|12|15)[0-9]{8}$",
    message="Enter a phone number in this format: '+201xxxxxxxxx'.",
)
