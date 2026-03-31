from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from AdminApp.models import *
from UserApp.models import *
from WorkoutApp.models import *
from DietApp.models import *
from ProgressApp.models import *

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Max

# Create your views here.

def dashboard(request):
   
   #------------------------- users card ----------------------------
  total_users = User.objects.count()
  
  two_days_ago = timezone.now() - timedelta(days=2)
  active_users = ProfileDb.objects.filter(user__last_login__gte=two_days_ago).count()
  
  five_days_ago = timezone.now() - timedelta(days=5)
  new_signups = User.objects.filter(date_joined__gte=five_days_ago).count()
  
  incomplete_profiles = ProfileDb.objects.filter(Age__isnull=True) | ProfileDb.objects.filter(
         Weight__isnull=True) | ProfileDb.objects.filter(Height__isnull=True) | ProfileDb.objects.filter(
        Goal__isnull=True) | ProfileDb.objects.filter(Activity_level__isnull=True)
  incomplete_count = incomplete_profiles.count()
  
  today = timezone.now().date()
  workouts_today = WorkoutLog.objects.filter(date_logged__date=today).count()
  
  #-------------- chart ----------------------------------------
  
  today = timezone.now().date()
  seven_days_ago = today - timedelta(days=6) 
  
  labels = [(today - timedelta(days=i)).strftime("%d %b") for i in reversed(range(7))]   
  
  # Users active per day
  active_users_counts = []
  for i in reversed(range(7)):
     day = today - timedelta(days=i)
     count = User.objects.filter(last_login__date=day).count()
     active_users_counts.append(count)

   # New signups per day
  new_signups_counts = []
  for i in reversed(range(7)):
     day = today - timedelta(days=i)
     count = User.objects.filter(date_joined__date=day).count()
     new_signups_counts.append(count)

   # Workouts logged per day
  workouts_counts = []
  for i in reversed(range(7)):
     day = today - timedelta(days=i)
     count = WorkoutLog.objects.filter(date_logged__date=day).count()
     workouts_counts.append(count)
     
     # ------------------------ Table -------------------------
     
  recent_signups = User.objects.order_by('-date_joined')[:5]
  recent_workouts = WorkoutLog.objects.select_related('user', 'workout').order_by('-date_logged')[:5]
  
  # --------------------- Top workouts --------------------------
  top_workouts_raw = (
    WorkoutLog.objects.values('workout__Name')
    .annotate(total_logged=Count('id'))
    .order_by('-total_logged')[:5]
)
  
  max_count = max([w['total_logged'] for w in top_workouts_raw], default=1)

  top_workouts = []
  for w in top_workouts_raw:
      width = int((w['total_logged'] / max_count) * 100)  # scale to 0-100%
      top_workouts.append({
        'workout__Name': w['workout__Name'],
        'total_logged': w['total_logged'],
        'bar_width': width,
    })
      
  
  context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_signups': new_signups,
        'incomplete_profiles': incomplete_count,
        'workouts_today': workouts_today,
        # chart
        'labels': labels,
        'active_users_counts': active_users_counts,
        'new_signups_counts': new_signups_counts,
        'workouts_counts': workouts_counts,
        'total_users': User.objects.count(),
        'active_users': sum(active_users_counts),
        'new_signups': sum(new_signups_counts),
        'workouts_today': WorkoutLog.objects.filter(date_logged__date=today).count(),
        # table
        'recent_signups': recent_signups,
        'recent_workouts': recent_workouts,
        # top workouts
        'top_workouts' : top_workouts,
    }

  return render(request, "dashboard.html", context)

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
                messages.warning(request, "Username Does'nt Exist")
                return redirect(admin_loginpage)
        else:
            messages.warning(request, "Invalid Username or Password")
            return redirect(admin_loginpage)


def admin_logout(request):
    request.session.pop('username', None)
    request.session.pop('password', None)
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

#--------------------------------------------------------------------------------------------------------

def view_users(request):
    users = User.objects.select_related('profiledb').annotate(
    total_workouts=Count('logs'),
    last_workout=Max('logs__date_logged')
)
    subscribers = ProfileDb.objects.filter(is_subscribed=True).select_related('user')
    total_subscribers = subscribers.count()
    
    return render(request, 'view_users.html', {'users': users, 'subscribers':subscribers, 'total_subscribers' : total_subscribers})
 
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect(view_users)
 
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    logs = user.logs.select_related('workout','progress').order_by('-date_logged')
    return render(request, 'user_detail.html', {'user': user, 'logs': logs})