from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customers_when_robot_available(sender, instance, created, **kwargs):
    orders = Order.objects.filter(robot_serial=instance.serial, is_finished=False)

    for order in orders:
        send_mail(
            subject='Ваш заказ на робота доступен!',
            message=f'Добрый день!\n\nНедавно вы интересовались нашим роботом модели {instance.model}, '
                    f'версии {instance.version}. Этот робот теперь в наличии. Если вам подходит '
                    f'этот вариант - пожалуйста, свяжитесь с нами.',
            from_email='example@yandex.ru',
            recipient_list=[order.customer.email],
        )

        order.is_finished = True
        order.save()

