from django.conf import settings
from django.db import models

from apps.employees.models import Employee
from apps.projects.models import Project


class Task(models.Model):
	"""Work item that belongs to a project and can be assigned to an employee."""

	class Status(models.TextChoices):
		TODO = 'TODO', 'Todo'
		IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
		COMPLETED = 'COMPLETED', 'Completed'

	class Priority(models.TextChoices):
		LOW = 'LOW', 'Low'
		MEDIUM = 'MEDIUM', 'Medium'
		HIGH = 'HIGH', 'High'

	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
	assigned_to = models.ForeignKey(
		Employee,
		on_delete=models.SET_NULL,
		related_name='assigned_tasks',
		null=True,
		blank=True,
	)
	title = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	due_date = models.DateField()
	priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		related_name='created_tasks',
		null=True,
		blank=True,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['due_date', 'priority', 'title']
		indexes = [
			models.Index(fields=['status']),
			models.Index(fields=['priority']),
			models.Index(fields=['due_date']),
		]

	def __str__(self) -> str:
		return self.title


class Comment(models.Model):
	"""Comment added to a task."""

	task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		related_name='task_comments',
		null=True,
		blank=True,
	)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self) -> str:
		return f'Comment on {self.task_id}'
