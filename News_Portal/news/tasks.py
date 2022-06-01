from celery import shared_task
import time

from .models import Post
from .signals import notify_subscribers_new_post


@shared_task
def email_subscribers_new_post(post_id):
    # Для того чтобы проверить работу celery, пока используем функцию
    # отправки сообщения, которую мы подключали к сигналам записи в базу
    notify_subscribers_new_post(Post.objects.get(pk=post_id), 'post_add')
