from django.urls import path

from .views import (CreateMeetupView, UpcomingMeetupsView,
                    SpecificMeetupView, AskQuestionView,
                    GetMeetupQuestionsView)

urlpatterns = [
	path('', CreateMeetupView.as_view(), name='create'),
	path('upcoming/', UpcomingMeetupsView.as_view(), name='upcoming'),
	path('<pk>', SpecificMeetupView.as_view(), name='specific'),
	path('<pk>/questions/ask/', AskQuestionView.as_view(),
	     name='ask-questions'),
	path('<for_meetup_id>/questions/get/', GetMeetupQuestionsView.as_view(),
	     name='get-questions'),
	]
