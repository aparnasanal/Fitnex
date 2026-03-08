from django.db import models
from django.contrib.auth.models import User
from AdminApp.models import WorkoutDb

# Create your models here.

class ProgressDb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    body_weight = models.FloatField()
    body_fat = models.FloatField(null=True, blank=True)
  
class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='logs')
    progress = models.ForeignKey(ProgressDb, on_delete=models.CASCADE)
    workout = models.ForeignKey(WorkoutDb, on_delete=models.CASCADE)
    date_logged = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    weight = models.FloatField()
    reps = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
  
