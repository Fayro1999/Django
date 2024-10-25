from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DispatchRiderSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import login
from .models import DispatchRider
from orders.models import Order
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate





class RegisterDispatchRiderView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request, *args, **kwargs):
        serializer = DispatchRiderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dispatch rider registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginDispatchRiderView(APIView):
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
