from django.urls import path

from .views import (CreateMeetupView, UpcomingMeetupsView,
                    SpecificMeetupView, AskQuestionView,
                    GetMeetupQuestionsView, VoteView,
                    SpecificQuestionView, AnswerQuestionView,
                    GetQuestionAnswersView)

urlpatterns = [
	path('', CreateMeetupView.as_view(), name='create'),
	path('upcoming/', UpcomingMeetupsView.as_view(), name='upcoming'),
	path('<pk>', SpecificMeetupView.as_view(), name='specific'),
	path('<pk>/questions/ask/', AskQuestionView.as_view(),
	     name='ask-questions'),
	path('<for_meetup_id>/questions/get/', GetMeetupQuestionsView.as_view(),
	     name='get-questions'),
	path('questions/<pk>/', SpecificQuestionView.as_view(), name='question'),
	path('questions/<pk>/vote/', VoteView.as_view(), name='vote'),
	path('questions/<pk>/answer/', AnswerQuestionView.as_view(), name='answer'),
	path('questions/<for_question_id>/answers/', GetQuestionAnswersView.as_view(), name='answers'),
	]
