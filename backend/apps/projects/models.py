from django.db import models

from apps.employees.models import Employee


class Project(models.Model):
	"""Company project with assigned employees and lifecycle status."""

	class Status(models.TextChoices):
		PLANNED = 'PLANNED', 'Planned'
		IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
		ON_HOLD = 'ON_HOLD', 'On Hold'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	name = models.CharField(max_length=150, unique=True)
	project_code = models.CharField(max_length=30, unique=True)
	description = models.TextField(blank=True)
	employees = models.ManyToManyField(Employee, related_name='projects', blank=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']
		indexes = [
			models.Index(fields=['name']),
			models.Index(fields=['project_code']),
			models.Index(fields=['status']),
		]

	def __str__(self) -> str:
		return f'{self.name} ({self.project_code})'
