from django.conf import settings
from django.db import models

from apps.departments.models import Department


class Employee(models.Model):
	"""Employee profile belonging to one department."""

	class Status(models.TextChoices):
		ACTIVE = 'ACTIVE', 'Active'
		INACTIVE = 'INACTIVE', 'Inactive'
		ON_LEAVE = 'ON_LEAVE', 'On Leave'

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		related_name='employee_profile',
		null=True,
		blank=True,
	)
	department = models.ForeignKey(
		Department,
		on_delete=models.PROTECT,
		related_name='employees',
	)
	employee_code = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	email = models.EmailField(unique=True)
	phone_number = models.CharField(max_length=20, blank=True)
	job_title = models.CharField(max_length=100)
	hire_date = models.DateField()
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
	address = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['first_name', 'last_name']
		indexes = [
			models.Index(fields=['employee_code']),
			models.Index(fields=['email']),
			models.Index(fields=['status']),
		]

	@property
	def full_name(self) -> str:
		return f'{self.first_name} {self.last_name}'.strip()

	def __str__(self) -> str:
		return f'{self.full_name} ({self.employee_code})'
