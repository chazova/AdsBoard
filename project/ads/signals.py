from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Reply, Ad
from django.core.mail import send_mail


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Reply)
def notify_user_reply(sender, instance, created, **kwargs):
    if created:
        subject = f'Новый отклик на Ваше объявление {instance.ad}'
        message = f'{instance.user} оставил отклик на Ваше объявление {instance.ad}: {instance.reply_text}. ' \
                  f'Отклик можно принять в личном кабинете.'
        author_email = instance.ad.author.author.email

        send_mail(
            subject=subject,
            message=message,
            from_email='test-mail-dj@yandex.ru',
            recipient_list=[author_email],
        )
    else:
        if instance.is_confirm == 'true':
            subject = f'Ответ на Ваш отклик по объявлению {instance.ad}'
            message = f'{instance.ad.author} принял Ваш отклик на объявление {instance.ad}. ' \
                      f'E-mail для связи с автором: {instance.ad.author.author.email}.'
            user_email = instance.user.email

            send_mail(
                subject=subject,
                message=message,
                from_email='test-mail-dj@yandex.ru',
                recipient_list=[user_email],
            )

@receiver(post_delete, sender=Reply)
def notify_user_delete_reply(sender, instance, **kwargs):
    subject = f'Ответ на Ваш отклик по объявлению {instance.ad}'
    message = f'{instance.ad.author} удалил Ваш отклик на объявление {instance.ad}.'
    user_email = instance.user.email

    send_mail(
        subject=subject,
        message=message,
        from_email='test-mail-dj@yandex.ru',
        recipient_list=[user_email],
    )