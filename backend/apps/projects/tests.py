from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.departments.models import Department
from apps.employees.models import Employee

from .models import Project

User = get_user_model()


class ProjectApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='project.admin',
			email='project.admin@example.com',
			password='StrongPass123!',
			role=User.Role.ADMIN,
		)
		self.employee_user = User.objects.create_user(
			username='project.viewer',
			email='project.viewer@example.com',
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
		self.client.force_authenticate(self.user)

	def project_payload(self, **overrides):
		payload = {
			'name': 'Internal HR Portal',
			'project_code': 'PRJ001',
			'description': 'Build internal HR workflows.',
			'employees': [self.employee.pk],
			'start_date': timezone.localdate().isoformat(),
			'end_date': None,
			'status': Project.Status.PLANNED,
			'is_active': True,
		}
		payload.update(overrides)
		return payload

	def test_project_list_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.get(reverse('project-list'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_create_project_with_employees(self):
		response = self.client.post(reverse('project-list'), self.project_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['data']['project_code'], 'PRJ001')
		self.assertEqual(len(response.data['data']['employee_details']), 1)
		self.assertTrue(Project.objects.filter(project_code='PRJ001').exists())

	def test_duplicate_project_name_is_rejected_case_insensitive(self):
		Project.objects.create(
			name='Internal HR Portal',
			project_code='PRJ001',
			start_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('project-list'),
			self.project_payload(name='internal hr portal', project_code='PRJ002'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('name', response.data['errors'])

	def test_duplicate_project_code_is_rejected_case_insensitive(self):
		Project.objects.create(
			name='Internal HR Portal',
			project_code='PRJ001',
			start_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('project-list'),
			self.project_payload(name='Finance Tracker', project_code='prj001'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('project_code', response.data['errors'])

	def test_project_end_date_cannot_be_before_start_date(self):
		today = timezone.localdate()

		response = self.client.post(
			reverse('project-list'),
			self.project_payload(start_date=today.isoformat(), end_date=(today - timezone.timedelta(days=1)).isoformat()),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('end_date', response.data['errors'])

	def test_authenticated_user_can_assign_employees(self):
		project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())

		response = self.client.post(
			reverse('project-assign-employees', kwargs={'pk': project.pk}),
			{'employee_ids': [self.employee.pk]},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(project.employees.count(), 1)

	def test_authenticated_user_can_change_project_status(self):
		project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())

		response = self.client.post(
			reverse('project-change-status', kwargs={'pk': project.pk}),
			{'status': Project.Status.IN_PROGRESS},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		project.refresh_from_db()
		self.assertEqual(project.status, Project.Status.IN_PROGRESS)

	def test_authenticated_user_can_search_and_filter_projects(self):
		project = Project.objects.create(
			name='Internal HR Portal',
			project_code='PRJ001',
			start_date=timezone.localdate(),
			status=Project.Status.IN_PROGRESS,
		)
		project.employees.add(self.employee)
		Project.objects.create(name='Finance Tracker', project_code='PRJ002', start_date=timezone.localdate())
		self.client.force_authenticate(self.employee_user)

		response = self.client.get(reverse('project-list'), {'search': 'hr', 'status': Project.Status.IN_PROGRESS})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 1)
		self.assertEqual(response.data['results'][0]['project_code'], 'PRJ001')

	def test_authenticated_user_can_update_project(self):
		project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())

		response = self.client.patch(
			reverse('project-detail', kwargs={'pk': project.pk}),
			{'description': 'Updated project description.', 'is_active': False},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		project.refresh_from_db()
		self.assertFalse(project.is_active)
		self.assertEqual(project.description, 'Updated project description.')

	def test_authenticated_user_can_delete_project(self):
		project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())

		response = self.client.delete(reverse('project-detail', kwargs={'pk': project.pk}))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Project.objects.filter(pk=project.pk).exists())

	def test_employee_user_cannot_create_project(self):
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(reverse('project-list'), self.project_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_employee_user_cannot_change_project_status(self):
		project = Project.objects.create(name='Internal HR Portal', project_code='PRJ001', start_date=timezone.localdate())
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(
			reverse('project-change-status', kwargs={'pk': project.pk}),
			{'status': Project.Status.IN_PROGRESS},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

