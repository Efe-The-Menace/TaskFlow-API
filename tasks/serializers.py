from .models import Task
from rest_framework import serializers
from django.contrib.auth.models import User


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed_status', 'owner', 'id']
