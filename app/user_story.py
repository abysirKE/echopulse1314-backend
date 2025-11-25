from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Comment
from app.story_logic import generate_fluent_paragraph

router = APIRouter()

@router.get("/story/{user_id}")
def get_user_story(user_id: int):
    session: Session = SessionLocal()
    comments = session.query(Comment).filter(Comment.user_id == user_id).all()
    session.close()

    if not comments:
        return {"message": f"No comments found for user {user_id}"}

    # Build metadata from this user's comments
    metadata = {
        "tone": comments[0].tone if comments[0].tone else "reflective",
        "emotion": comments[0].emotion if comments[0].emotion else "neutral",
        "tags": [c.tags for c in comments if c.tags],
        "themes": ["community", "progress"],  # you can expand this mapping later
        "idioms": [c.idioms for c in comments if c.idioms]
    }

    # Generate fluent bilingual paragraphs
    metadata["paragraphs"] = generate_fluent_paragraph(metadata, count=3)

    return {
        "user_id": user_id,
        "story": metadata
    }
