# story_generator.py

# Optional: future imports if needed
# import datetime

# 🔹 Tag → Theme mapping
tag_theme_map = {
    "harambee": "unity and collective effort",
    "jua kali": "resilience and hustle",
    "matatu": "movement and chaos"
}

# 🔹 Story generation logic
def generate_story(tag):
    theme = tag_theme_map.get(tag, "local life")
    
    if tag == "harambee":
        return "In the spirit of harambee, watu walikusanyika — pulling together, lifting each other, no one left behind."
    elif tag == "jua kali":
        return "Under the blazing sun, vijana wa jua kali walichora njia yao — crafting dreams from scrap, fueled by grit."
    elif tag == "matatu":
        return "Matatu zikipiga honi, maisha yanacheza — chaos, rhythm, and the pulse of Nairobi in motion."
    else:
        return f"{tag} echoes through the streets — a whisper of local life, a beat of the everyday."

# 🔹 Example usage
if __name__ == "__main__":
    for tag in ["harambee", "jua kali", "matatu"]:
        print(generate_story(tag))
