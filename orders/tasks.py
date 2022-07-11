from celery import shared_task

from django.core.mail import send_mail

from .models import Order
from e_library.settings import EMAIL_HOST_USER


@shared_task
def order_created(order_id):
    """Отправка email уведомление при успешном оформлении заказа"""
    order = Order.objects.get(id=order_id)
    subject = f"Заказа №{order.id}"
    message = f"{order.first_name}, Здравствуйте! Ваш заказ был принят в обработку! Благодарим вас за покупку!" \
              f"Номер вашего заказа: {order.id}"
    mail_sent = send_mail(subject,
                          message,
                          EMAIL_HOST_USER,
                          [order.email], )
    return mail_sent
