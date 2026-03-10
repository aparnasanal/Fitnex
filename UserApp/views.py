from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from AdminApp.models import *
from UserApp.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# profile completion
def is_profile_complete(profile):
    required_fields = [
        profile.Age,
        profile.Weight,
        profile.Target_weight,
        profile.Activity_level,
    ]
    return all(field is not None and field != "" for field in required_fields)

@login_required
def homepage(request):
  muscle = MuscleDb.objects.all()
  if request.user.is_authenticated:
        profile, created = ProfileDb.objects.get_or_create(user=request.user)
        if not is_profile_complete(profile):
          messages.warning(request, "Please complete your profile.")
          return redirect('profile_setup')
        
  return render(request, "home.html", {"muscle" : muscle})

def user_login(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)

      profile, _ = ProfileDb.objects.get_or_create(user=user)
      if not is_profile_complete(profile):
          messages.warning(request, "Please complete your profile.")
          return redirect('profile_setup')
      else:
        return redirect('home')
      
    else:
      messages.error(request, "Invalid Username or Password")
      return redirect('login')

  return render(request, "login.html")

def signup(request):
  if request.user.is_authenticated:
        profile, _ = ProfileDb.objects.get_or_create(user=request.user)
        if not is_profile_complete(profile):
            return redirect('profile_setup')
        return redirect('home')
  if request.method == "POST":
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if not username:
            messages.error(request, "Username can't be empty")
            return redirect('signup')
    
    if not email:
            messages.error(request, "Email can't be empty")
            return redirect('signup')
    
    if not password1:
        messages.error(request, "Enter a Password")
        return redirect('signup')

    if not password2:
        messages.error(request, "Enter Confirm Password")
        return redirect('signup')
    
    if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

    if User.objects.filter(username=username).exists():
      messages.error(request, "Username already taken")
      return redirect('signup')
    
    if User.objects.filter(email=email).exists():
      messages.error(request, "Email already exists")
      return redirect('signup')

    user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
    
    ProfileDb.objects.get_or_create(user=user)
    user = authenticate(request, username=username, password=password1)
    login(request, user)

    return redirect('profile_setup')
  
  return render(request, "signup.html")


@login_required
def profile_setup(request):

  profile = ProfileDb.objects.get_or_create(user=request.user)[0]

  if request.method == "POST":
      profile.Age = request.POST.get('age')
      profile.Gender = request.POST.get('gender')
      profile.Height = request.POST.get('height')
      profile.Weight = request.POST.get('weight')
      profile.Target_weight = request.POST.get('targetweight')
      profile.Goal = request.POST.get('goal')
      profile.Activity_level = request.POST.get('activity')
      profile.Experience_level = request.POST.get('experience')

      profile.save()

      return redirect('home')
      
  return render(request, "profile_setup.html")


def user_logout(request):
    logout(request)
    return redirect('login')


#_________________________________________________________________________________________________________________________

def contact(request):
    return render(request, "contact.html")
def save_message(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        obj = ContactDb(Name=name, Email=email, Subject=subject, Message=message)
        obj.save()

        return redirect(contact)
      
#___________________________________________________________________________________________________________

API_KEY = "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"

@csrf_exempt
def chatbot(request):

    if request.method == "POST":

        data = json.loads(request.body)
        message = data.get("message")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Gym Chatbot"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role":"system","content": "You are a fitness chatbot. Only answer questions about workouts, diet, muscles, and gym training."},
                    {"role":"user","content":message}
                    
                ]
            }
        )

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        return JsonResponse({"reply": reply})




