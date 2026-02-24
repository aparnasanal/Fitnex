from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileDb(models.Model):
  GOAL_CHOICES = [
        ('fat_loss', 'Fat Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance'),
    ]

  GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

  ACTIVITY_LEVEL = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly Active'),
        ('moderate', 'Moderately Active'),
        ('active', 'Very Active'),
    ]

  EXPERIENCE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

  User = models.OneToOneField(User, on_delete=models.CASCADE)
  
  Name = models.CharField(max_length=100)
  Age = models.IntegerField()
  Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

  Height = models.FloatField(help_text="Height in cm")
  Weight = models.FloatField(help_text="Weight in kg")
  Target_weight = models.FloatField(null=True, blank=True)

  Goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
  Activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL)
  Experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL)

  def __str__(self):
        return self.user.username