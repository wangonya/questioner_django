import django
import jwt

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework_jwt import utils
from django.contrib.auth import get_user_model
from django.conf import settings

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
		self.auth = 'JWT {0}'.format(self.token)

		self.test_super_user = User.objects.create_superuser('super user',
		                                                     'super@mail.com',
		                                                     'supertestpass')
		self.superpayload = utils.jwt_payload_handler(self.test_super_user)
		self.supertoken = utils.jwt_encode_handler(self.superpayload)
		self.super_auth = 'JWT {0}'.format(self.supertoken)

		self.reset_password_token = jwt.encode({
				'email': 'test@mail.com',
				'type': 'reset password',
				}, settings.SECRET_KEY).decode('utf-8')

		self.signup_path = reverse('authentication:signup')
		self.verify_path = reverse('authentication:verify', kwargs={
			'token': 'token={}'.format(self.token)
			})
		self.login_path = reverse('authentication:login')
		self.forgot_password_path = reverse('authentication:forgot')
		self.reset_password_path = reverse('authentication:reset', kwargs={
			'token': 'token={}'.format(self.reset_password_token)
			})

		self.create_meetup_path = reverse('meetup:create')
