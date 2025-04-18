from rest_framework import serializers
from .models import Task,SubTask,Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
     subtasks = SubTaskCreateSerializer(many=True, read_only=True)
     class Meta:
         model = Task
         fields = ['id', 'title', 'description', 'status', 'deadline', 'subtasks']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, value):
        if self.instance:
            if Category.objects.exclude(id=self.instance.id).filter(title=value).exists():
                raise ValidationError("Category already exists")
            else:
                if Category.objects.filter(title=value).exists():
                    raise ValidationError("Category already exists")
            return value
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    def validate_deadline(self, value):
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError("Deadline must be greater than now")
        return value
