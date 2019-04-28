from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericRelation

from apps.authentication.models import User


class MeetupModel(models.Model):
	title = models.CharField(max_length=100, null=False, blank=False)
	details = models.TextField(null=False, blank=False)
	location = models.CharField(max_length=100, null=False, blank=False)
	happening_on = models.DateField(null=False, blank=False)
	image = models.URLField(null=True, blank=True)
	tags = ArrayField(
		models.CharField(max_length=100), blank=True, null=True
	)

	class Meta:
		ordering = ["happening_on"]


class QuestionModel(models.Model):
	question = models.TextField(null=False, blank=False)
	asked_on = models.DateTimeField(auto_now_add=True)
	asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
	for_meetup = models.ForeignKey(MeetupModel, on_delete=models.CASCADE)
	votes = GenericRelation('VotesModel', related_query_name='question')

	class Meta:
		ordering = ["asked_on"]


class VotesModel(models.Model):
	pass
