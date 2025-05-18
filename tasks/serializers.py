from rest_framework import serializers
from .models import Task,SubTask,Category
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline','owner']

class SubTaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline','owner']



class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task','created_at', 'status', 'deadline']
        read_only_fields = ['created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
     subtasks = SubTaskSerializer(many=True, read_only=True)

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




class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 're_password']

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        re_pattern = r'^[a-zA-Z]+$'
        if first_name and not re.match(re_pattern, first_name):
            raise serializers.ValidationError({"first_name": "Имя должно содержать только латинские буквы."})

        if last_name and not re.match(re_pattern, last_name):
            raise serializers.ValidationError({"last_name": "Фамилия должна содержать только латинские буквы."})

        if not password:
            raise serializers.ValidationError({"password": "Пароль обязателен."})
        if not re_password:
            raise serializers.ValidationError({"re_password": "Подтверждение пароля обязательно."})
        if password != re_password:
            raise serializers.ValidationError({"re_password": "Пароли не совпадают."})

        validate_password(password)

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user