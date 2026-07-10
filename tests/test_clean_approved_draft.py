"""
Deterministic test for clean_approved_draft - doesn't depend on live LLM
output or search results, so it reliably exercises the exact scenario
(a tolerated-minor unsupported claim with trailing citation tags) instead
of hoping a live run happens to reproduce it.
"""

from agents.revision import clean_approved_draft
from schemas.critic_schema import RawCriticOutput, CriticDecision, Verdict, VerdictLabel, Severity
from schemas.decision_rules import decide


def test_clean_approved_draft_removes_claim_and_citation_tags():
    draft_text = (
        "RAG improves accuracy [f1]. "
        "A caution is noted that some findings are opinion-based [f1][f2][f3]. "
        "RAG also reduces hallucinations [f2]."
    )

    raw = RawCriticOutput(
        verdicts=[
            Verdict(claim="RAG improves accuracy", verdict=VerdictLabel.SUPPORTED,
                    severity=Severity.MAJOR, finding_ids=["f1"], feedback="fine as-is"),
            Verdict(claim="A caution is noted that some findings are opinion-based",
                    verdict=VerdictLabel.UNSUPPORTED, severity=Severity.MINOR,
                    finding_ids=["f1", "f2", "f3"], feedback="remove, not backed by any finding"),
            Verdict(claim="RAG also reduces hallucinations", verdict=VerdictLabel.SUPPORTED,
                    severity=Severity.MAJOR, finding_ids=["f2"], feedback="fine as-is"),
        ],
        summary_feedback="One unsupported claim should be removed.",
    )

    decision = decide(raw)
    assert decision.approved  # only a MINOR unsupported claim -> tolerated, not blocking

    cleaned, removed = clean_approved_draft(draft_text, decision)

    assert len(removed) == 1
    assert "opinion-based" in removed[0]

    # The actual bug we're testing for: no orphaned citation brackets left behind
    assert "[f1][f2][f3]" not in cleaned
    assert "[f1]" in cleaned  # from the first sentence, should still be there
    assert "[f2]" in cleaned  # from the third sentence, should still be there

    # No leftover double periods, double spaces, or stray punctuation
    assert ".." not in cleaned
    assert "  " not in cleaned

    print("Cleaned text:", cleaned)
    print("Removed:", removed)


if __name__ == "__main__":
    test_clean_approved_draft_removes_claim_and_citation_tags()
    print("PASSED")