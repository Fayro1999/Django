from rest_framework import viewsets
from .models import DeliveryDetail, DeliveryTime, PaymentMethod
from .serializers import DeliveryDetailSerializer, DeliveryTimeSerializer, PaymentMethodSerializer
from django.conf import settings
from django.views import View
from django.http import JsonResponse
import requests
import json



class DeliveryDetailViewSet(viewsets.ModelViewSet):
    queryset = DeliveryDetail.objects.all()
    serializer_class = DeliveryDetailSerializer

class DeliveryTimeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTime.objects.all()
    serializer_class = DeliveryTimeSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


# payment gateway

class InitializePaymentView(View):
    def post(self, request, *args, **kwargs):
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        data = json.loads(request.body)
        payload = {
            'email': data.get('email'),
            'amount': data.get('amount') * 100  # Amount in kobo
        }
        response = requests.post(url, headers=headers, json=payload)
        return JsonResponse(response.json())
