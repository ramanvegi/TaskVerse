from rest_framework import serializers

from apps.employees.models import Employee
from apps.employees.serializers import EmployeeSerializer

from .models import Project
from .validators import normalize_project_code, normalize_project_name, validate_project_dates


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project CRUD APIs."""

    employees = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.filter(status=Employee.Status.ACTIVE),
        required=False,
    )
    employee_details = EmployeeSerializer(source='employees', many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'project_code',
            'description',
            'employees',
            'employee_details',
            'start_date',
            'end_date',
            'status',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'employee_details', 'created_at', 'updated_at']

    def validate_name(self, value: str) -> str:
        name = normalize_project_name(value)
        queryset = Project.objects.filter(name__iexact=name)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Project name already exists.')
        return name

    def validate_project_code(self, value: str) -> str:
        code = normalize_project_code(value)
        queryset = Project.objects.filter(project_code__iexact=code)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Project code already exists.')
        return code

    def validate(self, attrs):
        start_date = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end_date = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        if start_date:
            validate_project_dates(start_date, end_date)
        return attrs


class ProjectAssignEmployeesSerializer(serializers.Serializer):
    employee_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.filter(status=Employee.Status.ACTIVE),
        source='employees',
    )


class ProjectStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Project.Status.choices)

