from django.shortcuts import render, redirect
from AdminApp.models import *

# Create your views here.

def workout_videos(request):
  workout = WorkoutDb.objects.all().order_by('?')
  return render(request, "workout_videos.html", {"workout" : workout})

def filtered_workout(request, m_name):
  workouts = WorkoutDb.objects.filter(Muscle_Group__iexact=m_name)
  return render(request, "filtered_workout.html", {"workouts" : workouts, 'Muscle_Group': m_name})
