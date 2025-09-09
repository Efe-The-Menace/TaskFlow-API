from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle
from .throttling import TenPerMinute
from .permissions import IsInAdminClass
from .endpoints import all_urls


@api_view()
@permission_classes([IsInAdminClass])
def overview(request):
    return Response(all_urls)

def get_task(pk):
    try:
        return Task.objects.select_related('owner').get(id=pk)

    except Task.DoesNotExist:
        raise Http404
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([TenPerMinute, AnonRateThrottle])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([TenPerMinute, AnonRateThrottle])
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
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)