import django

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

django.setup()
User = get_user_model()


class BaseTestCase(APITestCase):
	def setUp(self):
		self.client = APIClient()
		self.test_user = User.objects.create_user('test user')

		self.signup_path = reverse('authentication:signup')