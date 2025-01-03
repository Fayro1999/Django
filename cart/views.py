from analytics.models import StoreCart
from cart.models import Cart
from products.models import Product
from django.utils import timezone
from rest_framework.decorators import api_view

def add_to_cart(request, store_id, product_id):
    product = Product.objects.get(id=product_id)
    quantity = request.POST.get('quantity', 1)  # Default quantity to 1 if not provided
    amount = product.price * int(quantity)  # Calculate the amount

    # Logic for adding to cart
    cart_item, created = Cart.objects.update_or_create(
        user=request.user.storeuserprofile,  # Assuming the user has a related StoreUserProfile
        product=product,
        defaults={'quantity': quantity, 'amount': amount}
    )

    # Update analytics for cart
    StoreCart.objects.update_or_create(
        store_id=store_id,
        cart_date=timezone.now().date(),
        defaults={'cart_count': models.F('cart_count') + 1}
    )


@api_view(['GET'])
#@permission_classes([AllowAny])  # Ensure user authenticatio
def get_cart(request):
    # Fetch cart items for the logged-in user
    cart_items = Cart.objects.filter(user=request.user.storeuserprofile)

    # Serialize the data
    serializer = CartSerializer(cart_items, many=True)

    # Return the response
    return Response(serializer.data)