from django.contrib import admin

# Register your models here.
from todo.models import Task


class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'date_created', 'updated']
    search_fields = ['id', 'title']
    raw_id_fields = ['user']

admin.site.register(Task, TodoAdmin)