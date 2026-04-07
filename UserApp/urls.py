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
  path('edit_profile/', views.edit_profile, name="edit_profile"),


  path('contact/', views.contact, name="contact"),
  path('save_message/', views.save_message, name="save_message"),
  
  path('chatbot/', views.chatbot, name="chatbot"),
  path('subscribe/', views.subscribe, name="subscribe"),
  path('subscribe/success', views.subscribe_success, name="subscribe_success"),
  # path('subscribe/mock_success', views.mock_success, name="mock_success"),

]