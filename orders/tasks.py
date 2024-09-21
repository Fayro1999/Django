# orders/tasks.py
from fcm_django.models import FCMDevice
from django.utils import timezone

def send_order_notification(order, location):
    # Gather order details
    order_id = order.id
    product_image = order.products.first().image.url if order.products.exists() else None
    store = order.store
    store_name = store.name
    store_location = f"{store.address}, {store.city}, {store.state}"
    delivery_location = f"{order.delivery.receiver_address}" if order.delivery else None
    
    # Create notification payload
    notification_data = {
        'title': f"Delivery Request for Order {order_id}",
        'body': f"Store: {store_name}, Delivery Location: {delivery_location}",
        'order_id': order_id,
        'product_image': product_image,
        'store_location': store_location,
        'delivery_location': delivery_location
    }

    # Send push notifications to all riders in the location
    riders = FCMDevice.objects.filter(user__location=location)  # Adjust query to match rider's location field

    # Send notification
    riders.send_message(
        title=notification_data['title'],
        body=notification_data['body'],
        data=notification_data
    )

    # Log the notification timestamp
    order.last_notification_sent = timezone.now()
    order.save()
