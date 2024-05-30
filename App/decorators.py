from django.shortcuts import redirect

def notLoggedUser(view_func):
    def wrapper_func(request, *args, **kwargs) :
        if request.user.is_authenticated:
            return redirect('home') 
        else :
           return view_func(request,*args, **kwargs) 
    return wrapper_func

def forAdmins(view_func):
    def wrapper_func(request, *args, **kwargs): 
        group = None  
        if request.user.groups.exists():
            group= request.user.groups.all()[0].name 
        if group =='admin' : 
            return view_func(request,*args, **kwargs)  
        if group =="student":  
            return redirect('myCourses') 
        else:
            return #
    return wrapper_func 

def forStudents(view_func):
    def wrapper_func(request, *args, **kwargs): 
        group = None  
        if request.user.groups.exists():
            group= request.user.groups.all()[0].name 
        if group =='student' : 
            return view_func(request,*args, **kwargs)  
        if group =="admin":  
            return redirect('home') 
        else:
            return #
    return wrapper_func 
