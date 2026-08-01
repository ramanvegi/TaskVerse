from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.departments.models import Department

from .models import Employee

User = get_user_model()


class EmployeeApiTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='employee.admin',
			email='employee.admin@example.com',
			password='StrongPass123!',
			role=User.Role.ADMIN,
		)
		self.employee_user = User.objects.create_user(
			username='employee.viewer',
			email='employee.viewer@example.com',
			password='StrongPass123!',
			role=User.Role.EMPLOYEE,
		)
		self.department = Department.objects.create(name='Engineering', code='ENG')
		self.client.force_authenticate(self.user)

	def employee_payload(self, **overrides):
		payload = {
			'department': self.department.pk,
			'employee_code': 'EMP001',
			'first_name': 'John',
			'last_name': 'Doe',
			'email': 'john.doe@example.com',
			'phone_number': '+1 555 0101',
			'job_title': 'Backend Developer',
			'hire_date': timezone.localdate().isoformat(),
			'status': Employee.Status.ACTIVE,
			'address': 'Hyderabad',
		}
		payload.update(overrides)
		return payload

	def test_employee_list_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.get(reverse('employee-list'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_create_employee(self):
		response = self.client.post(reverse('employee-list'), self.employee_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['data']['email'], 'john.doe@example.com')
		self.assertEqual(response.data['data']['department_detail']['name'], 'Engineering')
		self.assertTrue(Employee.objects.filter(employee_code='EMP001').exists())

	def test_employee_email_duplicate_is_rejected_case_insensitive(self):
		Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('employee-list'),
			self.employee_payload(employee_code='EMP002', email='JOHN.DOE@example.com'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data['errors'])

	def test_employee_code_duplicate_is_rejected_case_insensitive(self):
		Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)

		response = self.client.post(
			reverse('employee-list'),
			self.employee_payload(employee_code='emp001', email='jane.doe@example.com'),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('employee_code', response.data['errors'])

	def test_employee_requires_valid_department(self):
		response = self.client.post(
			reverse('employee-list'),
			self.employee_payload(department=99999),
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('department', response.data['errors'])

	def test_authenticated_user_can_list_search_and_filter_employees(self):
		hr_department = Department.objects.create(name='Human Resources', code='HR')
		Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)
		Employee.objects.create(
			department=hr_department,
			employee_code='EMP002',
			first_name='Jane',
			last_name='Smith',
			email='jane.smith@example.com',
			job_title='HR Executive',
			hire_date=timezone.localdate(),
		)
		self.client.force_authenticate(self.employee_user)

		response = self.client.get(
			reverse('employee-list'),
			{'search': 'backend', 'department': self.department.pk},
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data['success'])
		self.assertEqual(response.data['count'], 1)
		self.assertEqual(response.data['results'][0]['employee_code'], 'EMP001')

	def test_authenticated_user_can_update_employee(self):
		employee = Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)

		response = self.client.patch(
			reverse('employee-detail', kwargs={'pk': employee.pk}),
			{'job_title': 'Senior Backend Developer', 'status': Employee.Status.ON_LEAVE},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		employee.refresh_from_db()
		self.assertEqual(employee.job_title, 'Senior Backend Developer')
		self.assertEqual(employee.status, Employee.Status.ON_LEAVE)

	def test_authenticated_user_can_delete_employee(self):
		employee = Employee.objects.create(
			department=self.department,
			employee_code='EMP001',
			first_name='John',
			last_name='Doe',
			email='john.doe@example.com',
			job_title='Backend Developer',
			hire_date=timezone.localdate(),
		)

		response = self.client.delete(reverse('employee-detail', kwargs={'pk': employee.pk}))

		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Employee.objects.filter(pk=employee.pk).exists())

	def test_employee_user_cannot_create_employee(self):
		self.client.force_authenticate(self.employee_user)

		response = self.client.post(reverse('employee-list'), self.employee_payload(), format='json')

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

