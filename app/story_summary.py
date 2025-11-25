from fastapi import APIRouter
from app.db import SessionLocal
from app.models import Comment
from app.story_logic import (
    generate_fluent_paragraph,
    get_cultural_events,
    detect_region  # ✅ NEW: import region detection
)
from story_generator import generate_story
from collections import Counter
from datetime import datetime

router = APIRouter()

def load_comments():
    session = SessionLocal()
    comments = session.query(Comment).all()
    session.close()
    return [
        {
            "user_id": c.user_id,
            "text": c.content,
            "emotion": c.emotion,
            "tone": c.tone,
            "tags": c.tags.split(",") if c.tags else [],
            "idioms": c.idioms.split(",") if c.idioms else []
        }
        for c in comments
    ]

@router.get("/story-summary")
def get_story_summary():
    comments = load_comments()

    tag_counts = Counter(tag for c in comments for tag in c["tags"])
    emotion_counts = Counter(c["emotion"] for c in comments if c["emotion"])
    tone_counts = Counter(c["tone"] for c in comments if c["tone"])
    all_tags = set(tag for c in comments for tag in c["tags"])
    all_idioms = set(idiom for c in comments for idiom in c["idioms"])

    theme_map = {
        "community": {"jamii", "harambee", "mtaa", "voice"},
        "innovation": {"jua kali", "matatu", "maendeleo"},
        "leadership": {"uhuru", "umoja", "shujaa"}
    }
    themes = [theme for theme, keywords in theme_map.items() if keywords & all_tags] or ["community"]

    top_tag = tag_counts.most_common(1)[0][0] if tag_counts else "local life"
    story_paragraph = generate_story(top_tag)

    metadata = {
        "tone": tone_counts.most_common(1)[0][0] if tone_counts else "reflective",
        "emotion": emotion_counts.most_common(1)[0][0] if emotion_counts else "neutral",
        "tags": list(all_tags),
        "themes": themes,
        "idioms": list(all_idioms),
        "events": get_cultural_events(datetime.utcnow().month),
        "region": detect_region(all_tags)  # ✅ NEW: add region to metadata
    }
    metadata["paragraphs"] = generate_fluent_paragraph(metadata, count=3)

    return {
        "title": "Echoed Voices",
        "summary": f"Generated from {len(comments)} comments",
        "emotion": metadata["emotion"],
        "tone": metadata["tone"],
        "themes": metadata["themes"],
        "region": metadata["region"],  # ✅ NEW: include region in response
        "tag_cloud": [{"tag": tag, "count": count} for tag, count in tag_counts.items()],
        "story": story_paragraph,
        "tags": metadata["tags"],
        "idioms": metadata["idioms"],
        "events": metadata["events"],
        "paragraphs": metadata["paragraphs"]
    }
