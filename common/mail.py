import os

from django.core.mail import send_mail


class Mail:
	@staticmethod
	def send_verification_mail(email, token):
		send_mail(
			'Verify Account',
			'Welcome to Questioner. Please click on the link below to '
			'verify your account. \n'
			'{}auth/verify/&token={}'.format(os.getenv('BASE_URL'), token),
			'{}'.format(os.getenv('EMAIL_HOST_USER')),
			[email],
			fail_silently=False,
			)

	@staticmethod
	def send_reset_password_mail(email, token):
		send_mail(
			'Reset Password',
			'Please click on the link below to '
			'reset your password. \n'
			'{}auth/reset/&token={}'.format(os.getenv('BASE_URL'), token),
			'{}'.format(os.getenv('EMAIL_HOST_USER')),
			[email],
			fail_silently=False,
			)