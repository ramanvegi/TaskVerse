from rest_framework import status, viewsets
from rest_framework.decorators import action

from common.responses.api_response import ApiResponse

from .models import Project
from .permissions import IsAuthenticatedProjectUser
from .serializers import ProjectAssignEmployeesSerializer, ProjectSerializer, ProjectStatusSerializer
from .services import ProjectService


class ProjectViewSet(viewsets.ModelViewSet):
	"""CRUD APIs for projects, employee assignment, and status changes."""

	serializer_class = ProjectSerializer
	permission_classes = [IsAuthenticatedProjectUser]
	filterset_fields = ['status', 'is_active', 'employees']
	search_fields = ['name', 'project_code', 'description', 'employees__first_name', 'employees__last_name']
	ordering_fields = ['name', 'project_code', 'start_date', 'end_date', 'created_at']
	ordering = ['name']

	def get_queryset(self):
		return ProjectService.get_projects()

	def retrieve(self, request, *args, **kwargs):
		project = self.get_object()
		serializer = self.get_serializer(project)
		return ApiResponse.success(serializer.data, 'Project fetched successfully.')

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return ApiResponse.success(serializer.data, 'Project created successfully.', status.HTTP_201_CREATED)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		project = self.get_object()
		serializer = self.get_serializer(project, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return ApiResponse.success(serializer.data, 'Project updated successfully.')

	def destroy(self, request, *args, **kwargs):
		project: Project = self.get_object()
		project.delete()
		return ApiResponse.success(None, 'Project deleted successfully.', status.HTTP_204_NO_CONTENT)

	@action(detail=True, methods=['post'], url_path='assign-employees')
	def assign_employees(self, request, pk=None):
		project = self.get_object()
		serializer = ProjectAssignEmployeesSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		ProjectService.assign_employees(project, serializer.validated_data['employees'])
		return ApiResponse.success(self.get_serializer(project).data, 'Employees assigned successfully.')

	@action(detail=True, methods=['post'], url_path='change-status')
	def change_status(self, request, pk=None):
		project = self.get_object()
		serializer = ProjectStatusSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		ProjectService.change_status(project, serializer.validated_data['status'])
		return ApiResponse.success(self.get_serializer(project).data, 'Project status updated successfully.')
