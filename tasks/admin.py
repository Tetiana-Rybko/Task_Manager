from django.contrib import admin
from .models import Task, SubTask, Category

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('title', 'description', 'status', 'deadline')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status','owner', 'deadline', 'id','created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'categories')
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return obj.title if len(obj.title) <= 10 else f'{obj.title[:10]}...'
    short_title.short_description = 'Title'


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status',)
    actions = ['mark_as_done']

    @admin.action(description="Mark selected subtasks as Done")
    def mark_as_done(self, request, queryset):
        queryset.update(status='Done')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)