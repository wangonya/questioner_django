from django.urls import path

from .views import (SignupView, VerifyAccountView, LoginView,
                    ForgotPasswordView, ResetPasswordView)

urlpatterns = [
	path('signup/', SignupView.as_view(), name='signup'),
	path('verify/<token>/', VerifyAccountView.as_view(), name='verify'),
	path('login/', LoginView.as_view(), name='login'),
	path('forgot/', ForgotPasswordView.as_view(), name='forgot'),
	path('reset/<token>/', ResetPasswordView.as_view(), name='reset'),
	]
