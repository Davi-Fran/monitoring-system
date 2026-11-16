from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_in_future(value):
        MEASUREMENT_TOLERANTE = timedelta(minutes=5)
        limit = timezone.now() + MEASUREMENT_TOLERANTE

        if value > limit:
            raise ValidationError(
                "Invalid measurement: the measurement date cannot be in the future.",
                code="future_measurement"
            )