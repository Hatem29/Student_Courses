from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.models import Group
from .decorators import * 


# @forAdmins
@login_required(login_url='login')
def home(request):
    return render(request, 'App/home.html')

@login_required(login_url='login')
def students(request):
    return render(request, 'App/students.html')

@notLoggedUser
def register(request):
    print(0)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                print(1)
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(email=email, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(email=email)
                new_student = Student.objects.create(user=user_model, id=user_model.id)
                new_student.save()
                print(2)
                return redirect('home')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        
    else:
        return render(request, 'App/register.html')

@notLoggedUser
def login(request):
    print('hannooooooo error')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('App/home')
        else:
            print('hannooooooo error')
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'App/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')