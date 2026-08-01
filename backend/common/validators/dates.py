from django.utils import timezone
from rest_framework import serializers


def validate_not_past_date(value):
    """Ensure a date is today or in the future."""

    if value < timezone.localdate():
        raise serializers.ValidationError('Date cannot be in the past.')
    return value

