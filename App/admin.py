from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentReg)
admin.site.register(Courses)
admin.site.register(CourseSchedules)
admin.site.register(Notification)