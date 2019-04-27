from django.db import models
from django.contrib.postgres.fields import ArrayField


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