from django.shortcuts import render, redirect
from AdminApp.models import *
from UserApp.models import *
from WorkoutApp.ai_workout import get_ai_workout_plan
from django.core.paginator import Paginator

import os
import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from AdminApp.models import WorkoutDb

# Create your views here.

def workout_videos(request):
  workout_list = WorkoutDb.objects.all().order_by('?')
  muscle = MuscleDb.objects.all()
  paginator = Paginator(workout_list, 12)   # 12 videos per page

  page_number = request.GET.get('page')
  workout = paginator.get_page(page_number)
  return render(request, "workout_videos.html", {"workout" : workout, "muscle" : muscle})

def filtered_workout(request, m_name):
  workouts = WorkoutDb.objects.filter(Muscle_Group__iexact=m_name)
  return render(request, "filtered_workout.html", {"workouts" : workouts, 'Muscle_Group': m_name})


def ai_suggestions(request):
    profile = request.user.profiledb 
    workouts = get_ai_workout_plan(profile)

    return render(request, "ai_suggestions.html", {"workouts": workouts})
  
def download_videos(request, muscle):
    
    videos = WorkoutDb.objects.filter(Muscle_Group=muscle)

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for video in videos:
            video_path = video.Video.path   # FileField path
            filename = os.path.basename(video_path)

            zip_file.write(video_path, filename)

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{muscle}_workouts.zip"'

    return response