from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from todo.models import Task
from .forms import TaskForm
from django.contrib import messages

# Create your views here.
def tasks(request):
    tasks = Task.objects.all()
    context = {'tasks' : tasks}
    return render(request, "todo/home.html", context)

def task_details(request, id):
    task = Task.objects.get(id=id)
    context = {'task' : task}
    return render(request, "todo/task_id.html", context)

def search_task(request):
    query_dict = request.GET
    try:
        query = int(query_dict.get('q'))

    except:
        query = None

    task = None
    
    if query is not None:
        try:
            task = Task.objects.get(id=query)
        except Task.DoesNotExist:
            task = None
    
    context = {'task' : task}
    return render(request, "todo/search.html", context)
        

@login_required
def add_task(request):
    if 'back' in request.POST:
        return redirect('tasks')
    form = TaskForm(request.POST or None)
    context = {'form' : form}
    if form.is_valid():
        task_obj = form.save()
        context['form'] = TaskForm()
        
        messages.success(request, f"Task: '{task_obj}' created successfully")
        return redirect('add_task')
    
    return render(request, "todo/add.html", context)