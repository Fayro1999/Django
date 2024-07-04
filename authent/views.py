from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import CustomUser
from .serializers import UserSerializer
from .token_generator import TokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
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
                    token_generator = TokenGenerator(settings.SECRET_KEY)
                    token = token_generator.make_token(user)
                    verification_url = f"{request.build_absolute_uri(reverse('verify-email'))}?token={token}&email={user.email}"
                    
                    send_mail(
                        'Email Verification',
                        f'Click the link to verify your email: {verification_url}',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    
                    return Response({'detail': 'Verification email sent.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f'Failed to register user: {e}')
                # Rollback user creation if any exception occurs
                if user:
                    user.delete()
                return Response({'error': 'Failed to register user. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        email = request.query_params.get('email')

        if not token or not email:
            return Response({"error": "Invalid request. Token and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, email=email)
        token_generator = TokenGenerator(settings.SECRET_KEY)
        
        if token_generator.validate_token(token, user):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)