from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'project_code', 'name', 'status', 'start_date', 'end_date', 'is_active')
	list_filter = ('status', 'is_active', 'start_date', 'created_at')
	search_fields = ('project_code', 'name', 'description')
	ordering = ('name',)
	filter_horizontal = ('employees',)
