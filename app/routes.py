# app/routes.py
from fastapi import APIRouter, Body
from app.auth import facebook_login
from app.db import SessionLocal
from app.models import Comment
from app.utils import generate_story_from_comments

from app.story_logic import (
    generate_fluent_paragraph,
    detect_themes,
    pick_proverbs,
    get_cultural_events
)
from datetime import datetime
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

router = APIRouter()

# --- Health & Auth ---
@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/login/facebook")
def login_with_facebook(token: str):
    return facebook_login(token)

# --- Comment Endpoints ---
@router.post("/comment")
def add_comment(user_id: int = Body(...), text: str = Body(...)):
    session = SessionLocal()
    new_comment = Comment(
        user_id=user_id,
        content=text,
        timestamp=datetime.utcnow()
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    session.close()
    return {"message": "Comment added", "id": new_comment.id}

@router.get("/comment")
def get_comments(user_id: int = None):
    session = SessionLocal()
    query = session.query(Comment)
    if user_id is not None:
        query = query.filter(Comment.user_id == user_id)
    comments = query.all()
    session.close()
    return {"comments": [{"id": c.id, "user_id": c.user_id, "text": c.content} for c in comments]}

@router.get("/comments/enriched")
def get_enriched_comments():
    session = SessionLocal()
    comments = session.query(Comment).all()
    session.close()
    return {
        "comments": [
            {
                "id": c.id,
                "user_id": c.user_id,
                "text": c.content,
                "emotion": c.emotion,
                "tone": c.tone,
                "tags": c.tags.split(",") if c.tags else [],
                "idioms": c.idioms.split(",") if c.idioms else []
            }
            for c in comments
        ]
    }

# --- Story Generation ---
@router.get("/generate_story")
def generate_story():
    session = SessionLocal()
    comments = session.query(Comment).filter(Comment.user_id == 1).all()
    story = generate_story_from_comments(comments)
    story["paragraphs"] = generate_fluent_paragraph(story, count=3)
    session.close()
    return {"story": story}

@router.get("/tag-cloud/{user_id}")
def user_tag_cloud(user_id: int):
    session = SessionLocal()
    comments = session.query(Comment).filter(Comment.user_id == user_id).all()
    session.close()

    tags = [tag for c in comments if c.tags for tag in c.tags.split(",")]
    tag_counts = Counter(tags)
    tag_cloud = [{"tag": tag, "count": count} for tag, count in tag_counts.items()]

    return {"user_id": user_id, "tag_cloud": tag_cloud}

@router.get("/community-analytics")
def community_analytics():
    session = SessionLocal()
    comments = session.query(Comment).all()
    session.close()

    enriched = [
        {
            "emotion": c.emotion,
            "tone": c.tone,
            "tags": c.tags.split(",") if c.tags else [],
            "idioms": c.idioms.split(",") if c.idioms else []
        }
        for c in comments
    ]

    tag_counts = Counter(tag for e in enriched for tag in e["tags"])
    emotion_counts = Counter([e["emotion"] for e in enriched if e["emotion"]])
    tone_counts = Counter([e["tone"] for e in enriched if e["tone"]])

    return {
        "total_comments": len(comments),
        "top_tags": tag_counts.most_common(10),
        "top_emotions": emotion_counts.most_common(5),
        "top_tones": tone_counts.most_common(5)
    }



@router.get("/story/{user_id}")
def get_story(user_id: int):
    session = SessionLocal()
    comments = session.query(Comment).filter(Comment.user_id == user_id).all()
    session.close()

    if not comments:
        return {"message": f"No comments found for user {user_id}"}

    # Collect tags and idioms from user comments
    tags = [c.tags for c in comments if c.tags]
    idioms = [c.idioms for c in comments if c.idioms]

    # Build metadata enriched with cultural helpers
    themes = detect_themes(tags)
    metadata = {
        "tone": comments[0].tone or "reflective",
        "emotion": comments[0].emotion or "neutral",
        "tags": tags,
        "themes": themes,
        "idioms": idioms,
        "proverbs": pick_proverbs(themes),
        "events": get_cultural_events(datetime.utcnow().month)
    }

    # Generate fluent bilingual paragraphs
    metadata["paragraphs"] = generate_fluent_paragraph(metadata, count=3)

    return {"user_id": user_id, "story": metadata}


# --- Story Summary Helpers ---
def generate_story_summary(comments, enriched):
    tag_counts = Counter(tag for e in enriched for tag in e["tags"])
    emotion_counts = Counter([e["emotion"] for e in enriched])
    tone_counts = Counter([e["tone"] for e in enriched])
    all_tags = set(tag for e in enriched for tag in e["tags"])
    all_idioms = set(idiom for e in enriched for idiom in e["idioms"])

    theme_map = {
        "community": {"jamii", "harambee", "mtaa", "voice"},
        "innovation": {"jua kali", "matatu", "maendeleo"},
        "leadership": {"uhuru", "umoja", "shujaa"}
    }
    themes = {theme for theme, keywords in theme_map.items() if keywords & all_tags}

    metadata = {
        "tone": tone_counts.most_common(1)[0][0] if enriched else "reflective",
        "emotion": emotion_counts.most_common(1)[0][0] if enriched else "neutral",
        "tags": list(all_tags),
        "themes": list(themes),
        "idioms": list(all_idioms),
        "events": get_cultural_events(datetime.utcnow().month)  # <-- seasonal enrichment
    }
    metadata["paragraphs"] = generate_fluent_paragraph(metadata, count=3)

    return {
        "title": "Echoed Voices",
        "summary": f"Generated from {len(comments)} comments",
        "emotion": metadata["emotion"],
        "tone": metadata["tone"],
        "themes": metadata["themes"],
        "tags": metadata["tags"],
        "idioms": metadata["idioms"],
        "events": metadata["events"],  # <-- include in response
        "tag_cloud": [{"tag": tag, "count": count} for tag, count in tag_counts.items()],
        "paragraphs": metadata["paragraphs"]
    }


    return {
        "title": "Echoed Voices",
        "summary": f"Generated from {len(comments)} comments",
        "emotion": metadata["emotion"],
        "tone": metadata["tone"],
        "themes": metadata["themes"],
        "tags": metadata["tags"],
        "idioms": metadata["idioms"],
        "tag_cloud": [{"tag": tag, "count": count} for tag, count in tag_counts.items()],
        "paragraphs": metadata["paragraphs"]
    }

def analyze_comment(comment_text: str):
    blob = TextBlob(comment_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        emotion = "joy"
    elif polarity > 0.2:
        emotion = "hope"
    elif polarity < -0.2:
        emotion = "grief"
    else:
        emotion = "resilience"

    tone_map = {
        "hopeful": ["hope", "change", "future"],
        "urgent": ["crisis", "must", "now"],
        "celebratory": ["success", "achievement", "shujaa", "harambee"],
        "reflective": ["community", "voice", "impact", "jamii"]
    }
    tone = next((t for t, kws in tone_map.items() if any(kw in comment_text.lower() for kw in kws)), "reflective")

    global_tags = ["hope", "change", "community", "voice", "impact"]
    local_tags = ["uhuru", "umoja", "maendeleo", "shujaa", "jamii", "mtaa", "harambee", "matatu", "jua kali"]
    words = comment_text.lower().split()
    tags = [word for word in words if word in global_tags + local_tags]

    idioms = []
    idiom_list = [
        "harambee spirit", "jua kali hustle", "pole pole ndio mwendo",
        "unity in diversity", "mtaa wa maendeleo", "mama mboga resilience",
        "ugatuzi empowerment", "boda boda hustle"
    ]
    for idiom in idiom_list:
        if idiom in comment_text.lower():
            idioms.append(idiom)

    return {"emotion": emotion, "tone": tone, "tags": tags, "idioms": idioms}

# --- Root ---
@router.get("/")
def root():
    return {"message": "EchoPulse1314 backend is running"}

@router.get("/tag-cloud")
def show_tag_cloud():
    session = SessionLocal()
    comments = session.query(Comment).all()
    enriched = [{"tags": c.tags.split(",") if c.tags else []} for c in comments]
    tag_counts = Counter(tag for e in enriched for tag in e["tags"])
    tag_cloud = [{"tag": tag, "count": count} for tag, count in tag_counts.items()]
    session.close()

    render_tag_cloud(tag_cloud)
    return {"message": "Tag cloud rendered"}

# --- Visualization ---
def render_tag_cloud(tag_cloud):
    freq = {item["tag"]: item["count"] for item in tag_cloud}
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()
