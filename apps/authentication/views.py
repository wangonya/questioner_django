import jwt

from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from rest_framework import (
	views, response, permissions, status
	)
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from common.mail import Mail

from .serializers import (SignupSerializer, LoginSerializer,
                          ForgotPasswordSerializer,
                          ResetPasswordSerializer,)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()


class SignupView(views.APIView):

	serializer_class = SignupSerializer
	permission_classes = (permissions.AllowAny,)

	def post(self, request):
		signup_data = request.data.get('user', {})
		serializer = self.serializer_class(data=signup_data)
		serializer.is_valid(raise_exception=True)
		user = User.objects.create_user(
				signup_data['username'],
				signup_data['email'],
				signup_data['password']
			)
		user.save()
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)
		Mail.send_verification_mail(user.email, token)
		res = {
				"status": status.HTTP_201_CREATED,
				"data": [{
					"message": "Signup successful",
					"email": user.email,
					"username": user.username,
					"token": token
					}]
			}
		return response.Response(res, status.HTTP_201_CREATED)


class VerifyAccountView(views.APIView):

	permission_classes = (permissions.AllowAny,)

	@staticmethod
	def get(request, *args, **kwargs):
		url = request.META['PATH_INFO'] + request.META['QUERY_STRING']
		token = {'token': url.split('=')[1].rstrip('/')}
		try:
			valid_token = VerifyJSONWebTokenSerializer().validate(token)
			user = valid_token['user']

			if not user.is_verified:
				user.is_verified = True
				user.save()

			res = {
				"status": status.HTTP_200_OK,
				"data": [{
					"message": "Account verification successful",
					"email": user.email,
					"username": user.username,
					"verified": user.is_verified
					}]
				}
			return response.Response(res, status.HTTP_200_OK)
		except ValidationError:
			res = {
				"status": status.HTTP_400_BAD_REQUEST,
				"data": [{
					"error": "Account verification failed",
					}]
				}
			return response.Response(res, status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):

	permission_classes = (permissions.AllowAny,)
	serializer_class = LoginSerializer

	def post(self, request):
		login_data = request.data.get('user', {})
		serializer = self.serializer_class(data=login_data)
		serializer.is_valid(raise_exception=True)
		user = authenticate(
			username=login_data['username'],
			password=login_data['password']
			)

		if user:
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)
			res = {
				"status": status.HTTP_200_OK,
				"data": [{
					"message": "Login successful",
					"email": user.email,
					"username": user.username,
					"token": token
					}]
				}
			return response.Response(res, status.HTTP_200_OK)
		else:
			res = {
				"status": status.HTTP_401_UNAUTHORIZED,
				"data": [{
					"error": "Invalid login details"
					}]
				}
			return response.Response(res, status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordView(views.APIView):

	permission_classes = (permissions.AllowAny,)
	serializer_class = ForgotPasswordSerializer

	def post(self, request):
		forgot_data = request.data.get('user', {})
		serializer = self.serializer_class(data=forgot_data)
		serializer.is_valid(raise_exception=True)

		try:
			User.objects.get(email=forgot_data['email'])
			token = jwt.encode({
				'email': forgot_data['email'],
				'type': 'reset password',
				}, settings.SECRET_KEY).decode('utf-8')

			Mail.send_reset_password_mail(forgot_data['email'], token)

			res = {
				"status": status.HTTP_200_OK,
				"data": [{
					"message": "Reset link sent",
					}]
				}

			return response.Response(res, status.HTTP_200_OK)
		except User.DoesNotExist:
			res = {
				"status": status.HTTP_400_BAD_REQUEST,
				"data": [{
					"error": "No account with that email",
					}]
				}

			return response.Response(res, status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(views.APIView):

	permission_classes = (permissions.AllowAny,)
	serializer_class = ResetPasswordSerializer

	def patch(self, request, *args, **kwargs):
		url = request.META['PATH_INFO'] + request.META['QUERY_STRING']
		token = url.split('=')[1].rstrip('/')
		try:
			decoded_token = jwt.decode(token, settings.SECRET_KEY)
			user = User.objects.get(email=decoded_token['email'])

			reset_data = request.data.get('user', {})
			serializer = self.serializer_class(data=reset_data)
			serializer.is_valid(raise_exception=True)

			user.set_password(reset_data['password'])
			user.save()

			res = {
				"status": status.HTTP_200_OK,
				"data": [{
					"message": "Password reset successful",
					"email": user.email,
					"username": user.username,
					}]
				}
			return response.Response(res, status.HTTP_200_OK)
		except Exception as e:
			if e.__class__.__name__ == 'ExpiredSignatureError':
				raise AuthenticationFailed('Token has expired')
			elif e.__class__.__name__ == 'DecodeError':
				raise AuthenticationFailed(
					'Unable to decode the given token')
			else:
				raise AuthenticationFailed(str(e))
