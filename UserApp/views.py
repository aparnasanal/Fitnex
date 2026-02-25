from django.shortcuts import render, redirect


def homepage(request):
  return render(request, "home.html")

def login(request):
  return render(request, "login.html")

def signup(request):
  return render(request, "signup.html")



