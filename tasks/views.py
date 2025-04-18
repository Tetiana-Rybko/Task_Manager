from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count
from django.http import HttpResponse
from .models import Task,SubTask
from .serializers import TaskSerializer,SubTaskCreateSerializer
from rest_framework import status




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


        return Response ({
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