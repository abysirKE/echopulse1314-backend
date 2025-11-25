EchoPulse Backend
Culturally intelligent storytelling engine powered by FastAPI. Transforms user comments into bilingual Swahili-English narratives enriched with emotion, seasonal events, idioms, and regional flavor.

Features
Comment-to-Story Conversion: Translates raw user input into structured, resonant story summaries.

Bilingual Output: Generates Swahili-English paragraphs with cultural nuance.

Seasonal Enrichment: Adds context-aware events like harvests, holidays, or local festivals.

Regional Flavor Detection: Maps tags to Kenyan regions (e.g. Nairobi, Kisumu, Mombasa).

Tag Cloud Visualization: Highlights dominant themes and keywords.

SQLite Integration: Stores comments and generated stories for reuse and analysis.

Tech Stack
FastAPI for backend routing and API endpoints

SQLite for lightweight data persistence

Python for story logic and enrichment

Git for version control

Optional Frontend: React or HTML/CSS dashboard (coming soon)

Installation
git clone https://github.com/abysirKE/echopulse1314-backend.git
cd echopulse1314-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

API Endpoint
POST /comment
{
  "user_id": 1,
  "text": "Harambee spirit and jua kali hustle"
}

Response:
{
  "message": "Comment added",
  "id": 1
}

Sample Output
"In the heart of Nairobi, the jua kali spirit thrives. From metalwork to mobile repairs, the hustle echoes resilience..."

Regional Tags
Region	Sample Tags
Nairobi	hustle, innovation, urban
Kisumu	lake, community, resilience
Mombasa	coast, trade, heritage

Contributing
Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to modify.

License
MIT License

---

Let me know when you’ve added it — I can help you write a `CONTRIBUTING.md`, set up GitHub Pages, or start the frontend layout. Want to sketch the dashboard next?
