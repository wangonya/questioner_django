import cloudinary

from rest_framework.views import status

from tests import BaseTestCase


class TestMeetup(BaseTestCase):
	def test_creator_is_admin(self):
		res = self.client.post(self.create_meetup_path, {},
		                       HTTP_AUTHORIZATION=self.auth, format='json')

		assert res.status_code == status.HTTP_401_UNAUTHORIZED
		assert "restricted to admins" in res.data['error']

	def test_create_meetup(self):
		data = {
			"meetup": {
				"title": "dsfsmmmf",
				"details": "meetup details",
				"location": "fdsfdsfd",
				"happening_on": "2019-02-02",
				"image": "andela.png",
				"tags": ["ds"]
			}
		}

		data2 = {
			"meetup": {
				"title": "dsfsmmmf",
				"details": "meetup details",
				"location": "fdsfdsfd",
				"happening_on": "2019-02-02",
				"image": "TX0AAlwxk.jpeg",
				"tags": ["ds"]
				}
			}

		data3 = {
			"meetup": {
				"title": "dsfsmmmf",
				"details": "meetup details",
				"location": "fdsfdsfd",
				"happening_on": "2019-02-02",
				"tags": ["ds"]
				}
			}

		res = self.client.post(self.create_meetup_path, data,
		                       HTTP_AUTHORIZATION=self.super_auth,
		                       format='json')

		assert res.status_code == status.HTTP_201_CREATED
		cloudinary.uploader.destroy('ah-django/dsfsmmmf')

		res = self.client.post(self.create_meetup_path, data2,
		                       HTTP_AUTHORIZATION=self.super_auth,
		                       format='json')

		assert res.status_code == status.HTTP_400_BAD_REQUEST

		res = self.client.post(self.create_meetup_path, data3,
		                       HTTP_AUTHORIZATION=self.super_auth,
		                       format='json')

		assert res.status_code == status.HTTP_201_CREATED

	def test_get_meetups(self):
		res = self.client.get(self.upcoming_meetups_path)
		assert res.status_code == status.HTTP_200_OK

		res = self.client.get(self.specific_meetup_path)
		assert res.status_code == status.HTTP_200_OK