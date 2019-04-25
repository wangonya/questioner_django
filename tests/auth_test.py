from rest_framework.views import status

from tests import BaseTestCase


class TestAuth(BaseTestCase):
	def test_register_user(self):
		data = {
			"user":
				{
					"email": "test2@mail.com",
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

	def test_login(self):
		data = {
			"user":
				{
					"username": "test user",
					"password": "testpass"
					}
			}
		res = self.client.post(self.login_path, data, format='json')

		assert res.status_code == status.HTTP_200_OK
		assert "successful" in res.data['data'][0]['message']

	def test_login_fail(self):
		data = {
			"user":
				{
					"username": "wronguser",
					"password": "password"
					}
			}
		res = self.client.post(self.login_path, data, format='json')

		assert res.status_code == status.HTTP_401_UNAUTHORIZED
		assert "Invalid" in res.data['data'][0]['error']

	def test_forgot_password(self):
		data = {
			"user":
				{
					"email": "test@mail.com",
					}
			}
		with self.settings(
				EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
				):
			res = self.client.post(self.forgot_password_path, data, format='json')

			assert res.status_code == status.HTTP_200_OK
			assert "link sent" in res.data['data'][0]['message']

	def test_forgot_password_invalid(self):
		data = {
			"user":
				{
					"email": "non-existent@mail.com",
					}
			}
		res = self.client.post(self.forgot_password_path, data, format='json')

		assert res.status_code == status.HTTP_400_BAD_REQUEST
		assert "No account with that email" in res.data['data'][0]['error']

	def test_reset_password(self):
		data = {
			"user":
				{
					"password": "newtestpass",
					}
			}
		res = self.client.patch(self.reset_password_path, data,
		                       format='json')

		assert res.status_code == status.HTTP_200_OK
		assert "reset successful" in res.data['data'][0]['message']

	def test_reset_password_invalid(self):
		data = {
			"user":
				{
					"password": "newtestpass",
					}
			}
		res = self.client.patch('/auth/reset/token=wrong.token123/', data,
		                       format='json')

		assert res.status_code == status.HTTP_401_UNAUTHORIZED
