# app/story_logic.py
import random
from datetime import datetime

# --- Swahili-English story templates ---
story_templates = [
    "Katika moyo wa {region}, voices rise with {tone} energy and {emotion} resolve.",
    "Kutoka kwa sauti za {tags}, hadithi ya {themes} inaibuka — a story of resilience from {region}.",
    "Guided by the spirit of {idioms}, safari hii inaonyesha mwendo wa jamii yetu ya {region}.",
    "Jamii ya {region} inaonyesha {emotion} na {tone}, tukielekea kwenye maendeleo ya kweli.",
    "From the rhythm of {tags}, tunasikia nguvu ya {themes} ikichanua katika {region}."
]


def generate_fluent_paragraph(metadata, count=2):
    paragraphs = []

    tags_str = ", ".join(metadata.get("tags", [])) or "jamii"
    themes_str = ", ".join(metadata.get("themes", [])) or "community"
    idioms_str = ", ".join(metadata.get("idioms", [])) or "harambee spirit"
    region_str = metadata.get("region", "Kenya")

    for _ in range(count):
        template = random.choice(story_templates)
        paragraph = template.format(
            tone=metadata.get("tone", "reflective"),
            emotion=metadata.get("emotion", "neutral"),
            tags=tags_str,
            themes=themes_str,
            idioms=idioms_str,
            region=region_str
        )
        if metadata.get("proverbs"):
            paragraph += f" {random.choice(metadata['proverbs'])}."
        if metadata.get("events"):
            paragraph += f" As {metadata['events'][0]} approaches, our unity shines."
        paragraphs.append(paragraph)

    return paragraphs



# --- Cultural Intelligence Helpers ---
def detect_themes(tags):
    theme_map = {
        "community": {"jamii", "harambee", "mtaa", "voice", "umoja"},
        "innovation": {"jua kali", "matatu", "fintech", "maendeleo"},
        "leadership": {"uhuru", "shujaa", "vijana", "wazee"},
        "resilience": {"hustle", "pole pole", "drought", "survival"}
    }
    themes = {theme for theme, keywords in theme_map.items() if keywords & set(tags)}
    return list(themes) if themes else ["community"]

def pick_proverbs(themes):
    proverbs_map = {
        "resilience": [
            "Pole pole ndio mwendo",
            "Maji ukiyavulia nguo huna budi kuyaoga"
        ],
        "community": [
            "Kidole kimoja hakivunji chawa",
            "Harambee spirit"
        ],
        "leadership": [
            "Kiongozi bora ni mtumishi",
            "Ngamia wa mbele huongoza msafara"
        ],
        "innovation": [
            "Ubunifu ni nguzo ya maendeleo",
            "Jua kali hustle builds dreams"
        ]
    }
    selected = []
    for theme in themes:
        if theme in proverbs_map:
            selected.extend(proverbs_map[theme])
    return selected

def detect_region(tags):
    region_map = {
        "Nairobi": {"matatu", "jua kali", "mtaa", "maendeleo"},
        "Kisumu": {"boda boda", "mama mboga", "ugatuzi", "fishing"},
        "Mombasa": {"swahili coast", "mtaa wa maendeleo", "ushirikiano", "pwani"}
    }
    for region, keywords in region_map.items():
        if keywords & set(tags):
            return region
    return "Kenya"

def get_cultural_events(month):
    cultural_events = {
        11: ["Constitution Day", "Post-harvest reflections"],
        12: ["Jamhuri Day", "Christmas celebrations"],
        4: ["Easter traditions", "Ramadhan reflections"],
        8: ["Mashujaa remembrance", "Harvest season"]
    }
    return cultural_events.get(month, [])

