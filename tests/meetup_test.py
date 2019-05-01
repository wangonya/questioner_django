import cloudinary

from rest_framework.views import status

from tests import BaseTestCase


class TestMeetup(BaseTestCase):
	def test_creator_is_admin(self):
		res = self.client.post(self.create_meetup_path, {},
		                       HTTP_AUTHORIZATION=self.auth, format='json')

		assert res.status_code == status.HTTP_401_UNAUTHORIZED
		assert "restricted to admins" in res.data['error']

	def test_meetups(self):
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
		meetup_id = res.data['data'][0]['id']

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

		res = self.client.get(self.upcoming_meetups_path)
		assert res.status_code == status.HTTP_200_OK

		res = self.client.get('/meetups/{}'.format(meetup_id))
		assert res.status_code == status.HTTP_200_OK

		question = {
					"question": {
						"question": "test question body"
					}
				}

		res = self.client.post('/meetups/{}/questions/ask/'.format(
			meetup_id), question, HTTP_AUTHORIZATION=self.auth, format='json')
		question_id = res.data['data'][0]['id']
		assert res.status_code == status.HTTP_201_CREATED

		res = self.client.get('/meetups/{}/questions/get/'.format(
			meetup_id))
		assert res.status_code == status.HTTP_200_OK

		res = self.client.post('/meetups/00/questions/ask/', question,
		                       HTTP_AUTHORIZATION=self.auth, format='json')
		assert res.status_code == status.HTTP_404_NOT_FOUND

		vote = {
				  "vote": {"vote": -1}
				}

		res = self.client.post('/meetups/questions/{}/vote/'.format(
			question_id), vote, HTTP_AUTHORIZATION=self.auth,
			format='json')
		assert res.status_code == status.HTTP_201_CREATED

		res = self.client.post('/meetups/questions/{}/vote/'.format(
			question_id), vote, HTTP_AUTHORIZATION=self.auth,
			format='json')
		assert res.status_code == status.HTTP_200_OK

		res = self.client.get('/meetups/questions/{}/'.format(question_id))
		assert res.status_code == status.HTTP_200_OK

		res = self.client.post('/meetups/questions/00/vote/', vote,
		                       HTTP_AUTHORIZATION=self.auth, format='json')
		assert res.status_code == status.HTTP_404_NOT_FOUND

		answer = {
			"answer": {"answer": -1}
		}

		res = self.client.post('/meetups/questions/{}/answer/'.format(
			question_id), answer, HTTP_AUTHORIZATION=self.auth,
			format='json')
		assert res.status_code == status.HTTP_201_CREATED

		res = self.client.post('/meetups/questions/00/answer/',
		                       answer, HTTP_AUTHORIZATION=self.auth, format='json')
		assert res.status_code == status.HTTP_404_NOT_FOUND

		res = self.client.get('/meetups/questions/{}/answers/'.format(question_id))
		assert res.status_code == status.HTTP_200_OK
