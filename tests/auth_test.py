from rest_framework.views import status

from tests import BaseTestCase


class TestAuth(BaseTestCase):
	def test_register_user(self):
		data = {
			"user":
				{
					"email": "test@mail.com",
					"username": "testuser",
					"password": "password"
					}
			}

		with self.settings(
				EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
				):
			res = self.client.post(self.signup_path, data, format='json')
			res_data = {
				"status": status.HTTP_201_CREATED,
				"data": [{
					"message": "Signup successful",
					"email": res.data['data'][0]['email'],
					"username": res.data['data'][0]['username'],
					"token": res.data['data'][0]['token']
					}]
				}

			assert res.status_code == status.HTTP_201_CREATED
			assert res.data == res_data

	def test_verify_account(self):
		res = self.client.get(self.verify_path)

		assert res.status_code == status.HTTP_200_OK
		assert "verification successful" in res.data['data'][0]['message']
		assert res.data['data'][0]['verified']

	def test_verify_account_fail(self):
		res = self.client.get('/auth/verify/&token=invalidtoken3743/')

		assert res.status_code == status.HTTP_400_BAD_REQUEST
