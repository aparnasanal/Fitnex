from django.urls import path
from ProgressApp import views

urlpatterns = [
  path('add_progress/', views.add_progress, name="add_progress"),
  path('save_progress/', views.save_progress, name="save_progress"),
  path('dashboard/', views.progress_dashboard, name="dashboard"),
]