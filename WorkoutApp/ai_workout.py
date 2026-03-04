from openai import OpenAI
from django.conf import settings
import json
import re
from AdminApp.models import WorkoutDb

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def clean_json(text):
    """
    Removes markdown or unwanted text around JSON
    """
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    text = text.strip()
    return text


def get_ai_workout_plan(profile):

    age = profile.Age or 25
    experience_level = profile.Experience_level or "Beginner"
    fitness_goal = profile.Goal or "Muscle Gain"

    if experience_level.lower() == "beginner":
        split_rule = """
Beginner Split:
Day 1 - Chest
Day 2 - Back
Day 3 - Legs
Day 4 - Shoulders
Day 5 - Arms
Day 6 - Core
"""
    else:
        split_rule = """
Advanced Split (Push Pull Legs):
Day 1 - Push
Day 2 - Pull
Day 3 - Legs
Day 4 - Push variation
Day 5 - Pull variation
Day 6 - Legs variation
"""

    prompt = f"""
Create a 6 day gym workout plan.

User:
Age: {age}
Goal: {fitness_goal}
Experience: {experience_level}

{split_rule}

Rules:
- EXACTLY 6 exercises per day
- Very short descriptions (max 10 words)
- Return STRICT JSON only
- No explanations
- No markdown

Format:
{{
  "Day 1": [{{"name":"","muscle_group":"","description":"","experience_level":"{experience_level}"}}],
  "Day 2": [],
  "Day 3": [],
  "Day 4": [],
  "Day 5": [],
  "Day 6": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200,
        )

        raw_output = response.choices[0].message.content
        cleaned = clean_json(raw_output)
        full_plan = json.loads(cleaned)

    except Exception as e:
        print("AI Workout JSON failed:", e)

        # Emergency fallback
        full_plan = {
            f"Day {i}": [
                {
                    "name": "Push-Up",
                    "muscle_group": "Chest",
                    "description": "Standard push-ups",
                    "experience_level": experience_level
                }
                for _ in range(6)
            ]
            for i in range(1, 8)
        }

    # Attach DB video URLs
    for day, exercises in full_plan.items():
        for ex in exercises:
            db_match = WorkoutDb.objects.filter(
                Name__icontains=ex.get("name", "")
            ).first()
            ex["video_url"] = db_match.Video.url if db_match else None

    return full_plan