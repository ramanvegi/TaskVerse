from django.db import models


class Department(models.Model):
	"""Company department that groups employees."""

	name = models.CharField(max_length=100, unique=True)
	code = models.CharField(max_length=20, unique=True, blank=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']
		indexes = [
			models.Index(fields=['name']),
			models.Index(fields=['code']),
		]

	def __str__(self) -> str:
		return self.name
