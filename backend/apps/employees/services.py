from django.db.models import QuerySet

from .models import Employee


class EmployeeService:
    """Reusable employee query/business logic."""

    @staticmethod
    def get_employees() -> QuerySet[Employee]:
        return Employee.objects.select_related('department', 'user').all().order_by('first_name', 'last_name')

    @staticmethod
    def get_active_employees() -> QuerySet[Employee]:
        return EmployeeService.get_employees().filter(status=Employee.Status.ACTIVE)

