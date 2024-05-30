from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import *
from django.contrib.auth.models import Group
from .decorators import * 
from .forms import * 
from .filters import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


@login_required(login_url='login')
@forAdmins
def home(request):
    courses = Courses.objects.all()
    students = Student.objects.all()
    schedules = CourseSchedules.objects.all()
    
    if request.GET.get('searchStudents'):
        query = request.GET.get('searchStudents')
        students = students.filter(first_name__icontains=query) | students.filter(last_name__icontains=query) | students.filter(email__icontains=query)
    else: 
        students = students

    if request.GET.get('searchCourses'):
        query = request.GET.get('searchCourses')
        courses = courses.filter(id__icontains=query) | courses.filter(name__icontains=query) | courses.filter(instructor__icontains=query)
    else: 
        courses = courses

    context = {
        'courses': courses,
        'students': students,
        'schedules': schedules,
    }

    return render(request, 'App/dashboard.html', context)

@login_required(login_url='login')
@forStudents
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
                group= Group.objects.get(name="student")
                user.groups.add(group) 

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

@login_required(login_url='login')
def course(request, pk):
    course = Courses.objects.get(id=pk)
    enroll = StudentReg.objects.filter(courseID = course).count()
    regs = StudentReg.objects.count()
    pop = enroll/regs * 100

    context = {'course':course,
               'enroll':enroll,
               'pop':pop,
               }
    return render(request, 'App/course.html', context)
   
@login_required(login_url='login')
@forAdmins
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        student.delete()
        user.delete()
        messages.warning(request, "deleted")
        return redirect('/') 

    context = {'student':student}
    return render(request, 'App/deleteStudent.html', context)

@login_required(login_url='login')
@forAdmins
def deleteCourse(request, pk):
    course = Courses.objects.get(id=pk)
    if request.method == 'POST': 
        course.delete()
        messages.warning(request, "deleted")
        return redirect('/') 
    
    context = {'course':course}
    return render(request, 'App/deleteCourse.html', context)

@login_required(login_url='login')
@forAdmins
def updateCourse(request, pk):
    course = Courses.objects.get(id=pk)
    courses = Courses.objects.all()
    schedules = course.courseSchedules

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()

            schedules.startTime = request.POST.get('startTime')
            schedules.endTime = request.POST.get('endTime')
            schedules.days = request.POST.get('days')
            schedules.roomNo = request.POST.get('roomNo')
            schedules.save()

            messages.success(request, 'Course and schedule updated successfully')
            return redirect('/')
        else:
            messages.warning(request, 'not valid')

    else:    
        form = CourseForm(instance=course)
    
    context = {'form': form, 'course': course, 'scheduled': schedules, 'courses': courses}
    return render(request, 'App/updateCourse.html', context)

@login_required(login_url='login')
@forAdmins
def createCourse(request):
    if request.method == 'POST':
        form = CourseScheduleForm(request.POST)
        if form.is_valid():
            course_id = request.POST['id']
            name = request.POST['name']
            description = request.POST['description']
            instructor = request.POST['instructor']
            capacity = int(request.POST['capacity'])
            prerequisites_ids = request.POST.getlist('prerequisites')
            
            if Courses.objects.filter(id=course_id).exists():
                messages.warning(request, 'Course with this ID already exists')
                return redirect('createCourse')
            
            schedule = form.save(commit=False)  
            
            course = Courses(
                id=course_id,
                name=name,
                description=description,
                instructor=instructor,
                capacity=capacity
            )
            
            course.save()
            
            schedule.course_id = course.id  
            schedule.save()  
            
            course.courseSchedules = schedule  
            course.save()  
            
            if prerequisites_ids:
                prerequisites = Courses.objects.filter(id__in=prerequisites_ids)
                course.prerequisites.add(*prerequisites)
            
            messages.success(request, 'Course created successfully')
            return redirect('home')
        else:
            messages.warning(request, 'There was an error in the form. Please correct it and try again.')
    else:
        form = CourseScheduleForm()
        courses = Courses.objects.all()
        return render(request, 'App/createCourse.html', {'form': form, 'courses': courses})

@login_required(login_url='login')
@forStudents
def myCourses(request):
    all_courses = []
    try:
        studentReg = StudentReg.objects.filter(studentID=request.user.id)
        # print("HANnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnoooooooooooooooooooooooooooooooooooooooooo")

        for item in studentReg:
            courses = Courses.objects.filter(id=item.courseID.id)
            all_courses.extend(courses)

    except ObjectDoesNotExist:
        pass

    context = {
        "courses":all_courses,
    }

    return render(request, "App/myCourses.html", context)

@login_required(login_url='login')
@forStudents
def courses(request):
    courses = Courses.objects.all()

    if request.GET.get('searchCourses'):
        query = request.GET.get('searchCourses')
        courses = courses.filter(id__icontains=query) | courses.filter(name__icontains=query) | courses.filter(instructor__icontains=query)
    else: 
        courses = courses

    context = {
        "courses":courses,
    }

    return render(request, "App/courses.html", context)

@login_required(login_url='login')
@forStudents
def enrollStudent(request, pk):
    student = Student.objects.get(id=request.user.id)
    course = Courses.objects.get(id=pk)
    
    if StudentReg.objects.filter(studentID=student, courseID=course).exists():
        messages.warning(request, "Course is already enrolled/taken")
        return redirect('courses')
    
    course_schedule = course.courseSchedules
    
    student_regs = StudentReg.objects.filter(studentID=student).values_list('courseID', flat=True)
    student_schedules = CourseSchedules.objects.filter(courses__in=student_regs)
    
    exist = student_schedules.filter(
        Q(startTime__range=(course_schedule.startTime, course_schedule.endTime)) |
        Q(endTime__range=(course_schedule.startTime, course_schedule.endTime)) |
        Q(startTime__lte=course_schedule.startTime, endTime__gte=course_schedule.endTime),
        roomNo=course_schedule.roomNo, days=course_schedule.days
    ).exists()
    
    if exist:
        messages.warning(request, "Course schedules not suitable")
        return redirect('courses')
    
    prerequisites = course.prerequisites.all()
    if not all(prerequisite.id in student_regs for prerequisite in prerequisites):
        messages.warning(request, "Not all pre-requisites are met")
        return redirect('courses')
    
    student_reg = StudentReg(studentID=student, courseID=course)
    student_reg.save()

    messages.success(request, 'Successfully')
    return redirect('courses')

@login_required(login_url='login')
@forStudents
def unrollStudent(request, pk):
    studentReg = StudentReg.objects.get(courseID=pk, studentID = request.user.id)
    studentReg.delete()
    return redirect('myCourses') 

def notification(request):
    notification = Notification.objects.all()
    print(notification)
    return render(request, 'App/notification.html', {'notification': notification})
