from django.core.management.base import BaseCommand
from tasks.models import Task, SubTask
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Создаёт задачу и подзадачи'

    def handle(self, *args, **kwargs):
        task = Task.objects.create(
            title="Prepare presentation",
            description="Prepare materials and slides for the presentation",
            status="New",
            deadline=datetime.now() + timedelta(days=3)
        )
        subtask_1 = SubTask.objects.create(
            title="Gather information",
            description="Find necessary information for the presentation",
            status="New",
            deadline=datetime.now() + timedelta(days=2),
            task=task
        )
        subtask_2 = SubTask.objects.create(
            title="Create slides",
            description="Create presentation slides",
            status="New",
            deadline=datetime.now() + timedelta(days=1),
            task=task
        )

        self.stdout.write(self.style.SUCCESS('Task and subtasks created successfully!'))