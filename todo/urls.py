from django.urls import path

from todo.views import (
    tasks,
    search_task, 
    add_task,
    task_details, 
    update_task, 
    delete_task
)

app_name = 'todo'
urlpatterns = [
    path('', tasks, name='all-tasks'),
    path('search/', search_task, name='search'),
    path('add_task/', add_task, name='add'),
    path('update/<int:id>/', update_task, name='update'),
    path('delete/<int:id>/', delete_task, name='delete'),
    path('<slug:slug>/', task_details, name='details')
    
]