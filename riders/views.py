from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DispatchRiderSerializer #LoginSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import login
from .models import DispatchRider
from orders.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import DispatchRider
from .serializers import DispatchRiderSerializer

User = get_user_model()

class RegisterDispatchRiderView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request, *args, **kwargs):
        # Extract user data from the request
        user_data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),  # Ensure password is included
            'first_name': request.data.get('first_name'),  # Include any other fields you need
            'last_name': request.data.get('last_name'),
            'username': request.data.get('email'),  # Setting username to email
        }

        # Extract dispatch rider data from the request
        rider_data = {
            'phone': request.data.get('phone'),
            'company': request.data.get('company'),
            'location': request.data.get('location'),
        }

        # Create a new user
        try:
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                username=user_data['username'] 
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create the DispatchRider instance
        dispatch_rider_data = {
            'user': user,  # Associate the created user
            **rider_data  # Add rider data
        }

        # Use a serializer to save the DispatchRider
        serializer = DispatchRiderSerializer(data=dispatch_rider_data)
        if serializer.is_valid():
            serializer.save()  # Save the dispatch rider
            return Response({"message": "Dispatch rider registered successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginDispatchRiderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "This account is inactive."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)


class ListDispatchRidersView(APIView):
    permission_classes = [AllowAny, IsAdminUser]  # Only admin users can list dispatch riders

    def get(self, request, *args, **kwargs):
        riders = DispatchRider.objects.all()
        serializer = DispatchRiderSerializer(riders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RiderResponseView(APIView):
     #permission_classes = [AllowAny, IsAdminUser] 
    def post(self, request, *args, **kwargs):
        rider = request.user
        order_id = request.data.get('order_id')
        response = request.data.get('response')  # Either 'accept' or 'decline'
        
        # Get the order
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if response == 'accept':
            # Assign the order to the rider
            order.assigned_rider = rider
            order.status = 'pending'  # Change status to 'pending'
            order.save()
            return Response({"message": "Delivery accepted successfully."}, status=status.HTTP_200_OK)

        elif response == 'decline':
            return Response({"message": "Delivery declined."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid response."}, status=status.HTTP_400_BAD_REQUEST)
