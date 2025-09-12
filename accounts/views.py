from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegistrationForm
from django.contrib import messages

# Create your views here.


def register_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        logout(request)
        messages.success(request, "Account successfully created! Please log in", extra_tags='register')
        return redirect('login')
    # else:
    #     messages.error(request, "Please correct the error below.")
    context = {'form' : form}
    return render(request, "accounts/register.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!', extra_tags='login')
            return redirect('todo:all-tasks')
        else:
            messages.error(request, "Invalid Username or Password!", extra_tags='login_error')
            
    
    else:
        form = AuthenticationForm()
    context = {'form' : form}

    return render(request, "accounts/login.html", context)

def logout_view(request):           
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "logout":
            logout(request)
            return redirect('login')
        elif action =="Stay":
            return redirect('todo:all-tasks')

    context = {}
    return render(request, "accounts/logout.html", context)
