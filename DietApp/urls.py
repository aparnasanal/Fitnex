from django.urls import path
from DietApp import views

urlpatterns = [
  path('diet/', views.diet_engine, name="diet"),
]