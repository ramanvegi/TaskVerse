from django.db.models import QuerySet

from .models import Department


class DepartmentService:
    """Reusable department query/business logic."""

    @staticmethod
    def get_departments() -> QuerySet[Department]:
        return Department.objects.all().order_by('name')

    @staticmethod
    def get_active_departments() -> QuerySet[Department]:
        return Department.objects.filter(is_active=True).order_by('name')

