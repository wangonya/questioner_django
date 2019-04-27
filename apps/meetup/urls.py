from django.urls import path

from .views import (CreateMeetupView)

urlpatterns = [
	path('', CreateMeetupView.as_view(), name='create'),
	]
