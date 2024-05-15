from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class CourseSchedules(models.Model):
    id = models.IntegerField(primary_key=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    days = models.IntegerField()
    roomNo = models.CharField(max_length=20)

class Courses(models.Model):
    id = models.CharField(primary_key=True,max_length=10)
    name = models.CharField( max_length=50)
    description = models.CharField(max_length=255)
    prerequisites = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    instructor = models.CharField(max_length=50)
    capacity = models.IntegerField()
    scheduled = models.ForeignKey(CourseSchedules, on_delete=models.CASCADE)

class StudentReg(models.Model):
    id = models.IntegerField(primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseID = models.ForeignKey(Courses, on_delete=models.CASCADE)

