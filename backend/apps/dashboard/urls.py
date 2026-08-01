from django.urls import path

from .views import (
    CompletedTasksReportView,
    DashboardSummaryView,
    EmployeesByDepartmentReportView,
    PendingTasksReportView,
    ProjectProgressReportView,
    TasksByEmployeeReportView,
)

urlpatterns = [
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('reports/employees-by-department/', EmployeesByDepartmentReportView.as_view(), name='employees-by-department-report'),
    path('reports/tasks-by-employee/', TasksByEmployeeReportView.as_view(), name='tasks-by-employee-report'),
    path('reports/pending-tasks/', PendingTasksReportView.as_view(), name='pending-tasks-report'),
    path('reports/completed-tasks/', CompletedTasksReportView.as_view(), name='completed-tasks-report'),
    path('reports/project-progress/', ProjectProgressReportView.as_view(), name='project-progress-report'),
]

