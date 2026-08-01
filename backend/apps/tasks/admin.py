from django.contrib import admin

from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'project', 'assigned_to', 'priority', 'status', 'due_date')
	list_filter = ('status', 'priority', 'project', 'due_date', 'created_at')
	search_fields = ('title', 'description', 'project__name', 'assigned_to__first_name', 'assigned_to__last_name')
	ordering = ('due_date', 'priority', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'task', 'author', 'created_at')
	list_filter = ('created_at',)
	search_fields = ('message', 'task__title', 'author__email')
