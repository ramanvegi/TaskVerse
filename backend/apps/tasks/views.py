from rest_framework import status, viewsets
from rest_framework.decorators import action

from common.responses.api_response import ApiResponse

from .models import Task
from .permissions import IsAuthenticatedTaskUser
from .serializers import CommentSerializer, TaskAssignSerializer, TaskSerializer, TaskStatusSerializer
from .services import TaskService


class TaskViewSet(viewsets.ModelViewSet):
	"""CRUD APIs for tasks, assignment, status changes, and comments."""

	serializer_class = TaskSerializer
	permission_classes = [IsAuthenticatedTaskUser]
	filterset_fields = ['project', 'assigned_to', 'status', 'priority', 'due_date']
	search_fields = ['title', 'description', 'project__name', 'assigned_to__first_name', 'assigned_to__last_name']
	ordering_fields = ['title', 'due_date', 'priority', 'status', 'created_at']
	ordering = ['due_date', 'priority', 'title']

	def get_queryset(self):
		return TaskService.get_tasks()

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)

	def retrieve(self, request, *args, **kwargs):
		task = self.get_object()
		serializer = self.get_serializer(task)
		return ApiResponse.success(serializer.data, 'Task fetched successfully.')

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return ApiResponse.success(serializer.data, 'Task created successfully.', status.HTTP_201_CREATED)

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		task = self.get_object()
		serializer = self.get_serializer(task, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return ApiResponse.success(serializer.data, 'Task updated successfully.')

	def destroy(self, request, *args, **kwargs):
		task: Task = self.get_object()
		task.delete()
		return ApiResponse.success(None, 'Task deleted successfully.', status.HTTP_204_NO_CONTENT)

	@action(detail=True, methods=['post'], url_path='assign')
	def assign(self, request, pk=None):
		task = self.get_object()
		serializer = TaskAssignSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		TaskService.assign_task(task, serializer.validated_data['assigned_to'])
		return ApiResponse.success(self.get_serializer(task).data, 'Task assigned successfully.')

	@action(detail=True, methods=['post'], url_path='change-status')
	def change_status(self, request, pk=None):
		task = self.get_object()
		serializer = TaskStatusSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		TaskService.change_status(task, serializer.validated_data['status'])
		return ApiResponse.success(self.get_serializer(task).data, 'Task status updated successfully.')

	@action(detail=True, methods=['get', 'post'], url_path='comments')
	def comments(self, request, pk=None):
		task = self.get_object()
		if request.method == 'GET':
			serializer = CommentSerializer(task.comments.select_related('author'), many=True)
			return ApiResponse.success(serializer.data, 'Comments fetched successfully.')

		serializer = CommentSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		comment = TaskService.add_comment(task, request.user, serializer.validated_data['message'])
		return ApiResponse.success(CommentSerializer(comment).data, 'Comment added successfully.', status.HTTP_201_CREATED)
