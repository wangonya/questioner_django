from rest_framework import serializers
from .models import MeetupModel, QuestionModel, VotesModel


class MeetupSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeetupModel
		fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	upvotes = serializers.SerializerMethodField()
	downvotes = serializers.SerializerMethodField()
	class Meta:
		model = QuestionModel
		fields = '__all__'

	def get_upvotes(self, inst):
		upvote_queryset = VotesModel.objects.filter(for_question=inst, vote=1)
		return upvote_queryset.count()

	def get_downvotes(self, inst):
		downvote_queryset = VotesModel.objects.filter(for_question=inst, vote=-1)
		return downvote_queryset.count()


class VotesSerializer(serializers.ModelSerializer):
	class Meta:
		model = VotesModel
		fields = '__all__'
