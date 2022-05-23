from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

from News_Portal.settings import DEFAULT_FROM_EMAIL


# Отправим письмо пользователю при регистрации. Пользователь успешно
# зарегистрировался, когда запись о нем добавилась в базу User
@receiver(post_save, sender=User)
def notify_user_created(sender, instance, **kwargs):
    send_mail(
        subject='Добро пожаловать',
        message=f'Здравствуйте, {instance.username}. Вы успешно '
                f'зарегистрировались на сайте',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[f'{instance.email}']
    )
