from celery import shared_task
import time

from .models import Post
from .signals import notify_subscribers_new_post
from .management.commands.email_subscribers_weekly import my_job


@shared_task
def email_subscribers_new_post(post_id):
    # Для того чтобы проверить работу celery, пока используем функцию
    # отправки сообщения, которую мы подключали к сигналам записи в базу
    notify_subscribers_new_post(Post.objects.get(pk=post_id), 'post_add')


@shared_task
def email_subscribers_posts_for_week():
    # Для того чтобы проверить работу celery, пока используем функцию
    # отправки сообщений подписчикам с новостями за прошедшую неделю
    my_job()
