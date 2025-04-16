from django.http import HttpResponse
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count


def home(request):
    return HttpResponse("Привет! Всё работает!")

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListView(generics.ListAPIView):
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