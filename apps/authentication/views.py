from django.contrib.auth import get_user_model
from rest_framework import (
	views, response, permissions, status
	)
from rest_framework_jwt.settings import api_settings

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
		res = {
				"status": status.HTTP_201_CREATED,
				"data": [{
					"message": "Signup successful",
					"email": user.email,
					"username": user.username,
					"token": token
					}]
			}
		return response.Response(res)
