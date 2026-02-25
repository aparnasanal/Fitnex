from django.urls import path
from UserApp import views

urlpatterns = [
  path('home/', views.homepage, name="home"),
  path('login/', views.login, name="login"),
  path('signup/', views.signup, name="signup"),
]