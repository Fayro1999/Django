from django.http import JsonResponse
from stores.models import StoreDetails
from products.models import Product
from django.db.models import Q
from stores.serializers import StoreDetailsSerializer  # Importing from the stores app
from products.serializers import ProductSerializer  # Importing from the products app


# API to search stores and products
def search_all(request):
    query = request.GET.get('q', '')

    # Search stores by name, address, city, state
    store_results = StoreDetails.objects.filter(
        Q(store_name__icontains=query) |
        Q(store_address__icontains=query) |
        Q(city__icontains=query) |
        Q(state__icontains=query)
    )

    # Search products by name, description, or store name
    product_results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(store__store_name__icontains=query)
    )

    # Serialize data
    store_data = [{'store_name': store.store_name, 'store_address': store.store_address} for store in store_results]
    product_data = [{'product_name': product.name, 'store_name': product.store.store_name, 'description': product.description} for product in product_results]

    return JsonResponse({
        'stores': store_data,
        'products': product_data,
    })
