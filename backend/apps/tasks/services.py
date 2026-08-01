from django.db.models import QuerySet

from apps.employees.models import Employee

from .models import Comment, Task


class TaskService:
    """Reusable task query and business logic."""

    @staticmethod
    def get_tasks() -> QuerySet[Task]:
        return Task.objects.select_related('project', 'assigned_to', 'assigned_to__department', 'created_by').prefetch_related('comments')

    @staticmethod
    def assign_task(task: Task, employee: Employee | None) -> Task:
        task.assigned_to = employee
        task.save(update_fields=['assigned_to', 'updated_at'])
        return task

    @staticmethod
    def change_status(task: Task, status: str) -> Task:
        task.status = status
        task.save(update_fields=['status', 'updated_at'])
        return task

    @staticmethod
    def add_comment(task: Task, author, message: str) -> Comment:
        return Comment.objects.create(task=task, author=author, message=message)

