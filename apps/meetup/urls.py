from django.urls import path

from .views import (CreateMeetupView, UpcomingMeetupsView,
                    SpecificMeetupView)

urlpatterns = [
	path('', CreateMeetupView.as_view(), name='create'),
	path('upcoming/', UpcomingMeetupsView.as_view(), name='upcoming'),
	path('<pk>', SpecificMeetupView.as_view(), name='specific'),
	]
