from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Department

User = get_user_model()


class DepartmentApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='department.admin',
			email='department.admin@example.com',
			password='StrongPass123!',
			role=User.Role.ADMIN,
		)
		self.client.force_authenticate(self.user)
		self.employee_user = User.objects.create_user(
			username='department.employee',
			email='department.employee@example.com',
			password='StrongPass123!',
			role=User.Role.EMPLOYEE,
		)

	def test_department_list_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.get(reverse('department-list'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_create_department(self):
		response = self.client.post(
			reverse('department-list'),
			{
				'name': 'Engineering',
				'code': 'ENG',
				'description': 'Builds and maintains products.',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['data']['name'], 'Engineering')
		self.assertTrue(Department.objects.filter(name='Engineering').exists())

	def test_duplicate_department_name_is_rejected_case_insensitive(self):
		Department.objects.create(name='Human Resources', code='HR')

		response = self.client.post(
			reverse('department-list'),
			{'name': 'human resources', 'code': 'HR2'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('name', response.data['errors'])

	def test_duplicate_department_code_is_rejected_case_insensitive(self):
		Department.objects.create(name='Finance', code='FIN')

		response = self.client.post(
			reverse('department-list'),
			{'name': 'Accounts', 'code': 'fin'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('code', response.data['errors'])

	def test_authenticated_user_can_list_and_search_departments(self):
		Department.objects.create(name='Engineering', code='ENG')
		Department.objects.create(name='Human Resources', code='HR')
		self.client.force_authenticate(self.employee_user)

		response = self.client.get(reverse('department-list'), {'search': 'eng'})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['count'], 1)
		self.assertEqual(response.data['results'][0]['name'], 'Engineering')

	def test_authenticated_user_can_update_department(self):
		department = Department.objects.create(name='Operations', code='OPS')

		response = self.client.patch(
			reverse('department-detail', kwargs={'pk': department.pk}),
			{'description': 'Handles day-to-day operations.', 'is_active': False},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		department.refresh_from_db()
		self.assertFalse(department.is_active)
		self.assertEqual(department.description, 'Handles day-to-day operations.')

	def test_authenticated_user_can_delete_department(self):
		department = Department.objects.create(name='Support', code='SUP')

		response = self.client.delete(reverse('department-detail', kwargs={'pk': department.pk}))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Department.objects.filter(pk=department.pk).exists())

	def test_employee_user_cannot_create_department(self):
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(
			reverse('department-list'),
			{'name': 'Finance', 'code': 'FIN'},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

