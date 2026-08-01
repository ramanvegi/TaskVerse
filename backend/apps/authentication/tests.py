from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationApiTests(APITestCase):
	def test_user_can_register_and_receive_tokens(self):
		response = self.client.post(
			reverse('register'),
			{
				'username': 'john.doe',
				'email': 'john@example.com',
				'first_name': 'John',
				'last_name': 'Doe',
				'password': 'StrongPass123!',
				'password_confirm': 'StrongPass123!',
			},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data['success'])
		self.assertIn('access', response.data['data']['tokens'])
		self.assertEqual(response.data['data']['user']['email'], 'john@example.com')

	def test_profile_requires_authentication(self):
		response = self.client.get(reverse('profile'))

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Create your tests here.
