from rest_framework import serializers

from apps.tasks.serializers import TaskSerializer


class DashboardSummarySerializer(serializers.Serializer):
    total_employees = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_projects = serializers.IntegerField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()


class EmployeesByDepartmentSerializer(serializers.Serializer):
    department_id = serializers.IntegerField()
    department_name = serializers.CharField()
    employee_count = serializers.IntegerField()


class TasksByEmployeeSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    employee_name = serializers.CharField()
    task_count = serializers.IntegerField()


class ProjectProgressSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    project_name = serializers.CharField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    progress_percentage = serializers.FloatField()


class TaskReportSerializer(TaskSerializer):
    pass

