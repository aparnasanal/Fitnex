from django.shortcuts import render, redirect
from AdminApp.models import *
from ProgressApp.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def add_progress(request):
  workouts = WorkoutDb.objects.all().order_by('?')
  return render(request, "add_progress.html", {"workouts" : workouts})

@login_required
def save_progress(request):

    if request.method == "POST":

        date = request.POST.get('date')
        weight = request.POST.get('bodyweight')
        body_fat = request.POST.get('bodyfat')

        progress = ProgressDb.objects.create(user=request.user, date=date, body_weight=weight, body_fat=body_fat)

        workouts = request.POST.getlist('workout[]')
        weight = request.POST.getlist('weight[]')
        reps = request.POST.getlist('reps[]')
        sets = request.POST.getlist('sets[]')

        for i in range(len(workouts)):

            if workouts[i]:

                WorkoutLog.objects.create(
                    progress=progress, workout_id=workouts[i], weight=weight[i] if weight[i] else None,
                    reps=reps[i] if reps[i] else None, sets=sets[i] if sets[i] else None)

        return redirect('home')