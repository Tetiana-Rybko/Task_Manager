from .serializers import SubTaskCreateSerializer
from .views import TaskCreateView, TaskListView, TaskDetailView, home, TaskStatsView, create_subtask
from django.urls import path


urlpatterns = [
    path('stats/', TaskStatsView.as_view(), name='task-stats'),
    path('', home, name='home'),
    path('create/', TaskCreateView.as_view(), name='tasks-create'),
    path('list/',TaskListView.as_view(), name='tasks-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='tasks-detail'),
    path('subtask/create/',create_subtask,name='subtask-create'),

]