from django.shortcuts import render,redirect
from .ai_engine import generate_ai_diet
from UserApp.models import ProfileDb
from django.contrib.auth.decorators import login_required
from django.contrib import messages

activity_multipliers = {
    'Sedentary': 1.2,
    'Light': 1.375,
    'Moderate': 1.55,
    'Active': 1.725,
} 

@login_required
def diet_engine(request):
  profile = ProfileDb.objects.get(user=request.user)

  if not profile.Age or not profile.Height or not profile.Weight:
    messages.error(request, "Complete profile first")
    return redirect('profile_setup')
  activity_multiplier = activity_multipliers.get(profile.Activity_level)
  if not activity_multiplier:
    messages.error(request, "Select activity level")
    return redirect('profile_setup')

  if profile.Gender == "male":
    bmr = (10 * profile.Weight) + (6.25 * profile.Height) - (5 * profile.Age) + 5
  else:
    bmr = (10 * profile.Weight) + (6.25 * profile.Height) - (5 * profile.Age) - 161

  
  tdee = bmr * activity_multipliers[profile.Activity_level]

  if profile.Goal == 'fat_loss':
        calories = tdee - 500
  elif profile.Goal == 'muscle_gain':
      calories = tdee + 300
  else:
      calories = tdee

  ai_diet = generate_ai_diet(profile, calories)

  return render(request, "diet.html", {
      "diet_plan": ai_diet,
      "calories": round(calories)
  })