from rest_framework import serializers


class CreateTask(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    tg_id = serializers.IntegerField()
    deadline = serializers.DateTimeField()


class GetTask(serializers.Serializer):
    task_id = serializers.IntegerField()

class TgId(serializers.Serializer):
    telegram_user_id=serializers.IntegerField()