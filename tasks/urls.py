from .views import TaskCreateView,TaskListView,TaskDetailView
from django.urls import path


urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='tasks-create'),
    path('list/',TaskListView.as_view(), name='tasks-list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='tasks-detail'),
]