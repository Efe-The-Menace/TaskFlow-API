from .models import Task
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class Userserializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TaskSerializer(ModelSerializer):
    owner = Userserializer(read_only=True)
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed_status', 'owner']