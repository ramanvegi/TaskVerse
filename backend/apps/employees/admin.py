from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('id', 'employee_code', 'full_name', 'email', 'department', 'job_title', 'status')
	list_filter = ('status', 'department', 'hire_date', 'created_at')
	search_fields = ('employee_code', 'first_name', 'last_name', 'email', 'job_title')
	ordering = ('first_name', 'last_name')
