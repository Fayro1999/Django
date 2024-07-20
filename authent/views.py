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
import logging

logger = logging.getLogger(__name__)
token_generator = TokenGenerator()

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

            user = None  # Initialize user to None
            # Use transaction.atomic to ensure database integrity
            try:
                with transaction.atomic():
                    user = serializer.save()
                    user.is_active = False  # Ensure the user is inactive until email verification
                    user.save()

                    # Send verification email
                    code = token_generator.make_token(user)
                    
                    send_mail(
                        'Email Verification',
                        f'Your verification code is {code}. It will expire in 10 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    cache.set(f'verify_{user.email}', {'email': user.email, 'code': code}, timeout=600)  # Store for 10 minutes
                    
                    return Response({'detail': 'Verification email sent.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f'Failed to register user: {e}')
                # Rollback user creation if any exception occurs
                if user:
                    user.delete()
                return Response({'error': 'Failed to register user. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.debug('Request data: %s', request.data)
        code = request.data.get('code')
        email = cache.get(f'verify_{user.email}')  # Retrieve the email from the request

        logger.debug('Retrieved code: %s, email: %s', code, email)

        if not code or not email:
            logger.error('Code or email missing in request.')
            return Response({"error": "Invalid request. Code and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the stored data from the cache
        cached_data = cache.get(f'verify_{email}')

        if cached_data is None or cached_data['code'] != code:
            logger.error('Invalid or expired code.')
            return Response({"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.verification_code = None  # Clear the verification code
            user.verification_code_expiration = None  # Clear the expiration time
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "This account is inactive."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)


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
