from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import User
from .forms import userForm


def home(request):
    works = ['1. need to define database', '2. System design',
             '3. i hope you can write html from ']
    context = {
        'works': works
    }
    return render(request, "base/home.html", context)


def read(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'base/read.html', context)


def create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        text = request.POST['text']
        users = User.objects.create(
            name=name, email=email, password=password, text=text)
        users.save()
        return HttpResponse('success')
    form = userForm()
    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Success')
            return redirect('home')

    return render(request, 'base/create.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')


def login_req(request):
    if request.user.is_authenticated:
        return redirect('read')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(username=user.username, password=password)
        # user = EmailBackend.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            print('succes')
            login(request, user)
            return redirect('read')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'base/loginform.html')


def update(request, pk):
    users = User.objects.get(id=pk)
    if request.method == 'POST':
        users.name = request.POST['name']
        users.email = request.POST['email']
        users.password = request.POST['password']
        users.text = request.POST['text']
        users.save()
        return HttpResponse('success')
    context = {
        'users': users
    }
    return render(request, 'base/update.html', context)


def delete(request, pk):
    if request.method == 'POST':
        users = User.objects.get(id=pk)
        users.delete()
        return redirect('read')
    return render(request, 'base/delete.html')
