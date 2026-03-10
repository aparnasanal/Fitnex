from django.urls import path
from UserApp import views
from allauth.account import views as allauth_views

urlpatterns = [
  path('', views.user_login, name="login"),
  path('home/', views.homepage, name="home"),

  path('login/', views.user_login, name="login"),
  path('logout/', views.user_logout, name="logout"),

  path('signup/', views.signup, name="signup"),

  path('profile_setup/', views.profile_setup, name="profile_setup"),


  path('contact/', views.contact, name="contact"),
  path('save_message/', views.save_message, name="save_message"),
  
  path('chatbot/', views.chatbot, name="chatbot"),
]