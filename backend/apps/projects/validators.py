import re

from rest_framework import serializers

_CODE_PATTERN = re.compile(r'^[A-Z0-9_-]+$')


def normalize_project_name(value: str) -> str:
    name = ' '.join(value.strip().split())
    if len(name) < 2:
        raise serializers.ValidationError('Project name must contain at least 2 characters.')
    return name


def normalize_project_code(value: str) -> str:
    code = value.strip().upper()
    if not _CODE_PATTERN.match(code):
        raise serializers.ValidationError('Project code can contain only uppercase letters, numbers, hyphens, and underscores.')
    return code


def validate_project_dates(start_date, end_date):
    if end_date and end_date < start_date:
        raise serializers.ValidationError({'end_date': 'End date cannot be before start date.'})

