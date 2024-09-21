from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny 
from django.db.models import Sum
from .models import StoreVisitor, StoreOrder, StoreRevenue, StoreCart, VisitorPurchase
from .models import WebsiteVisitor, WebsiteOrder, WebsiteRevenue, WebsiteCart, WebsitePurchase
from .serializers import WebsiteVisitorSerializer, WebsiteOrderSerializer, WebsiteRevenueSerializer, WebsiteCartSerializer, WebsitePurchaseSerializer


class StoreStatisticsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, store_id):
        today = timezone.now().date()

        visitors = StoreVisitor.objects.filter(store_id=store_id, visit_date=today).count()
        orders = StoreOrder.objects.filter(store_id=store_id, order_date=today).count()
        revenue = StoreRevenue.objects.filter(store_id=store_id, revenue_date=today).aggregate(total_revenue=Sum('revenue'))['total_revenue'] or 0
        carts = StoreCart.objects.filter(store_id=store_id, cart_date=today).count()
        abandoned_carts = StoreCart.objects.filter(store_id=store_id, cart_date=today).aggregate(abandoned=Sum('abandoned_cart_count'))['abandoned'] or 0
        purchases = VisitorPurchase.objects.filter(store_id=store_id, purchase_date=today).count()

        return Response({
            "visitors": visitors,
            "orders": orders,
            "revenue": revenue,
            "carts": carts,
            "abandoned_carts": abandoned_carts,
            "purchases": purchases,
        })

    def post(self, request):
        store_id = request.data.get('store_id')
        visitors = request.data.get('visitors', 0)
        orders = request.data.get('orders', 0)
        revenue = request.data.get('revenue', 0.0)
        carts = request.data.get('carts', 0)
        abandoned_carts = request.data.get('abandoned_carts', 0)
        purchases = request.data.get('purchases', 0)

        today = timezone.now().date()

        # Handle StoreVisitor
        store_visitor, created = StoreVisitor.objects.get_or_create(store_id=store_id, visit_date=today)
        if created:
            store_visitor.visitor_count = visitors
        else:
            store_visitor.visitor_count += visitors
        store_visitor.save()

        # Handle StoreOrder
        store_order, created = StoreOrder.objects.get_or_create(store_id=store_id, order_date=today)
        if created:
            store_order.total_orders = orders
        else:
            store_order.total_orders += orders
        store_order.save()

        # Handle StoreRevenue
        store_revenue, created = StoreRevenue.objects.get_or_create(store_id=store_id, revenue_date=today)
        if created:
            store_revenue.revenue = revenue
        else:
            store_revenue.revenue += revenue
        store_revenue.save()

        # Handle StoreCart
        store_cart, created = StoreCart.objects.get_or_create(store_id=store_id, cart_date=today)
        if created:
            store_cart.cart_count = carts
            store_cart.abandoned_cart_count = abandoned_carts
        else:
            store_cart.cart_count += carts
            store_cart.abandoned_cart_count += abandoned_carts
        store_cart.save()

        # Handle VisitorPurchase
        visitor_purchase, created = VisitorPurchase.objects.get_or_create(store_id=store_id, purchase_date=today)
        if created:
            visitor_purchase.visitor_count = purchases
        else:
            visitor_purchase.visitor_count += purchases
        visitor_purchase.save()

        return Response({"message": "Statistics updated successfully"}, status=status.HTTP_200_OK)




# website analytics

class WebsiteAnalyticsView(APIView):
    def get(self, request, *args, **kwargs):
        # Aggregate data here
        total_visitors = WebsiteVisitor.objects.all().aggregate(total=Sum('visitor_count'))['total']
        total_orders = WebsiteOrder.objects.all().aggregate(total=Sum('total_orders'))['total']
        total_revenue = WebsiteRevenue.objects.all().aggregate(total=Sum('revenue'))['total']
        total_cart = WebsiteCart.objects.all().aggregate(total=Sum('cart_count'))['total']
        total_abandoned_cart = WebsiteCart.objects.all().aggregate(total=Sum('abandoned_cart_count'))['total']
        total_purchases = WebsitePurchase.objects.all().aggregate(total=Sum('visitor_count'))['total']

        data = {
            'total_visitors': total_visitors,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_cart': total_cart,
            'total_abandoned_cart': total_abandoned_cart,
            'total_purchases': total_purchases
        }
        return Response(data, status=status.HTTP_200_OK)
