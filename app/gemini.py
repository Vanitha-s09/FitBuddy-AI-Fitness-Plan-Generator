import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. "
        "Please add your Gemini API key to the .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_workout_plan(name, age, weight, goal, intensity):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe and practical 7-day general fitness plan.

User details:
Name: {name}
Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

Requirements:
1. Create a 7-day plan.
2. Label Day 1 to Day 7.
3. Include simple exercises.
4. Include rest or recovery.
5. Mention approximate duration.
6. Keep the language simple.
7. Do not recommend extreme exercise.
8. Do not recommend starvation or crash diets.
9. Do not provide medical diagnosis.
10. For users under 18, focus on healthy activity,
sleep, hydration and balanced meals rather than weight loss.

Format:

DAY 1
Workout:
Duration:

DAY 2
Workout:
Duration:

DAY 3
Workout:
Duration:

DAY 4
Workout:
Duration:

DAY 5
Workout:
Duration:

DAY 6
Workout:
Duration:

DAY 7
Workout:
Duration:

SAFETY NOTE:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_nutrition_tip(age, goal):

    prompt = f"""
You are FitBuddy, a general wellness assistant.

Age: {age}
Fitness goal: {goal}

Give 5 simple nutrition and recovery tips.

Include:
- Balanced meals
- Fruits and vegetables
- Protein sources
- Hydration
- Sleep and recovery

Do not recommend:
- Starvation
- Crash diets
- Extreme calorie restriction
- Dangerous supplements

Keep the language simple.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text