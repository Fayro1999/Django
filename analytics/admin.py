from django.contrib import admin
from .models import StoreVisitor, StoreOrder, StoreRevenue, StoreCart, VisitorPurchase

admin.site.register(StoreVisitor)
admin.site.register(StoreOrder)
admin.site.register(StoreRevenue)
admin.site.register(StoreCart)
admin.site.register(VisitorPurchase)
