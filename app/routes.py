from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .database import get_db
from .models import UserPlan
from .gemini import generate_workout_plan, generate_nutrition_tip

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: str = Form(""),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        workout_plan = generate_workout_plan(
            name,
            age,
            weight,
            goal,
            intensity
        )

        nutrition_tip = generate_nutrition_tip(
            age,
            goal
        )

    except Exception:
        workout_plan = """
DAY 1
Workout: Light walking and stretching
Duration: 20 minutes

DAY 2
Workout: Bodyweight exercises and easy walking
Duration: 20 minutes

DAY 3
Workout: Stretching and mobility exercises
Duration: 15-20 minutes

DAY 4
Workout: Light cardio and simple strength exercises
Duration: 20 minutes

DAY 5
Workout: Walking and flexibility exercises
Duration: 20 minutes

DAY 6
Workout: Simple full-body activity
Duration: 20 minutes

DAY 7
Workout: Rest and gentle stretching
Duration: 10-15 minutes

SAFETY NOTE:
Start slowly, stay hydrated, and take rest when needed.
"""

        nutrition_tip = """
1. Eat balanced meals with different food groups.
2. Include fruits and vegetables regularly.
3. Include healthy protein sources in your meals.
4. Drink enough water throughout the day.
5. Get enough sleep and allow time for recovery.

These are general wellness tips, not medical advice.
"""

    new_plan = UserPlan(
        name=name,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": new_plan
        }
    )


@router.get("/users", response_class=HTMLResponse)
async def view_users(
    request: Request,
    db: Session = Depends(get_db)
):
    users = (
        db.query(UserPlan)
        .order_by(UserPlan.id.desc())
        .all()
    )

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "users": users
        }
    )


@router.get("/health")
async def health():
    return {
        "status": "running",
        "application": "FitBuddy"
    }