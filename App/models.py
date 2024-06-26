from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class CourseSchedules(models.Model):
    DAYS = (
        ('3-days','sunday-tuesday-thursday'),
        ('2-days','monday-wensday'),
    )
    id = models.AutoField(primary_key=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.CharField(max_length=10, null=True, choices=DAYS)
    roomNo = models.CharField(max_length=20)


class Courses(models.Model):
    id = models.CharField(primary_key=True,max_length=10)
    name = models.CharField( max_length=50)
    description = models.CharField(max_length=255)
    prerequisites = models.ManyToManyField('self', blank=True)
    instructor = models.CharField(max_length=50)
    capacity = models.IntegerField()
    courseSchedules = models.ForeignKey(CourseSchedules, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class StudentReg(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Courses, on_delete=models.CASCADE)
    def __str__(self):
        return self.studentID.user.username + " " + self.courseID.name

class Notification(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_created=True,null=True)
    message = models.TextField()

    def _str_(self):
        return f'Notification for {self.course.name} course'