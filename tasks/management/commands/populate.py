from django.core.management.base import BaseCommand
from faker import Faker
import random
from tasks.models import Task, SubTask, Category
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Наполняет базу тестовыми задачами'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')

        SubTask.objects.all().delete()
        Task.objects.all().delete()
        Category.objects.all().delete()

        category_names = ['Фортепиано', 'Гитара', 'Скрипка', 'Теория музыки', 'Хоровое пение']
        task_statuses = ['New', 'In progress', 'Pending', 'Blocked', 'Done']
        subtask_statuses = task_statuses

        subtask_templates = [
            'Разучить гаммы',
            'Пальцевая техника',
            'Разучить часть произведения',
            'Повторить старый материал',
            'Уделить внимание ритму',
            'Слушать запись для вдохновения'
        ]

        categories = []
        for name in category_names:
            categories.append(Category.objects.create(name=name))

        for _ in range(10):
            task = Task.objects.create(
                title=fake.unique.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=2),
                status=random.choice(task_statuses),
                deadline=timezone.now() + timedelta(days=random.randint(5, 30)),
            )
            task.categories.set(random.sample(categories, k=random.randint(1, 2)))

            for _ in range(random.randint(2, 4)):
                SubTask.objects.create(
                    task=task,
                    title=random.choice(subtask_templates),
                    description=fake.sentence(),
                    status=random.choice(subtask_statuses),
                    deadline=timezone.now() + timedelta(days=random.randint(2, 20)),
                )

        self.stdout.write(self.style.SUCCESS('База успешно заполнена!'))
