# backend/app/story.py
from fastapi import APIRouter
from pydantic import BaseModel
from story_generator import generate_story
from app.story_logic import generate_fluent_paragraph  # centralized import

router = APIRouter()

class TagRequest(BaseModel):
    tag: str

@router.post("/story")
def get_story(request: TagRequest):
    story = generate_story(request.tag)

    # Add fluent paragraphs if metadata is present
    if isinstance(story, dict) and all(k in story for k in ["tone", "emotion", "tags", "themes", "idioms"]):
        story["paragraphs"] = generate_fluent_paragraph(story, count=3)

    return {"tag": request.tag, "story": story}
