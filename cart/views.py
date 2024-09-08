from analytics.models import StoreCart
from cart.models import Cart
from products.models import Product
from django.utils import timezone

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
