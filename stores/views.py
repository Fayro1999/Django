from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from stores.models import StoreUserProfile
from .models import StoreDetails
from .serializers import StoreDetailsSerializer
from authent.models import CustomUser
from stores.serializers import StoreSerializer #SetPasswordSerializer
from authent.serializers import UserSerializer
from authent.token_generator import TokenGenerator
from products.models import Product
from products.serializers import ProductSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
token_generator = TokenGenerator()
CustomUser = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Endpoint hit")
        
        # Extract user data from request
        user_data = request.data.get('user')
        
        # Prepare store data without phone since it's part of the CustomUser model
        store_data = {
            'groups': request.data.get('groups', []),
            'user_permissions': request.data.get('user_permissions', [])
        }

        # Initialize serializers with the provided data
        user_serializer = UserSerializer(data=user_data)

        # Print to check data being passed
        print("User data:", user_data)
        print("Store data:", store_data)

        # Check if user serializer is valid
        if user_serializer.is_valid():
            email = user_serializer.validated_data.get('email')

            if CustomUser.objects.filter(email=email).exists():
                return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            user = None
            try:
                with transaction.atomic():
                    user = user_serializer.save()
                    user.is_active = False  # Mark the user as inactive until email verification
                    user.save()

                    # Create the store user profile
                    store_profile = StoreUserProfile.objects.create(
                        user=user
                    )

                    # Now set the many-to-many fields using set()
                    store_profile.groups.set(store_data['groups'])
                    store_profile.user_permissions.set(store_data['user_permissions'])

                    # Generate and send verification email
                    code = token_generator.make_token(user)

                    send_mail(
                        'Email Verification',
                        f'Your verification code is {code}. It will expire in 10 minutes.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    # Store the verification code in cache
                
                    cache.set(f'stores_verify_{code}', {'email': user.email, 'code': code}, timeout=600)

                    return Response({'detail': 'Verification email sent.'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f'Failed to register user: {e}')
                if user:
                    user.delete()  # Rollback user creation if any exception occurs
                return Response({'error': 'Failed to register user. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If user serializer is invalid, return its errors
        return Response({'user': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')

        if not code:
            logger.error('Code missing in request.')
            return Response({"error": "Invalid request. Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_data = cache.get(f'stores_verify_{code}')

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
            user = StoreUserProfile.objects.get(email=email)
        except StoreUserProfile.DoesNotExist:
            logger.error('User not found for email: %s', email)
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)


class ResendCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = StoreUserProfile.objects.get(email=email)
            if user.is_active:
                return Response({"error": "This account is already verified."}, status=status.HTTP_400_BAD_REQUEST)

            code = token_generator.make_token(user)
            send_mail(
                'Email Verification',
                f'Your verification code is {code}. It will expire in 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            cache.set(f'verify_{user.email}', {'email': user.email, 'code': code}, timeout=600)

            return Response({'detail': 'Verification code resent.'}, status=status.HTTP_200_OK)

        except StoreUserProfile.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)



class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(password)
        user.save()

        return Response({"message": "Password set successfully."}, status=status.HTTP_200_OK)


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




class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user =StoreUserProfile.objects.get(email=email)
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

        except StoreUserProfile.DoesNotExist:
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
            user = StoreUserProfile.objects.get(email=email)
            user.set_password(password)
            user.save()
            cache.delete(f'reset_{token}')  # Delete the token after successful reset
            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)
        
        except StoreUserProfile.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)





class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = StoreUserProfile.objects.all()
        serializer =StoreSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReferenceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a reference GET request for your API."}, status=status.HTTP_200_OK)



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import StoreUserProfile, StoreDetails
from .serializers import StoreDetailsSerializer
from products.models import Product
from products.serializers import ProductSerializer

class StoreDetailsView(APIView):
    def get(self, request, *args, **kwargs):
        # Get store by primary key (pk) provided in URL
        store_id = kwargs.get('pk')
        try:
            store = StoreDetails.objects.get(pk=store_id)
        except StoreDetails.DoesNotExist:
            return Response({'error': 'Store not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize store details
        store_data = StoreDetailsSerializer(store).data
        
        # Fetch products associated with this store
        products = Product.objects.filter(vendor=store)
        products_data = ProductSerializer(products, many=True).data
        
        # Combine store details and products
        store_data['products'] = products_data
        
        return Response(store_data)
    
    def post(self, request, *args, **kwargs):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Retrieve the StoreUserProfile for the authenticated user
            store_user_profile = StoreUserProfile.objects.get(user=request.user)
        except StoreUserProfile.DoesNotExist:
            return Response({'error': 'Store user profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Include store_user_profile ID in the incoming data
        data = request.data.copy()
        data['store_user_profile'] = store_user_profile.id

        # Serialize and validate the incoming data
        serializer = StoreDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Store details added successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateStoreProfileView(APIView):
    def put(self, request, store_id, *args, **kwargs):
        try:
            store = StoreDetails.objects.get(store_user_profile__id=store_id)
        except StoreDetails.DoesNotExist:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoreDetailsSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


