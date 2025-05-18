from django.db.models.signals import pre_save
from django.dispatch import receiver

from tasks.models import Task


@receiver(pre_save, sender=Task)
def task_created_signal(sender, instance, created, **kwargs):
    if created:
        print("=" * 100)
        print("=" * 100)
        print()
        print(f"New Task was created. It's {instance.name}")
        print()
        print("=" * 100)
        print("=" * 100)
    else:
        print("=" * 100)
        print("=" * 100)
        print()
        print(f"The task was updated. Now it's {instance.name}")
        print()
        print("=" * 100)
        print("=" * 100)
