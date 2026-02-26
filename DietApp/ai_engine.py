from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def generate_ai_diet(profile, calories):

  prompt = f"""
  Create a personalised Indian diet plan.

  User Details:
  Age : {profile.Age}
  Gender : {profile.Gender}
  Height : {profile.Height} cm
  Weight : {profile.Weight} kg
  Goal : {profile.Goal}
  Activity Level : {profile.Activity_level}
  Daily Calorie Target: {round(calories)} kcal

  Provide:
    - Breakfast
    - Lunch
    - Dinner
    - 2 Snacks
    - Macro breakdown
    - Total calories
    """
  
  response = client.chat.completions.create(
    model = "gpt-4.1-mini",
    messages = [
      {"role" : "system", "content" : "You are a certified nutritionist."},
      {"role" : "user", "content" : prompt}
    ],
    temperature = 0.7,
    max_tokens=800
  )

  return response.choices[0].message.content

