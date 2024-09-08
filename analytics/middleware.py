# analytics/middleware.py

from django.utils.deprecation import MiddlewareMixin
from analytics.models import StoreVisitor
from django.utils import timezone
from django.db.models import F
from django.shortcuts import get_object_or_404

class VisitorTrackingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        store_id = view_kwargs.get('store_id')
        if store_id:
            today = timezone.now().date()
            
            # Check if a StoreVisitor entry already exists for today
            try:
                store_visitor = StoreVisitor.objects.get(store_id=store_id, visit_date=today)
                store_visitor.visitor_count = F('visitor_count') + 1
                store_visitor.save()
            except StoreVisitor.DoesNotExist:
                # Create a new entry if it doesn't exist
                StoreVisitor.objects.create(
                    store_id=store_id,
                    visit_date=today,
                    visitor_count=1
                )

