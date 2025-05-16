import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django_celery_beat.models import PeriodicTask, IntervalSchedule

def create_task():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )

    if not PeriodicTask.objects.filter(name='send_message_task').exists():
        PeriodicTask.objects.create(
            interval=schedule,
            name='send_message_task',
            task='main.tasks.check_deadline',
            enabled=True,
        )
        print("Periodic task created")
    else:
        print("Periodic task already exists")

if __name__ == "__main__":
    create_task()