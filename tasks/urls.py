from django.urls import path
from .views import (
    home,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskStatsView,
    create_subtask,
    task_detail_view,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskDayView
)



urlpatterns = [
    path('', home, name='home'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('subtasks/create/', create_subtask, name='create-subtask'),
    path('task-detail/<int:task_id>/', task_detail_view, name='task-detail-view'),
    path('task/by-day/', TaskDayView.as_view(), name='task-by-day'),



]