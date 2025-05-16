from django.db import models
from datetime import date, datetime
from django.utils.timezone import now
import pytz


def get_moscow_time():
    moscow_tz = pytz.timezone("Europe/Moscow")
    return now().astimezone(moscow_tz)


class User(models.Model):
    tg_id = models.BigIntegerField()

    def __str__(self):
        return f'tg_id:{self.tg_id}'


class Tasks(models.Model):
    title = models.CharField(verbose_name='заголовок')
    description = models.CharField(verbose_name='описание')
    deadline = models.DateTimeField(default=get_moscow_time, verbose_name='Дата и время создания таски')
    user = models.ForeignKey(User,related_name='tasks',on_delete=models.SET_NULL, null=True, blank=True)
    status= models.CharField(default='in_progres',verbose_name='Статус')


    def __str__(self):
        if self.user:
            return f'id:{self.id},title:{self.title},tg_id:{self.user.tg_id}'
        else:
            return ''