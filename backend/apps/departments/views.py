from rest_framework import status, viewsets

from common.responses.api_response import ApiResponse

from .models import Department
from .permissions import IsAuthenticatedDepartmentUser
from .serializers import DepartmentSerializer
from .services import DepartmentService


class DepartmentViewSet(viewsets.ModelViewSet):
	"""CRUD APIs for company departments."""

	serializer_class = DepartmentSerializer
	permission_classes = [IsAuthenticatedDepartmentUser]
	filterset_fields = ['is_active']
	search_fields = ['name', 'code', 'description']
	ordering_fields = ['name', 'code', 'created_at', 'updated_at']
	ordering = ['name']

	def get_queryset(self):
		return DepartmentService.get_departments()

	def retrieve(self, request, *args, **kwargs):
		department = self.get_object()
		serializer = self.get_serializer(department)
		return ApiResponse.success(serializer.data, 'Department fetched successfully.')

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return ApiResponse.success(serializer.data, 'Department created successfully.', status.HTTP_201_CREATED)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		department = self.get_object()
		serializer = self.get_serializer(department, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return ApiResponse.success(serializer.data, 'Department updated successfully.')

	def destroy(self, request, *args, **kwargs):
		department: Department = self.get_object()
		department.delete()
		return ApiResponse.success(None, 'Department deleted successfully.', status.HTTP_204_NO_CONTENT)
