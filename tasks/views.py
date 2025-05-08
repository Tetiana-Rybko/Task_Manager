from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count
from django.http import HttpResponse
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskCreateSerializer, TaskDetailSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

def home(request):
    return HttpResponse("Привет! Всё работает!")

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

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

class SubTaskDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

class TaskDayView(APIView):
    def get(self, request):
        return Response({"message": "TaskDayView работает!"})