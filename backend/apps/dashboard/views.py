from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from common.responses.api_response import ApiResponse

from .serializers import (
	DashboardSummarySerializer,
	EmployeesByDepartmentSerializer,
	ProjectProgressSerializer,
	TaskReportSerializer,
	TasksByEmployeeSerializer,
)
from .services import DashboardService, ReportService


class DashboardSummaryView(GenericAPIView):
	serializer_class = DashboardSummarySerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return ApiResponse.success(DashboardService.get_summary(), 'Dashboard summary fetched successfully.')


class EmployeesByDepartmentReportView(GenericAPIView):
	serializer_class = EmployeesByDepartmentSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = ReportService.employees_by_department()
		return ApiResponse.success(data, 'Employees by department report fetched successfully.')


class TasksByEmployeeReportView(GenericAPIView):
	serializer_class = TasksByEmployeeSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = ReportService.tasks_by_employee()
		return ApiResponse.success(data, 'Tasks by employee report fetched successfully.')


class PendingTasksReportView(GenericAPIView):
	serializer_class = TaskReportSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		serializer = self.get_serializer(ReportService.pending_tasks(), many=True)
		return ApiResponse.success(serializer.data, 'Pending tasks report fetched successfully.')


class CompletedTasksReportView(GenericAPIView):
	serializer_class = TaskReportSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		serializer = self.get_serializer(ReportService.completed_tasks(), many=True)
		return ApiResponse.success(serializer.data, 'Completed tasks report fetched successfully.')


class ProjectProgressReportView(GenericAPIView):
	serializer_class = ProjectProgressSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = ReportService.project_progress()
		return ApiResponse.success(data, 'Project progress report fetched successfully.')
