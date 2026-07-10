"""
Targeted check for the direction-reversal fix in the Critic's prompt.

Unlike test_clean_approved_draft.py, this DOES call the real LLM (the thing
being tested is prompt behavior, not pure code logic), so it costs an API
call and isn't fully deterministic - but it isolates the exact scenario
that slipped through before, rather than hoping a live full-pipeline run
happens to reproduce it.
"""

import os
from dotenv import load_dotenv
from agents.critic import critique
from schemas.research_schema import ResearchOutput, Finding, Source

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

research = ResearchOutput(
    findings=[
        Finding(
            id="f1",
            claim="RAG reduces the need for frequent model retraining",
            evidence="By retrieving current information at query time, RAG reduces how often "
                      "the underlying model itself needs to be retrained on new data.",
            source_id="s1",
            confidence=0.9,
            limitations="",
        )
    ],
    sources=[Source(id="s1", title="Test source", url="https://example.com")],
    open_questions=[],
    confidence=0.9,
)

draft_with_reversed_claim = (
    "RAG may require frequent model retraining, according to research on retrieval systems [f1]."
)

print("Testing draft with REVERSED polarity (should be flagged, not supported):")
print(f"  Draft: {draft_with_reversed_claim}\n")

raw = critique(draft_with_reversed_claim, research, api_key)

for v in raw.verdicts:
    print(f"  [{v.verdict.value} | {v.severity.value}] {v.claim}")
    print(f"      feedback: {v.feedback}")

flagged_correctly = any(
    v.verdict.value in ("contradicted", "unsupported", "partially_supported")
    for v in raw.verdicts
)
print(f"\nCorrectly flagged (not marked supported): {flagged_correctly}")