from datetime import datetime, timedelta

import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from News_Portal.settings import DEFAULT_FROM_EMAIL
from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    # Все посты за прошедшую неделю
    week_ago = datetime.now() - timedelta(weeks=1)

    # пройдем по всем пользователям и направим каждому уведомление
    for user in User.objects.all():
        # Все посты за неделю в категориях, на которые подписан пользователь
        week_posts = Post.objects.filter(
            creation_time__date__gte=week_ago,
            categories__in=Category.objects.filter(subscribers=user)
        )

        # Пропустим, если интересующих нас статей нет
        if not week_posts:
            continue

        urls = ['http://127.0.0.1/news/' + str(week_posts[i].pk)
                for i in range(len(week_posts))]

        message = f'Здравствуй, {user.username}. Новые статьи в твоих любимых ' \
                  f'разделах за неделю: \n\n'

        for url in urls:
            message += url + '\n'

        print(message)

        html_content = render_to_string(
            '../templates/notify_subscribers_about_new_posts_weekly.html',
            {
                'subscriber': user.username,
                'week_posts': week_posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body=message,
            from_email=DEFAULT_FROM_EMAIL,
            to=[f'{user.email}']
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
