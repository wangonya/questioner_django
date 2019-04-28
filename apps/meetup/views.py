import cloudinary
import imghdr

from pathlib import Path
from rest_framework import (
	views, response, permissions, status,
	generics,
	)
from django.template.defaultfilters import slugify

from .serializers import (MeetupSerializer, QuestionSerializer)
from .models import (MeetupModel, QuestionModel)


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


class UpcomingMeetupsView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = MeetupSerializer
	queryset = MeetupModel.objects.all()


class SpecificMeetupView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = MeetupSerializer
	queryset = MeetupModel.objects.all()

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

# TODO: ADD FILTERING BY TAG


class AskQuestionView(views.APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = QuestionSerializer

	def post(self, request, pk):
		question_data = request.data.get('question', {})
		question_data['asked_by'] = request.user.id
		try:
			question_data['for_meetup'] = MeetupModel.objects.get(pk=pk).id
		except MeetupModel.DoesNotExist:
			return response.Response({"error": "no meetup with id {}"
			                         .format(pk)},
			                         status=status.HTTP_404_NOT_FOUND)
		serializer = self.serializer_class(data=question_data)
		serializer.is_valid(raise_exception=True)

		serializer.save()
		res = {
			"status": status.HTTP_201_CREATED,
			"data": [serializer.data]
			}
		return response.Response(res, status.HTTP_201_CREATED)


class GetMeetupQuestionsView(generics.ListAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = QuestionSerializer
	queryset = QuestionModel.objects.all()
	lookup_field = 'for_meetup_id'

	def get(self, request, *args, **kwargs):
		self.queryset = QuestionModel.objects.filter(
			for_meetup_id=kwargs['for_meetup_id'])
		return self.list(request, *args, **kwargs)
