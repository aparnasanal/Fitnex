from django.urls import path
from AdminApp import views

urlpatterns = [
  path('dashboard/', views.dashboard, name="dashboard"),
  path('admin_loginpage/', views.admin_loginpage, name="admin_loginpage"),
  path('admin_login/', views.admin_login, name="admin_login"),
  path('admin_logout/', views.admin_logout, name="admin_logout"),

  path('add_msucle', views.add_muscle, name="add_muscle"),
  path('save_muscle', views.save_muscle, name="save_muscle"),
  path('view_muscle', views.view_muscle, name="view_muscle"),
]