from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.responses.api_response import ApiResponse

from .serializers import (
	ChangePasswordSerializer,
	LoginSerializer,
	LogoutSerializer,
	RegisterSerializer,
	UserSerializer,
)
from .services import AuthService


class RegisterView(GenericAPIView):
	serializer_class = RegisterSerializer
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		data = {
			'user': UserSerializer(user).data,
			'tokens': AuthService.build_tokens_for_user(user),
		}
		return ApiResponse.success(data, 'Registration successful.', status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
	serializer_class = LoginSerializer
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		data = {
			'user': UserSerializer(user).data,
			'tokens': AuthService.build_tokens_for_user(user),
		}
		return ApiResponse.success(data, 'Login successful.')


class ProfileView(GenericAPIView):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return ApiResponse.success(UserSerializer(request.user).data, 'Profile fetched successfully.')


class ChangePasswordView(GenericAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.get_serializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return ApiResponse.success(None, 'Password changed successfully.')


class LogoutView(GenericAPIView):
	serializer_class = LogoutSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		AuthService.blacklist_refresh_token(serializer.validated_data['refresh'])
		return ApiResponse.success(None, 'Logout successful.')

# Create your views here.
