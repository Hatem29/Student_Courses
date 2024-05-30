from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students', views.students, name='students'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('course/<str:pk>', views.course, name='course'),
    path('deleteStudent/<str:pk>', views.deleteStudent, name='deleteStudent'),
    path('updateCourse/<str:pk>', views.updateCourse, name='updateCourse'),
    path('deleteCourse/<str:pk>', views.deleteCourse, name='deleteCourse'),
    path('createCourse', views.createCourse, name='createCourse'),
    path('myCourses', views.myCourses, name="myCourses"),
    path('courses', views.courses, name="courses"),
    path('enrollStudent/<str:pk>', views.enrollStudent, name="enrollStudent"),
    path('unrollStudent/<str:pk>', views.unrollStudent, name="unrollStudent"),
    path('notification', views.notification, name="notification"),

]