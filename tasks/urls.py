from django.urls import path
from .views import (
    home,
    TaskListCreateView,
    TaskDetailView,
    TaskStatsView,
    create_subtask,
    task_detail_view,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    TaskDayView,
    CategoryViewSet,
    log_test_view, UserTaskListView,
    RegisterView
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/stats/', TaskStatsView.as_view(), name='task-stats'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('subtasks/create/', create_subtask, name='create-subtask'),
    path('task-detail/<int:task_id>/', task_detail_view, name='task-detail-view'),
    path('task/by-day/', TaskDayView.as_view(), name='task-by-day'),
    path('log-test/', log_test_view),
    path('my-tasks/', UserTaskListView.as_view(), name='user-tasks'),
    path('register/', RegisterView.as_view(), name='register'),
] + router.urls