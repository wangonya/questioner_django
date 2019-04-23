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
