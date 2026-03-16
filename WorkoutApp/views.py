from django.shortcuts import render, redirect
from AdminApp.models import *
from UserApp.models import *
from WorkoutApp.ai_workout import get_ai_workout_plan
from django.core.paginator import Paginator
from django.db.models import Q

import os
import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from AdminApp.models import WorkoutDb

# Create your views here.

def workout_videos(request):

    workouts = WorkoutDb.objects.all()
    muscle = MuscleDb.objects.all()
    query = request.GET.get('q')

    if query:
        workouts = workouts.filter(
            Q(Name__icontains=query) |
            Q(Muscle_Group__icontains=query) |
            Q(Description__icontains=query)
        )
    else:
        workouts = workouts.order_by('?')  

    paginator = Paginator(workouts, 12)  
    page_number = request.GET.get('page')
    workout = paginator.get_page(page_number)

    return render(request, "workout_videos.html", {
        "workout": workout,
        "muscle": muscle,
        "query": query
    })
def filtered_workout(request, m_name):
  workouts = WorkoutDb.objects.filter(Muscle_Group__iexact=m_name)
  query = request.GET.get('q')
  
  if query:
    workouts=workouts.filter(
      Q(Name__icontains=query) |
      Q(Description__icontains=query)
    )
    
  return render(request, "filtered_workout.html", {"workouts" : workouts, 'Muscle_Group': m_name,
                                                    "query" : query})


def ai_suggestions(request):
    profile = request.user.profiledb 
    subscription_active = request.user.profiledb.subscription_active()
    
    context = {
        "profile": profile,
        "subscription_active": subscription_active
    }
    
    if not subscription_active:
        return render(request, "ai_suggestions.html", context)
    
    workouts = get_ai_workout_plan(profile)
    context["workouts"] = workouts

    return render(request, "ai_suggestions.html", context)
  
def download_videos(request, muscle):
    
    videos = WorkoutDb.objects.filter(Muscle_Group=muscle)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for video in videos:
            video_path = video.Video.path 
            filename = os.path.basename(video_path)

            zip_file.write(video_path, filename)

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{muscle}_workouts.zip"'

    return response