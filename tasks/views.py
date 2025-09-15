from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.throttling import AnonRateThrottle
from .throttling import TenPerMinute
from .permissions import IsInAdminClass
from .endpoints import all_urls
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

@api_view()
@permission_classes([IsInAdminClass])
def overview(request):
    return Response(all_urls)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@throttle_classes([TenPerMinute, AnonRateThrottle])
def task_list_create(request):
    if request.method == 'GET':
        perpage = request.query_params.get('perpage', default=3)
        page = request.query_params.get('page', default=1)
        tasks = Task.objects.select_related('owner').all()
        paginator = Paginator(tasks, per_page=perpage)
        try:
            tasks = paginator.page(number=page)
        except EmptyPage:
            tasks = []
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def get_task(pk):
    try:
        return Task.objects.select_related('owner').get(id=pk)

    except Task.DoesNotExist:
        raise Http404
    

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
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)  
    if request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        admin = get_object_or_404(Group, name='Admin')
        if request.method == 'POST':
            admin.user_set.add(user)
        elif request.method == 'DELETE':
            admin.user_set.remove(user)
            return Response({"Message": "OK"})
    return Response({"Message": "error"}, status=status.HTTP_400_BAD_REQUEST)

