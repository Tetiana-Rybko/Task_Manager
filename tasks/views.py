from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count
from django.http import HttpResponse
from .models import Task, SubTask,Category
from .serializers import TaskSerializer, SubTaskCreateSerializer, TaskDetailSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import models
from .serializers import CategorySerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
import logging

def home(request):
    return HttpResponse("Привет! Всё работает!")

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

class TaskStatsView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        status_count = Task.objects.values('status').order_by('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(deadline__lt=now()).count()

        return Response({
            'total_tasks': total_tasks,
            'overdue_tasks': overdue_tasks,
            'status_count': status_count,
        })

@api_view(['POST'])
def create_subtask(request):
    serializer = SubTaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def task_detail_view(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(status=404)

    serializer = TaskDetailSerializer(task)
    return Response(serializer.data)

class SubTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = SubTask.objects.all()
        task_name = self.request.query_params.get('task')
        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)
        return queryset
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

class TaskDayView(APIView):
    def get(self, request):
        return Response({"message": "TaskDayView работает!"})



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response({"message": "Категория мягко удалена."})

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = Category.objects.all()
        data = []
        for category in categories:
            task_count = Task.objects.filter(categories=category).count()
            data.append({
                'category': category.name,
                'task_count': task_count
            })
        return Response(data)

logger_http = logging.getLogger('django.request')

def log_test_view(request):
    logger_http.info('TEST: HTTP LOG OK!')
    return HttpResponse('prêt! vérifier http_logs.log')


