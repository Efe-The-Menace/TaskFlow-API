from django.shortcuts import render
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view()
def tasks(request):
    if request.user.is_superuser:
        items = Task.objects.all()
    else:
        items = Task.objects.select_related('owner').filter(owner__username=request.user)
    serialized = TaskSerializer(items, many=True)
    return Response(serialized.data)