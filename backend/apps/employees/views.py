from rest_framework import status, viewsets

from common.responses.api_response import ApiResponse

from .models import Employee
from .permissions import IsAuthenticatedEmployeeUser
from .serializers import EmployeeSerializer
from .services import EmployeeService


class EmployeeViewSet(viewsets.ModelViewSet):
	"""CRUD APIs for employees."""

	serializer_class = EmployeeSerializer
	permission_classes = [IsAuthenticatedEmployeeUser]
	filterset_fields = ['department', 'status']
	search_fields = ['first_name', 'last_name', 'email', 'employee_code', 'job_title', 'department__name']
	ordering_fields = ['first_name', 'last_name', 'email', 'employee_code', 'hire_date', 'created_at']
	ordering = ['first_name', 'last_name']

	def get_queryset(self):
		return EmployeeService.get_employees()

	def retrieve(self, request, *args, **kwargs):
		employee = self.get_object()
		serializer = self.get_serializer(employee)
		return ApiResponse.success(serializer.data, 'Employee fetched successfully.')

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return ApiResponse.success(serializer.data, 'Employee created successfully.', status.HTTP_201_CREATED)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		employee = self.get_object()
		serializer = self.get_serializer(employee, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return ApiResponse.success(serializer.data, 'Employee updated successfully.')

	def destroy(self, request, *args, **kwargs):
		employee: Employee = self.get_object()
		employee.delete()
		return ApiResponse.success(None, 'Employee deleted successfully.', status.HTTP_204_NO_CONTENT)
