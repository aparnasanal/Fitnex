from django.urls import path
from DietApp import views

urlpatterns = [
  path('', views.diet_engine, name="diet"),
]