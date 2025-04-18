from rest_framework import serializers
from .models import Task,SubTask,Category
from rest_framework.exceptions import ValidationError

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']
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
