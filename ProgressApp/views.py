from django.shortcuts import render, redirect
from AdminApp.models import *
from ProgressApp.models import *
from UserApp.models import *
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

def add_progress(request):
  workouts = WorkoutDb.objects.all().order_by('?')
  return render(request, "add_progress.html", {"workouts" : workouts})

@login_required
def save_progress(request):

    if request.method == "POST":

        date = request.POST.get('date')
        weight = request.POST.get('bodyweight')
        body_fat = request.POST.get('bodyfat')
        user = request.POST.get('user')

        progress = ProgressDb.objects.create(user=request.user, date=date, body_weight=weight, body_fat=body_fat)
        workouts = request.POST.getlist('workout[]')
        weight = request.POST.getlist('weight[]')
        reps = request.POST.getlist('reps[]')
        sets = request.POST.getlist('sets[]')

        for i in range(len(workouts)):

            if workouts[i]:

                WorkoutLog.objects.create(
                    user=request.user, progress=progress, workout_id=workouts[i], weight=weight[i] if weight[i] else None,
                    reps=reps[i] if reps[i] else None, sets=sets[i] if sets[i] else None)

        return redirect('progress_dashboard')

def progress_dashboard(request):
    # Get user profile
    profile = ProfileDb.objects.get(user=request.user)
    goal = profile.Goal  # Fat Loss, Muscle Gain, Maintenance

    # Get all progress entries for the user, ordered by date
    progress_entries = ProgressDb.objects.filter(user=request.user).order_by("date")

    # Prepare lists for charts
    dates = []
    weights = []
    body_fats = []

    for p in progress_entries:
        if p.date:
            dates.append(p.date.strftime("%Y-%m-%d"))
        if p.body_weight is not None:
            weights.append(float(p.body_weight))
        if p.body_fat is not None:
            body_fats.append(float(p.body_fat))

    # Weight progress interpretation
    weight_status = "Not enough data yet."
    weight_color = "#ffffff"  # default neutral color
    fat_status = "Not enough data yet."
    fat_color = "#ffffff"
    
    if len(weights) >= 2:
        start = weights[0]
        end = weights[-1]

        if goal == "Fat Loss":
            weight_status = "Great! Your weight is decreasing 📉" if end < start else "Weight increased. Adjust diet/workout."
            weight_color = "#3EFFC1" if weights[-1] < weights[0] else "#ff4c4c"
        elif goal == "Muscle Gain":
            weight_status = "Great! You're gaining weight 💪" if end > start else "Weight not increasing yet."
            weight_color = "#3EFFC1" if weights[-1] > weights[0] else "#ff4c4c"
        elif goal == "Maintenance":
            weight_status = "Perfect! Weight maintained ⚖️" if abs(end-start) <= 1 else "Weight fluctuating."
            weight_color = "#3EFFC1" if abs(weights[-1]-weights[0]) <= 1 else "#ff4c4c"

    # Body fat progress interpretation
    fat_status = ""
    if len(body_fats) >= 2:
        start_fat = body_fats[0]
        end_fat = body_fats[-1]
        if goal == "Fat Loss":
            fat_status = "Body fat decreasing ✅" if end_fat < start_fat else "Body fat not decreasing. Adjust diet."
            fat_color = "#3EFFC1" if body_fats[-1] < body_fats[0] else "#ff4c4c"
        elif goal == "Muscle Gain":
            fat_status = "Body fat stable or slightly increasing 💪" if end_fat >= start_fat else "Body fat decreasing unexpectedly."
            fat_color = "#3EFFC1" if body_fats[-1] >= body_fats[0] else "#ff4c4c"
        elif goal == "Maintenance":
            fat_status = "Body fat maintained ⚖️" if abs(end_fat-start_fat) <= 1 else "Body fat fluctuating."
            fat_color = "#3EFFC1" if abs(body_fats[-1]-body_fats[0]) <= 1 else "#ff4c4c"

    # Strength chart data
    logs = WorkoutLog.objects.filter(progress__user=request.user).order_by("progress__date")
    strength_labels = []
    strength_data = []

    for log in logs:
        label = f"{log.workout.Name} ({log.progress.date.strftime('%Y-%m-%d')})"
        strength_labels.append(label)
        strength_data.append(log.weight)
  

    # Prepare context for template
    context = {
        "dates": json.dumps(dates),
        "weights": json.dumps(weights),
        "body_fats": json.dumps(body_fats),
        "goal": goal,
        "weight_status": weight_status,
        "fat_status": fat_status,
        "weight_color": weight_color,
        "fat_color": fat_color,
        "strength_labels": json.dumps(strength_labels),
        "strength_data": json.dumps(strength_data),
    }

    return render(request, "progress_view.html", context)