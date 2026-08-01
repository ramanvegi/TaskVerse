from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()


class DashboardReportApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='dashboard.admin',
			email='dashboard.admin@example.com',
			password='StrongPass123!',
		)
		self.department = Department.objects.create(name='Engineering', code='ENG')
		self.employee = Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)
		self.project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())
		self.todo_task = Task.objects.create(
			project=self.project,
			assigned_to=self.employee,
			title='Pending task',
			due_date=timezone.localdate(),
			status=Task.Status.TODO,
		)
		self.completed_task = Task.objects.create(
			project=self.project,
			assigned_to=self.employee,
			title='Completed task',
			due_date=timezone.localdate(),
			status=Task.Status.COMPLETED,
		)
		self.client.force_authenticate(self.user)

	def test_dashboard_summary_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.get(reverse('dashboard-summary'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_dashboard_summary_returns_counts(self):
		response = self.client.get(reverse('dashboard-summary'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['data']['total_employees'], 1)
		self.assertEqual(response.data['data']['total_departments'], 1)
		self.assertEqual(response.data['data']['total_projects'], 1)
		self.assertEqual(response.data['data']['total_tasks'], 2)
		self.assertEqual(response.data['data']['completed_tasks'], 1)
		self.assertEqual(response.data['data']['pending_tasks'], 1)

	def test_employees_by_department_report(self):
		response = self.client.get(reverse('employees-by-department-report'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['data'][0]['department_name'], 'Engineering')
		self.assertEqual(response.data['data'][0]['employee_count'], 1)

	def test_tasks_by_employee_report(self):
		response = self.client.get(reverse('tasks-by-employee-report'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['data'][0]['employee_name'], 'John Doe')
		self.assertEqual(response.data['data'][0]['task_count'], 2)

	def test_pending_and_completed_task_reports(self):
		pending_response = self.client.get(reverse('pending-tasks-report'))
		completed_response = self.client.get(reverse('completed-tasks-report'))

		self.assertEqual(pending_response.status_code, status.HTTP_200_OK)
		self.assertEqual(completed_response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(pending_response.data['data']), 1)
		self.assertEqual(len(completed_response.data['data']), 1)
		self.assertEqual(pending_response.data['data'][0]['title'], 'Pending task')
		self.assertEqual(completed_response.data['data'][0]['title'], 'Completed task')

	def test_project_progress_report(self):
		response = self.client.get(reverse('project-progress-report'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['data'][0]['project_name'], 'Internal HR Portal')
		self.assertEqual(response.data['data'][0]['total_tasks'], 2)
		self.assertEqual(response.data['data'][0]['completed_tasks'], 1)
		self.assertEqual(response.data['data'][0]['progress_percentage'], 50.0)
