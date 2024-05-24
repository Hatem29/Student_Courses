from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.models import Group
from .decorators import * 
from .forms import * 


# @forAdmins
@login_required(login_url='login')
def home(request): 
    courses = Courses.objects.all()
    students = Student.objects.all()
    Schedules = CourseSchedules.objects.all()
    context = {
        "courses":courses,
        "students":students,
        'schedules':Schedules,
    }
    return render(request, "App/dashboard.html",context)


@login_required(login_url='login')
def students(request):
    return render(request, 'App/students.html')

@notLoggedUser
def register(request):
    print(0)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first = request.POST['first']
        last = request.POST['last']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first, last_name=last)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_student = Student.objects.create(user=user_model, id=user_model.id, first_name=first, last_name=last, email=email)
                new_student.save()
                return redirect('home')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')
        
    else:
        return render(request, 'App/register.html')

@notLoggedUser
def login(request):
    # print('hannooooooo error')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            # print(username + ' ' + password)
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'App/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def course(request, pk):
    course = Courses.objects.get(id=pk)
    context = {'course':course}
    return render(request, 'App/course.html', context)

def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        student.delete()
        user.delete()
        return redirect('/') 

    context = {'student':student}
    return render(request, 'App/deleteStudent.html', context)

def deleteCourse(request, pk):
    course = Courses.objects.get(id=pk)
    scheduled = CourseSchedules.objects.get(id=course.scheduled.id)
    if request.method == 'POST': 
        course.delete()
        scheduled.delete()
        return redirect('/') 
    
    context = {'course':course}
    return render(request, 'App/deleteCourse.html', context)

def updateCourse(request, pk):
    course = Courses.objects.get(id=pk)
    courses = Courses.objects.all()
    schedules = CourseSchedules.objects.all()

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully')
            return redirect('/')
    else:
        form = CourseForm(instance=course)

    context = {'form': form, 'course': course, 'scheduled': schedules, 'courses': courses}
    return render(request, 'App/updateCourse.html', context)

def createCourse(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        description = request.POST['description']
        prerequisites_id = request.POST.get('prerequisites') 
        instructor = request.POST['instructor']
        capacity = request.POST['capacity']
        scheduled_id = request.POST['scheduled']

        if prerequisites_id == '':
            prerequisites = None
        else:
            prerequisites = Courses.objects.get(id=prerequisites_id)
        
        if scheduled_id == '':
            messages.info(request, 'Course withot scheduled')
            return redirect('createCourse')
        else:
            scheduled = CourseSchedules.objects.get(id=scheduled_id)
        
        if Courses.objects.filter(id=id).exists():
            messages.info(request, 'Course with this ID already exists')
            return redirect('createCourse')
        else:
            course = Courses(id=id, name=name, description=description, prerequisites=prerequisites, instructor=instructor, capacity=capacity, scheduled=scheduled)
            course.save()
            return redirect('home')
    else:
        courses = Courses.objects.all()
        scheduled = CourseSchedules.objects.all()
        return render(request, 'App/createCourse.html', {'courses': courses, 'scheduled': scheduled})
    
def createScheduled(request):
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('/')  
    else:
        form = CourseScheduleForm()
    return render(request, 'App/createScheduled.html', {'form': form})

def deleteScheduled(request,pk):
    scheduled = CourseSchedules.objects.get(id=pk)
    if request.method == 'POST': 
        scheduled.delete()
        return redirect('/') 
  
    return render(request, 'App/deleteScheduled.html', {'scheduled': scheduled})
