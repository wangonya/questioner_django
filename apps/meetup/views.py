import cloudinary
import imghdr

from pathlib import Path
from rest_framework import (
	views, response, permissions, status
	)
from django.template.defaultfilters import slugify

from .serializers import (MeetupSerializer, )


class CreateMeetupView(views.APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = MeetupSerializer

	def post(self, request):
		if not request.user.is_superuser:
			res = {
				"status": status.HTTP_401_UNAUTHORIZED,
				"error": "restricted to admins"
				}
			return response.Response(res, status.HTTP_401_UNAUTHORIZED)

		meetup_data = request.data.get('meetup', {})
		try:
			image_path = Path(meetup_data['image'])
			if image_path.is_file() and imghdr.what(meetup_data['image']):
				res = cloudinary.uploader.unsigned_upload(
					meetup_data['image'], 'dvyip3rs',
					public_id=slugify(meetup_data['title']))
				meetup_data['image'] = res['url']
			else:
				return response.Response({"error": "image not found"},
				                         status=status.HTTP_400_BAD_REQUEST)
		except KeyError:
			pass
		serializer = self.serializer_class(data=meetup_data)
		serializer.is_valid(raise_exception=True)

		serializer.save()
		res = {
			"status": status.HTTP_201_CREATED,
			"data": [serializer.data]
			}
		return response.Response(res, status.HTTP_201_CREATED)
