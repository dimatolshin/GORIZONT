from celery import shared_task
from django.utils.timezone import now
import pytz
from datetime import timedelta
from asgiref.sync import async_to_sync
from telegram import send_message_to_user

moscow_tz = pytz.timezone('Europe/Moscow')


@shared_task(acks_late=True, reject_on_worker_lost=True)
def check_deadline():
    from .models import Tasks
    print("I'm here")
    current_time = now().astimezone(moscow_tz).replace(tzinfo=None)
    [async_to_sync(send_message_to_user)(telegram_id=task.user.tg_id,
                                         minutes=int((task.deadline - current_time).total_seconds()) // 60,
                                         seconds=int((task.deadline - current_time).total_seconds()) % 60,
                                         task_id=task.id) for task in
     Tasks.objects.filter(deadline__lte=current_time + timedelta(minutes=10), deadline__gte=current_time,
                          status='in_progres').select_related('user').all()]
