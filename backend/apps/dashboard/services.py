from django.db.models import Count, Q
from django.utils import timezone

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task


class DashboardService:
    """Read-only dashboard aggregation logic."""

    @staticmethod
    def get_summary() -> dict:
        today = timezone.localdate()
        return {
            'total_employees': Employee.objects.count(),
            'total_departments': Department.objects.count(),
            'total_projects': Project.objects.count(),
            'total_tasks': Task.objects.count(),
            'completed_tasks': Task.objects.filter(status=Task.Status.COMPLETED).count(),
            'pending_tasks': Task.objects.exclude(status=Task.Status.COMPLETED).count(),
            'overdue_tasks': Task.objects.exclude(status=Task.Status.COMPLETED).filter(due_date__lt=today).count(),
        }


class ReportService:
    """Read-only report aggregation logic."""

    @staticmethod
    def employees_by_department() -> list[dict]:
        departments = Department.objects.annotate(employee_count=Count('employees')).order_by('name')
        return [
            {
                'department_id': department.id,
                'department_name': department.name,
                'employee_count': department.employee_count,
            }
            for department in departments
        ]

    @staticmethod
    def tasks_by_employee() -> list[dict]:
        employees = Employee.objects.annotate(task_count=Count('assigned_tasks')).order_by('first_name', 'last_name')
        return [
            {
                'employee_id': employee.id,
                'employee_name': employee.full_name,
                'task_count': employee.task_count,
            }
            for employee in employees
        ]

    @staticmethod
    def pending_tasks():
        return Task.objects.select_related('project', 'assigned_to').exclude(status=Task.Status.COMPLETED).order_by('due_date')

    @staticmethod
    def completed_tasks():
        return Task.objects.select_related('project', 'assigned_to').filter(status=Task.Status.COMPLETED).order_by('-updated_at')

    @staticmethod
    def project_progress() -> list[dict]:
        projects = Project.objects.annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count('tasks', filter=Q(tasks__status=Task.Status.COMPLETED)),
        ).order_by('name')
        progress = []
        for project in projects:
            percentage = 0
            if project.total_tasks:
                percentage = round((project.completed_tasks / project.total_tasks) * 100, 2)
            progress.append(
                {
                    'project_id': project.id,
                    'project_name': project.name,
                    'total_tasks': project.total_tasks,
                    'completed_tasks': project.completed_tasks,
                    'progress_percentage': percentage,
                }
            )
        return progress

