from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	"""Application user used for JWT authentication and ownership tracking."""

	class Role(models.TextChoices):
		ADMIN = 'ADMIN', 'Admin'
		MANAGER = 'MANAGER', 'Manager'
		EMPLOYEE = 'EMPLOYEE', 'Employee'

	email = models.EmailField(unique=True)
	role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
	phone_number = models.CharField(max_length=20, blank=True)
	is_email_verified = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.email

# Create your models here.
