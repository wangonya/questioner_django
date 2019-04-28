from rest_framework import serializers
from .models import MeetupModel, QuestionModel


class MeetupSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeetupModel
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionModel
		fields = '__all__'
