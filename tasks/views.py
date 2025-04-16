from django.http import HttpResponse

def home(request):
    return HttpResponse("Привет! Всё работает!")

from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
# Create your views here.
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer