from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from orders.models import Order
from orders.serializers import OrderSerializer,  OrderAuthenticationSerializer
from cart.models import Cart 
from stores.models import StoreDetails
from .tasks import send_order_notification  # Task that sends notifications

class CreateOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user

        # Fetch the cart items for this user
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total amount and quantity
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)

        # Assuming all products belong to the same store, get the store from the first cart item
        store = cart_items.first().product.store  # Adjust according to your product-store relationship

        # Create the order with calculated amount and quantity
        order = Order.objects.create(
            user=user,
            store=store,
            quantity=total_quantity,
            amount=total_amount,
            status='received'  # Set the initial status
        )

        # Add the products from the cart to the order
        for item in cart_items:
            order.products.add(item.product)

        # Clear the cart after placing the order
        cart_items.delete()

        # Serialize the order
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AssignDeliveryView(APIView):
    def post(self, request, order_id):
        try:
            # Retrieve the order
            order = Order.objects.get(id=order_id)

            # Assuming the delivery location is based on the store's location or delivery address
            location = order.store.city  # Adjust if using delivery.receiver_address

            # Send notifications to riders in that location
            send_order_notification(order, location)

            return Response({'message': 'Delivery assigned and notification sent'}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)




class OrderAuthenticationView(APIView):
    def post(self, request):
        serializer = OrderAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.authenticate_order()
            return Response({
                "message": f"Order {order.order_id} for {order.user.get_full_name()} authenticated successfully.",
                "order_status": order.status,
                "amount": order.amount
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

