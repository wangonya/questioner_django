from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=255, required=True)
	password = serializers.CharField(max_length=128, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
	password = serializers.CharField(max_length=200, required=True)
