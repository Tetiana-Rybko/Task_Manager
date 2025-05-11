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
        fields = ['id', 'title', 'description', 'tasks','created_id', 'status', 'deadline']
        read_only_fields = ['created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
     subtasks = SubTaskCreateSerializer(many=True, read_only=True)

     class Meta:
         model = Task
         fields = ['id', 'title', 'description', 'status', 'deadline', 'subtasks']


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name','is_deleted','deleted_at']

    def validate_name(self, value):
        if self.instance:
            if Category.objects.exclude(id=self.instance.id).filter(name=value).exists():
                raise ValidationError("Category already exists")
            else:
                if Category.objects.filter(name=value).exists():
                    raise ValidationError("Category already exists")
            return value

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','is_deleted','deleted_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id','title','description','status','deadline','categories']

    def validate_deadline(self, value):
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError("Deadline must be greater than now")
        return value
