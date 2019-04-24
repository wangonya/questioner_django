from django.contrib.auth import get_user_model
from rest_framework import (
	views, response, permissions, status
	)
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import ValidationError

from common.mail import Mail

from .serializers import SignupSerializer

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


class VerifyAccount(views.APIView):

	permission_classes = (permissions.AllowAny,)

	def get(self, request, *args, **kwargs):
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
