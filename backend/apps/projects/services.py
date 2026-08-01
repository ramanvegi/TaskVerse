from django.db.models import QuerySet

from apps.employees.models import Employee

from .models import Project


class ProjectService:
    """Reusable project query and assignment logic."""

    @staticmethod
    def get_projects() -> QuerySet[Project]:
        return Project.objects.prefetch_related('employees', 'employees__department').all().order_by('name')

    @staticmethod
    def assign_employees(project: Project, employees: list[Employee]) -> Project:
        project.employees.set(employees)
        return project

    @staticmethod
    def change_status(project: Project, status: str) -> Project:
        project.status = status
        project.save(update_fields=['status', 'updated_at'])
        return project

