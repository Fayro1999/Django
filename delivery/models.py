from django.db import models

class DeliveryDetail(models.Model):
    reciever_name = models.CharField(max_length=255)
    reciever_mobile = models.CharField(max_length=255)
    reciver_address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.reciever_name}'

class DeliveryTime(models.Model):
    delivery_time = models.DateField()

    def __str__(self):
        return f'{self.delivery_time}'
   
class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.payment_method}'
    
