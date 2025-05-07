import pytest
from rest_framework.test import APIClient
from tasks.models import Task, SubTask


@pytest.mark.django_db
def test_filter_subtasks_by_task_and_status():
    client = APIClient()

    task = Task.objects.create(title="Музыка", description="Описание", status="todo")

    SubTask.objects.create(task=task, title="Купить гитару", status="done")
    SubTask.objects.create(task=task, title="Выучить аккорды", status="in_progress")
    SubTask.objects.create(task=task, title="Сыграть песню", status="done")
    SubTask.objects.create(task=task, title="Записать видео", status="todo")
    SubTask.objects.create(task=task, title="Выложить видео", status="done")
    SubTask.objects.create(task=task, title="Ответить на комментарии", status="done")

    response = client.get("/api/subtasks/?task=Музыка&status=done")

    assert response.status_code == 200

    assert len(response.data['results']) == 5
    for subtask in response.data['results']:
        assert subtask['status'] == 'done'


