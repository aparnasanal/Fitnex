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
import os
from dotenv import load_dotenv
from datetime import date, timedelta
from django.conf import settings
import razorpay


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
  profile = request.user.profiledb
  remaining_days = None
  if request.user.is_authenticated:
        profile, created = ProfileDb.objects.get_or_create(user=request.user)
        if not is_profile_complete(profile):
          messages.warning(request, "Please complete your profile.")
          return redirect('profile_setup')
  if profile.is_subscribed and profile.subscription_expiry:
        remaining_days = (profile.subscription_expiry - date.today()).days
        if remaining_days <= 0:
            profile.is_subscribed = False
            profile.subscription_expiry = None
            profile.save()
            remaining_days = None
        
  return render(request, "home.html", {"muscle" : muscle, "remaining_days": remaining_days, "profile": profile})

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
      
#--------------------------------------------------------------------------------------------------------------------------

@login_required
def subscribe(request):
    profile = request.user.profiledb

    # Render the payment page even on GET
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order_amount = 49900  # ₹499 in paise
    order_currency = 'INR'
    order_receipt = f"order_rcptid_{request.user.id}"

    razorpay_order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'notes': {'plan': 'AI Fitness Subscription'}
    })

    context = {
        'order_id': razorpay_order['id'],
        'amount': order_amount,
        'key_id': settings.RAZORPAY_KEY_ID,
        'profile': profile
    }
    return render(request, "subscribe_payment.html", context)

@csrf_exempt
@login_required
def subscribe_success(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = request.user.profiledb
        profile.is_subscribed = True
        profile.subscription_expiry = date.today() + timedelta(days=30)
        profile.save()
        return JsonResponse({"message": "Payment successful! Subscription activated."})
    return JsonResponse({"error": "Invalid request"}, status=400)


#--------------------------------------------------------------------------------------------------------------

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@csrf_exempt
@login_required
def chatbot(request):
    if request.method == "POST":
        try:
            profile = request.user.profiledb

            if not profile.subscription_active():
                return JsonResponse({
                    "reply": "Subscribe to access chatbot.."
                })

            data = json.loads(request.body)
            message = data.get("message", "").strip()

            if not message:
                return JsonResponse({"reply": "Please type a message."})

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful fitness and gym expert. "
                            "Answer only questions related to workouts, nutrition, exercises, and healthy lifestyle. "
                            "If the question is unrelated, politely say you can only answer fitness related questions."
                        )
                    },
                    {"role": "user", "content": message}
                ]
            }

            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(OPENROUTER_URL, json=payload, headers=headers)
            result = response.json()

            if "error" in result:
                reply = f"API Error: {result['error']['message']}"
            elif "choices" in result:
                reply = result["choices"][0]["message"]["content"]
            elif "output" in result:
                reply = result["output"][0]["content"]
            else:
                reply = "Sorry, I could not get a response."

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"error": "Invalid request"}, status=400)