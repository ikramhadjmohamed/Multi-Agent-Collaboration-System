import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from agents.writer import write
from schemas.research_schema import ResearchOutput
from schemas.draft_schema import Draft
from utils.storage import load_json, save_json

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Pass a saved research JSON path as an argument, e.g.:
# python -m scripts.check_writer data/research_20260706_143434.json
research_path = sys.argv[1]
research = load_json(Path(research_path), ResearchOutput)

question = "What are the main benefits and risks of RAG (retrieval-augmented generation)?"
draft_text = write(question, research, api_key)

print("=== DRAFT ===")
print(draft_text)

draft = Draft(text=draft_text, revision=0)
saved_path = save_json(draft, "draft")
print(f"\nSaved to: {saved_path}")