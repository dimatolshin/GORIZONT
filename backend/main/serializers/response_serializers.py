from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    user=UserSerializer(allow_null=True)
    class Meta:
        model = Tasks
        fields = '__all__'