import django

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_jwt import utils
from django.contrib.auth import get_user_model

django.setup()
User = get_user_model()


class BaseTestCase(APITestCase):
	def setUp(self):
		self.client = APIClient()
		self.test_user = User.objects.create_user('test user',
		                                          'test@mail.com',
		                                          'testpass')
		self.payload = utils.jwt_payload_handler(self.test_user)
		self.token = utils.jwt_encode_handler(self.payload)

		self.signup_path = reverse('authentication:signup')
		self.verify_path = reverse('authentication:verify', kwargs={
			'token': 'token={}'.format(self.token)
			})
		self.login_path = reverse('authentication:login')
