from django.http import JsonResponse
from stores.models import StoreDetails
from products.models import Product
from django.db.models import Q
from stores.serializers import StoreDetailsSerializer
from products.serializers import ProductSerializer

def search_all(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'stores': [], 'products': []}, status=200)

    # Search stores
    store_results = StoreDetails.objects.filter(
        Q(store_name__icontains=query) |
        Q(store_address__icontains=query) |
        Q(city__icontains=query) |
        Q(state__icontains=query)
    )

    # Search products (Change store__store_name to vendor__store_name)
    product_results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(vendor__store_name__icontains=query)  # Fix: Change store to vendor
    ).select_related('vendor')  # Optimize DB queries

    # Serialize data
    store_data = StoreDetailsSerializer(store_results, many=True).data
    product_data = ProductSerializer(product_results, many=True).data

    return JsonResponse({'stores': store_data, 'products': product_data})
