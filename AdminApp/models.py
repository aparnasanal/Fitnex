from django.db import models

# Create your models here.

class MuscleDb(models.Model):
  M_Name = models.CharField(max_length=100)
  M_Image = models.ImageField(upload_to="Muscle Groups")

class WorkoutDb(models.Model):
  Name = models.CharField(max_length=100)
  Muscle_Group = models.CharField(max_length=100)
  Description = models.TextField()
  Video = models.FileField(upload_to="Workout Videos")