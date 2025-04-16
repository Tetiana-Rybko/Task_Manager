from .views import TaskCreateView
from django.urls import path


urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='tasks-create'),
]