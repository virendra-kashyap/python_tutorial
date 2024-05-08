from django.shortcuts import render, redirect, get_object_or_404
from .models import Users
from .forms import UsersForm, LoginForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
import logging

logger = logging.getLogger(__name__)

def users_list(request):
    users = Users.objects.all()
    paginator = Paginator(users, 7)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users_list.html', {'page_obj': page_obj})

def save_user(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UsersForm()
    return render(request, 'user_form.html', {'form': form})

def update_user(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        form = UsersForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = UsersForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def delete_user(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    return render(request, 'user_delete.html', {'user': user})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('users_list')  # Redirect to the home page after successful login
            else:
                # Authentication failed, handle accordingly
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})