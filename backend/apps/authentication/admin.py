from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	list_display = ('id', 'email', 'username', 'role', 'is_active', 'is_staff')
	list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
	search_fields = ('email', 'username', 'first_name', 'last_name')
	ordering = ('-created_at',)
	fieldsets = UserAdmin.fieldsets + (
		('Application Details', {'fields': ('role', 'phone_number', 'is_email_verified')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		('Application Details', {'fields': ('email', 'role', 'phone_number')}),
	)

# Register your models here.
