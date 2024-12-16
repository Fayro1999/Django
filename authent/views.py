from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import CustomUser
from .serializers import UserSerializer
from .token_generator import TokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
token_generator = TokenGenerator()
CustomUser = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            if CustomUser.objects.filter(username=username).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = None
            try:
                with transaction.atomic():
                    user = serializer.save()
                    user.is_active = False
                    user.save()

                    code = token_generator.make_token(user)
                    send_mail(
                        'Email Verification',
                        f'Your verification code is {code}. It will expire in 10 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    cache.set(f'verify_{code}', {'email': user.email, 'code': code}, timeout=600)

                    return Response({'detail': 'Verification email sent.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f'Failed to register user: {e}')
                if user:
                    user.delete()
                return Response({'error': 'Failed to register user. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')

        if not code:
            logger.error('Code missing in request.')
            return Response({"error": "Invalid request. Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the stored data from the cache
        cached_data = cache.get(f'verify_{code}')

        if not cached_data:
            logger.error('Verification data not found in cache.')
            return Response({"error": "Invalid or expired verification data"}, status=status.HTTP_400_BAD_REQUEST)

        email = cached_data.get('email')
        cached_code = cached_data.get('code')

        logger.debug('Retrieved code: %s, email: %s', cached_code, email)

        if cached_code != code:
            logger.error('Invalid or expired code.')
            return Response({"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            logger.error('User not found for email: %s', email)
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({"message": "Email verified successfully", "id": user.id, "token": token.key,}, status=status.HTTP_200_OK)




class ResendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            if user.is_active:
                return Response({"error": "This account is already verified."}, status=status.HTTP_400_BAD_REQUEST)

            # Send a new verification code
            code = token_generator.make_token(user)
            send_mail(
                'Email Verification',
                f'Your verification code is {code}. It will expire in 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            cache.set(f'verify_{user.email}', {'email': user.email, 'code': code}, timeout=600)  # Store for 10 minutes

            return Response({'detail': 'Verification code resent.'}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)






class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "id": user.id,
                "is_admin": user.is_admin}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "This account is inactive."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)




class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            token = get_random_string(50)  # Generate a random token
            cache.set(f'reset_{token}', email, timeout=600)  # Store the token with a 10-minute expiration
            reset_link = f'{settings.FRONTEND_URL}/reset-password/{token}'

            send_mail(
                'Password Reset Request',
                f'Use the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)




class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        email = cache.get(f'reset_{token}')
        if not email:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            cache.delete(f'reset_{token}')  # Delete the token after successful reset
            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)





class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReferenceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a reference GET request for your API."}, status=status.HTTP_200_OK)
