import os
from dotenv import load_dotenv
from agents.researcher import research

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

result = research("What are the main benefits and risks of RAG (retrieval-augmented generation)?", api_key)

print("=== FINDINGS ===")
for f in result.findings:
    print(f"[{f.id}] ({f.confidence}) {f.claim}")
    print(f"    evidence: {f.evidence}")
    print(f"    source: {f.source_id}")

print("\n=== SOURCES ===")
for s in result.sources:
    print(f"[{s.id}] {s.title} — {s.url}")

print("\n=== OPEN QUESTIONS ===")
for q in result.open_questions:
    print(f"- {q}")

print(f"\nOverall confidence: {result.confidence}")