import django_filters 
from .models import *


class CoursesFilter(django_filters.FilterSet) : 
    class Meta : 
        model= Courses 
        fields=['id', 'name', 'instructor']

class StudentsFilter(django_filters.FilterSet) : 
    class Meta : 
        model= Student
        fields=['first_name', 'last_name']
