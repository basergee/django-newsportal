from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from News_Portal.settings import DEFAULT_FROM_EMAIL
from .models import PostCategory


# Отправим письмо пользователю при регистрации. Пользователь успешно
# зарегистрировался, когда запись о нем добавилась в базу User
@receiver(post_save, sender=User)
def notify_user_created(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Добро пожаловать',
            message=f'Здравствуйте, {instance.username}. Вы успешно '
                    f'зарегистрировались на сайте',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[f'{instance.email}']
        )


# Отправим письмо всем пользователям, подписанным на категорию, при добавлении
# новой новости этой категории.
# Вызов функции происходит два раза. Один раз с параметром action='pre_add',
# второй раз с параметром action='post_add'. Обработаем только второй случай.
# Отключаем от сигнала записи в базу, чтобы проверить работу через celery
# @receiver(m2m_changed, sender=PostCategory)
def notify_subscribers_new_post(instance, action, **kwargs):
    if action == 'post_add':
        # Из instance можно получить информацию о посте.
        # Составим текст и заголовок для письма пользователю
        email_subject = instance.title
        email_text = instance.content[:50] + '...'

        for c in instance.categories.all():
            for s in c.subscribers.all():
                url = 'http://127.0.0.1/news/' + str(instance.pk)
                message = f'Здравствуй, {s.username}. Новая статья в твоём ' \
                          f'любимом разделе: "{c.name}"!\n\n' + \
                          email_subject + '\n\n' + email_text + '\n' + url

                html_content = render_to_string(
                    '../templates/notify_subscribers_about_new_post.html',
                    {
                        'subscriber': s.username,
                        'category': c.name,
                        'post_title': email_subject,
                        'post_text':email_text,
                        'url': url,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=email_subject,
                    body=message,
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[f'{s.email}']
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
