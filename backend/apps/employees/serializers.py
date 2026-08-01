from rest_framework import serializers

from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer

from .models import Employee
from .validators import normalize_employee_code, normalize_required_text, validate_phone_number


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee CRUD APIs."""

    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.filter(is_active=True))
    department_detail = DepartmentSerializer(source='department', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'department',
            'department_detail',
            'employee_code',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'job_title',
            'hire_date',
            'status',
            'address',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'department_detail', 'full_name', 'created_at', 'updated_at']

    def validate_employee_code(self, value: str) -> str:
        code = normalize_employee_code(value)
        queryset = Employee.objects.filter(employee_code__iexact=code)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Employee code already exists.')
        return code

    def validate_first_name(self, value: str) -> str:
        return normalize_required_text(value, 'First name')

    def validate_last_name(self, value: str) -> str:
        return normalize_required_text(value, 'Last name')

    def validate_job_title(self, value: str) -> str:
        return normalize_required_text(value, 'Job title')

    def validate_email(self, value: str) -> str:
        email = value.lower().strip()
        queryset = Employee.objects.filter(email__iexact=email)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Employee email already exists.')
        return email

    def validate_phone_number(self, value: str) -> str:
        return validate_phone_number(value)


