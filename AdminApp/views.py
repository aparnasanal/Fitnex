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

def view_message(request):
   msg = ContactDb.objects.all()
   return render(request, "view_messages.html", {"msg" : msg})


#--------------------------------MUSCLE GROUPS--------------------------------


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

def edit_muscle(request, m_id):
   muscle = MuscleDb.objects.get(id=m_id)
   return render(request, "edit_muscle.html", {"muscle" : muscle})

def update_muscle(request, mus_id):
   if request.method == "POST":
      m_name = request.POST.get('mname')
      try:
        m_img = request.FILES['mimg']
        fs = FileSystemStorage()
        file = fs.save(m_img.name, m_img) 
        MuscleDb.objects.filter(id=mus_id).update(M_Name=m_name, M_Image=file) 
         
      except MultiValueDictKeyError:
        MuscleDb.objects.filter(id=mus_id).update(M_Name=m_name) 

      return redirect(view_muscle)      

def delete_muscle(request, m_id):
   muscle = MuscleDb.objects.filter(id=m_id)
   muscle.delete()

   return redirect(view_muscle)


#--------------------------------WORKOUT--------------------------------

def add_workout(request):
   muscle = MuscleDb.objects.all()
   return render(request, "add_workout.html",
                 {"muscle" : muscle})


def save_workout(request):
   if request.method == "POST":
      name = request.POST.get('name')
      muscle = request.POST.get('m_group')
      description = request.POST.get('description')
      video = request.FILES['video']

      obj = WorkoutDb(Name=name, Muscle_Group=muscle, Description=description, Video=video)
      obj.save()
      
      return redirect(add_workout)

def view_workout(request):
   videos = WorkoutDb.objects.all()
   return render(request, "view_workout.html", {"videos" : videos})


def edit_workout(request, w_id):
   workout = WorkoutDb.objects.get(id=w_id)
   muscles = MuscleDb.objects.all()
   return render(request, "edit_workout.html", {"workout" : workout, "muscles" : muscles})

def update_workout(request, work_id):
   if request.method == "POST":
      name = request.POST.get('name')
      muscle = request.POST.get('m_group')
      description = request.POST.get('description')
      try:
         video = request.FILES['video']
         fs = FileSystemStorage()
         file = fs.save(video.name, video)
         WorkoutDb.objects.filter(id=work_id).update(Name=name, Muscle_Group=muscle, Description=description, Video=file)
      except MultiValueDictKeyError:
         WorkoutDb.objects.filter(id=work_id).update(Name=name, Muscle_Group=muscle, Description=description)
      
      return redirect(view_workout)

def delete_workout(request, w_id):
   workout = WorkoutDb.objects.filter(id=w_id)
   workout.delete()

   return redirect(view_workout)