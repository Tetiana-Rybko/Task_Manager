import os
import django
import random
from faker import Faker
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskManager.settings')
django.setup()

# from your_app_name.models import Task, SubTask, Category  # замените на имя вашего приложения
from tasks.models import Task, SubTask, Category
fake = Faker()

STATUSES = ['New', 'In progress', 'Pending', 'Blocked', 'Done']

# Создание категорий
def create_categories(n=5):
    categories = []
    for _ in range(n):
        name = fake.word().capitalize()
        category, created = Category.objects.get_or_create(name=name)
        categories.append(category)
    return categories

# Создание задач и подзадач
def create_tasks(categories, n=10):
    for _ in range(n):
        title = fake.sentence(nb_words=3).rstrip('.')
        description = fake.text()
        status = random.choice(STATUSES)
        deadline = fake.date_time_between(start_date='+1d', end_date='+30d')

        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )

        task.categories.set(random.sample(categories, k=random.randint(1, 3)))

        # Создание подзадач
        for _ in range(random.randint(1, 4)):
            sub_title = fake.sentence(nb_words=2).rstrip('.')
            sub_description = fake.text()
            sub_status = random.choice(STATUSES)
            sub_deadline = fake.date_time_between(start_date='now', end_date=deadline)

            SubTask.objects.create(
                title=sub_title,
                description=sub_description,
                status=sub_status,
                deadline=sub_deadline,
                task=task
            )

if __name__ == '__main__':
    categories = create_categories()
    create_tasks(categories)
    print("Данные успешно сгенерированы.")