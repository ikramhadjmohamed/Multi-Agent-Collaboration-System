"""
Directly tests what happens when the Researcher's own findings genuinely
CONFLICT with each other - not just "one-sided evidence" (which is what
the live DuckDuckGo test on the AI-existential-risk question actually
showed), but two findings that directly contradict one another.

This is deterministic (hand-built ResearchOutput) rather than hoping live
search happens to surface two opposing sources for the same query.
"""

import os
from dotenv import load_dotenv
from agents.writer import write
from agents.critic import critique
from schemas.research_schema import ResearchOutput, Finding, Source

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

question = "Does AI pose an existential risk to humanity?"

research = ResearchOutput(
    findings=[
        Finding(
            id="f1",
            claim="AI poses a severe, near-term existential risk to humanity",
            evidence="Leading AI safety researchers estimate a significant probability "
                      "of catastrophic outcomes from advanced AI within the coming decades.",
            source_id="s1",
            confidence=0.85,
            limitations="",
        ),
        Finding(
            id="f2",
            claim="AI does not pose a meaningful existential risk; such concerns are overstated",
            evidence="Several AI researchers argue that existential risk claims are speculative "
                      "and distract from AI's real, immediate harms like bias and job displacement.",
            source_id="s2",
            confidence=0.85,
            limitations="",
        ),
    ],
    sources=[
        Source(id="s1", title="AI Safety Researcher Perspective", url="https://example.com/s1"),
        Source(id="s2", title="AI Skeptic Perspective", url="https://example.com/s2"),
    ],
    open_questions=[],
    confidence=0.8,
)

print("=== Writer's draft from genuinely conflicting findings ===")
draft = write(question, research, api_key)
print(draft)

print("\n=== Critic reviewing ===")
raw = critique(draft, research, api_key)
for v in raw.verdicts:
    print(f"  [{v.verdict.value} | {v.severity.value}] {v.claim}")
    print(f"      finding_ids: {v.finding_ids} | feedback: {v.feedback}")
print(f"\nSummary feedback: {raw.summary_feedback}")