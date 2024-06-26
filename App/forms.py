from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User


class CourseForm(ModelForm):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'description', 'prerequisites', 'instructor', 'capacity'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prerequisites'].queryset = Courses.objects.all()

class CourseScheduleForm(ModelForm):
    class Meta:
        model = CourseSchedules
        fields = ['startTime', 'endTime', 'days', 'roomNo'] 
   