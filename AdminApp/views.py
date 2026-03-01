from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from AdminApp.models import *
from UserApp.models import *

# Create your views here.

def dashboard(request):
  return render(request, "dashboard.html")

def admin_loginpage(request):
  return render(request, "admin_loginpage.html")

def admin_login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        if User.objects.filter(username__contains=uname).exists():
            user = authenticate(username=uname, password=passw)

            if user is not None:
                login(request, user)
                request.session['username'] = uname
                request.session['password'] = passw
                return redirect(dashboard)
            else:
                return redirect(admin_loginpage)
        else:
            return redirect(admin_loginpage)


def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_loginpage)


#_________________________________________________________________________________________________________________________________


def add_muscle(request):
  return render(request, "add_muscle_group.html")

def save_muscle(request):
  if request.method=="POST":
    m_name = request.POST.get('mname')
    m_img = request.FILES['mimg']

    obj = MuscleDb(M_Name=m_name, M_Image=m_img)
    obj.save()

    return redirect(add_muscle)
  
def view_muscle(request):
  muscles = MuscleDb.objects.all()
  return render(request, "view_muscle.html",
                {"mus" : muscles})

def view_message(request):
   msg = ContactDb.objects.all()
   return render(request, "view_messages.html", {"msg" : msg})