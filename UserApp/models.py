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

  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiledb')
  
  Age = models.IntegerField(null=True, blank=True)
  Gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

  Height = models.FloatField(help_text="Height in cm", null=True, blank=True)
  Weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
  Target_weight = models.FloatField(null=True, blank=True)

  Goal = models.CharField(max_length=20, choices=GOAL_CHOICES, null=True, blank=True)
  Activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL, null=True, blank=True)
  Experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL, null=True, blank=True)
  
  is_subscribed = models.BooleanField(default=False)
  subscription_expiry = models.DateField(null=True, blank=True)

  def subscription_active(self):
        return self.is_subscribed and self.subscription_expiry and self.subscription_expiry >= date.today()

  def __str__(self):
        return self.user.username
  

class ContactDb(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Subject = models.CharField(max_length=200)
    Message = models.TextField()