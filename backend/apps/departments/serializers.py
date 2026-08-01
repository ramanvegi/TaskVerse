from rest_framework import serializers

from .models import Department
from .validators import normalize_department_code, normalize_department_name


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department CRUD APIs."""

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'code',
            'description',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value: str) -> str:
        name = normalize_department_name(value)
        queryset = Department.objects.filter(name__iexact=name)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Department name already exists.')
        return name

    def validate_code(self, value: str) -> str:
        code = normalize_department_code(value)
        if not code:
            return code

        queryset = Department.objects.filter(code__iexact=code)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Department code already exists.')
        return code

