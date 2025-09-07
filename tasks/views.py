from django.shortcuts import render, get_object_or_404
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import Http404



# @api_view(['GET', 'POST'])
# def tasks(request):
#     items = Task.objects.select_related('owner').all()
#     serialized = TaskSerializer(items, many=True)
#     return Response(serialized.data)

@api_view()
def overview(request):
    all_urls = {
        'To see all endpoints': '/overview/',
        'List and Create': '/api/tasks/',
        'Single View(Retrieve, update and delete)': 'api/task/<int:pk>/'
    }
    return Response(all_urls)

def get_task(pk):
    try:
        return Task.objects.select_related('owner').get(id=pk)

    except Task.DoesNotExist:
        raise Http404
    

@api_view(['GET', 'POST'])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, 201)
        return Response(serializer.errors, 400)
    

@api_view(['GET', 'PUT'])
def task_detail(request, pk):
    item = get_task(pk)
    if request.method == 'GET':
        serialized = TaskSerializer(item)
        return Response(serialized.data)
    elif request.method == 'PUT':
        serialized = TaskSerializer(item, data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors)
