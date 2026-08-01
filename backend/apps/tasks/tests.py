from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.departments.models import Department
from apps.employees.models import Employee
from apps.projects.models import Project

from .models import Comment, Task

User = get_user_model()


class TaskApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='task.admin',
			email='task.admin@example.com',
			password='StrongPass123!',
			role=User.Role.ADMIN,
		)
		self.employee_user = User.objects.create_user(
			username='task.employee',
			email='task.employee@example.com',
			password='StrongPass123!',
			role=User.Role.EMPLOYEE,
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
		self.project = Project.objects.create(
			name='Internal HR Portal',
			project_code='PRJ001',
			start_date=timezone.localdate(),
		)
		self.project.employees.add(self.employee)
		self.client.force_authenticate(self.user)

	def task_payload(self, **overrides):
		payload = {
			'project': self.project.pk,
			'assigned_to': self.employee.pk,
			'title': 'Create employee API',
			'description': 'Build and test employee endpoint.',
			'due_date': timezone.localdate().isoformat(),
			'priority': Task.Priority.HIGH,
			'status': Task.Status.TODO,
		}
		payload.update(overrides)
		return payload

	def test_task_list_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.get(reverse('task-list'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_create_task(self):
		response = self.client.post(reverse('task-list'), self.task_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['data']['title'], 'Create employee API')
		self.assertEqual(response.data['data']['created_by'], self.user.pk)
		self.assertTrue(Task.objects.filter(title='Create employee API').exists())

	def test_task_due_date_cannot_be_in_past(self):
		response = self.client.post(
			reverse('task-list'),
			self.task_payload(due_date=(timezone.localdate() - timezone.timedelta(days=1)).isoformat()),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('due_date', response.data['errors'])

	def test_authenticated_user_can_assign_task(self):
		task = Task.objects.create(
			project=self.project,
			title='Create task API',
			due_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('task-assign', kwargs={'pk': task.pk}),
			{'assigned_to': self.employee.pk},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		task.refresh_from_db()
		self.assertEqual(task.assigned_to, self.employee)

	def test_authenticated_user_can_change_task_status(self):
		task = Task.objects.create(
			project=self.project,
			assigned_to=self.employee,
			title='Create task API',
			due_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('task-change-status', kwargs={'pk': task.pk}),
			{'status': Task.Status.IN_PROGRESS},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		task.refresh_from_db()
		self.assertEqual(task.status, Task.Status.IN_PROGRESS)

	def test_authenticated_user_can_add_and_view_comments(self):
		task = Task.objects.create(
			project=self.project,
			assigned_to=self.employee,
			title='Create task API',
			due_date=timezone.localdate(),
		)
		self.client.force_authenticate(self.employee_user)

		add_response = self.client.post(
			reverse('task-comments', kwargs={'pk': task.pk}),
			{'message': 'Initial implementation completed.'},
			format='json',
		)
		list_response = self.client.get(reverse('task-comments', kwargs={'pk': task.pk}))

		self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(list_response.status_code, status.HTTP_200_OK)
		self.assertEqual(Comment.objects.filter(task=task).count(), 1)
		self.assertEqual(list_response.data['data'][0]['message'], 'Initial implementation completed.')

	def test_authenticated_user_can_search_and_filter_tasks(self):
		Task.objects.create(
			project=self.project,
			assigned_to=self.employee,
			title='Create employee API',
			due_date=timezone.localdate(),
			priority=Task.Priority.HIGH,
		)
		Task.objects.create(
			project=self.project,
			title='Write docs',
			due_date=timezone.localdate(),
			priority=Task.Priority.LOW,
		)
		self.client.force_authenticate(self.employee_user)

		response = self.client.get(reverse('task-list'), {'search': 'employee', 'priority': Task.Priority.HIGH})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 1)
		self.assertEqual(response.data['results'][0]['title'], 'Create employee API')

	def test_authenticated_user_can_update_task(self):
		task = Task.objects.create(
			project=self.project,
			title='Create task API',
			due_date=timezone.localdate(),
		)

		response = self.client.patch(
			reverse('task-detail', kwargs={'pk': task.pk}),
			{'priority': Task.Priority.LOW, 'description': 'Updated description.'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		task.refresh_from_db()
		self.assertEqual(task.priority, Task.Priority.LOW)
		self.assertEqual(task.description, 'Updated description.')

	def test_authenticated_user_can_delete_task(self):
		task = Task.objects.create(
			project=self.project,
			title='Create task API',
			due_date=timezone.localdate(),
		)

		response = self.client.delete(reverse('task-detail', kwargs={'pk': task.pk}))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Task.objects.filter(pk=task.pk).exists())

	def test_employee_user_cannot_create_task(self):
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(reverse('task-list'), self.task_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_employee_user_cannot_assign_task(self):
		task = Task.objects.create(
			project=self.project,
			title='Create task API',
			due_date=timezone.localdate(),
		)
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(
			reverse('task-assign', kwargs={'pk': task.pk}),
			{'assigned_to': self.employee.pk},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

