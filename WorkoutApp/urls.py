from django.urls import path
from WorkoutApp import views

urlpatterns = [
  path('workout_videos/', views.workout_videos, name="workout_videos"),
  path('filtered_workout/<m_name>/', views.filtered_workout, name="filtered_workout"),
  path('ai_suggestions/', views.ai_suggestions, name="ai_suggestions"),
]