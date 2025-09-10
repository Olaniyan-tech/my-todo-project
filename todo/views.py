from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.urls import reverse
from todo.models import Task
from .forms import TaskForm
from django.contrib import messages

# Create your views here.

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    context = {'tasks' : tasks}
    return render(request, "todo/home.html", context)

@login_required
def task_details(request, slug=None):
    task = get_object_or_404(Task, slug=slug, user=request.user)

    if request.method == "POST":
        task.completed = 'completed' in request.POST            
        task.save()
        return redirect('/')
    context = {'task' : task}
    return render(request, "todo/task_details.html", context)

@login_required
def search_task(request):
    if not request.user.is_authenticated:
        return redirect('login')
    query = request.GET.get('q')
    qs = Task.objects.search(query=query)
    context = {'search_task' : qs}
    if request.GET:
        context['search_task'] = qs[:5]
    return render(request, "todo/search.html", context)
        

@login_required
def add_task(request):
    if 'back' in request.POST:
        return redirect('tasks')
    form = TaskForm(request.POST or None)
    context = {'form' : form}
    if form.is_valid():
        task_obj = form.save(commit=False)
        task_obj.user = request.user
        task_obj.save()
        
        messages.success(request, f"Task: '{task_obj}' created successfully.")
        return redirect(task_obj.get_absolute_url())
    
    return render(request, "todo/add.html", context)

@login_required
def update_task(request, id=None):
    obj = get_object_or_404(Task, id=id)
    form = TaskForm(request.POST or None, instance=obj)
    context = {'form' : form}
    if form.is_valid():
        if form.has_changed():
            form.save()
            messages.success(request, 'Updated Successfully.')
        else:
            messages.info(request, 'No changes detected.')
                     
        return redirect(obj.get_absolute_url())
    
    return render(request, "todo/update.html", context)

@login_required
def delete_task(request, id=None):
    try: 
        task = Task.objects.get(id=id)
    except:
        task = None
    if task is None:
        return HttpResponse("Task not found!!!")
    
    if request.method == "POST":
        task.delete()
        messages.success(request, f"Task '{task}' deleted successfully!")
        redirect_url = reverse("todo:all-tasks")
        return redirect(redirect_url)
    context = {'task' : task}
    return render(request, "todo/delete.html", context)