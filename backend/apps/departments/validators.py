import re

from rest_framework import serializers


_CODE_PATTERN = re.compile(r'^[A-Z0-9_-]+$')


def normalize_department_name(value: str) -> str:
    name = ' '.join(value.strip().split())
    if len(name) < 2:
        raise serializers.ValidationError('Department name must contain at least 2 characters.')
    return name


def normalize_department_code(value: str) -> str:
    code = value.strip().upper()
    if code and not _CODE_PATTERN.match(code):
        raise serializers.ValidationError('Department code can contain only uppercase letters, numbers, hyphens, and underscores.')
    return code

