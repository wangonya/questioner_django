from rest_framework import serializers
from .models import MeetupModel


class MeetupSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeetupModel
		fields = '__all__'
