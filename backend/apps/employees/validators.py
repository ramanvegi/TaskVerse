import re

from rest_framework import serializers

_CODE_PATTERN = re.compile(r'^[A-Z0-9_-]+$')
_PHONE_PATTERN = re.compile(r'^[0-9+\-() ]*$')


def normalize_required_text(value: str, field_name: str, min_length: int = 2) -> str:
    text = ' '.join(value.strip().split())
    if len(text) < min_length:
        raise serializers.ValidationError(f'{field_name} must contain at least {min_length} characters.')
    return text


def normalize_employee_code(value: str) -> str:
    code = value.strip().upper()
    if not _CODE_PATTERN.match(code):
        raise serializers.ValidationError('Employee code can contain only uppercase letters, numbers, hyphens, and underscores.')
    return code


def validate_phone_number(value: str) -> str:
    phone_number = value.strip()
    if phone_number and not _PHONE_PATTERN.match(phone_number):
        raise serializers.ValidationError('Phone number contains invalid characters.')
    return phone_number

