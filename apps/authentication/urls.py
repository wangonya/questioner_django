from django.urls import path

from .views import SignupView, VerifyAccount

urlpatterns = [
	path('signup/', SignupView.as_view(), name='signup'),
	path('verify/<token>/', VerifyAccount.as_view(), name='verify')
	]
