"""
The approval rule, in code — deliberately NOT delegated to the LLM.

Rule (as you defined it):
- Any MAJOR claim that is unsupported, contradicted, or only partially
  supported -> reject (a central claim being overstated still needs revision).
- MINOR issues (unsupported/contradicted only) are tolerated individually,
  but too many -> reject too. Minor partially_supported is left alone.
"""

from schemas.critic_schema import RawCriticOutput, CriticDecision, VerdictLabel, Severity

# A "bad" verdict is one that means the claim isn't cleanly backed by evidence.
BAD_VERDICTS = {VerdictLabel.UNSUPPORTED, VerdictLabel.CONTRADICTED}

# For MAJOR claims specifically, "partially_supported" is ALSO treated as
# blocking. Reasoning: a central claim that overstates or generalizes its
# evidence is exactly the kind of thing a fact-checker should push back on.
# Minor partially_supported claims are left alone - a side detail being
# slightly overstated isn't worth another revision round.
MAJOR_BAD_VERDICTS = BAD_VERDICTS | {VerdictLabel.PARTIALLY_SUPPORTED}

# Tune this: how many minor issues are tolerable before the draft still
# gets sent back. Start conservative; loosen it if your revision loop
# keeps rejecting drafts that were actually fine.
MINOR_ISSUE_THRESHOLD = 2


def decide(raw: RawCriticOutput) -> CriticDecision:
    major_issues = sum(
        1 for v in raw.verdicts
        if v.severity == Severity.MAJOR and v.verdict in MAJOR_BAD_VERDICTS
    )
    minor_issues = sum(
        1 for v in raw.verdicts
        if v.severity == Severity.MINOR and v.verdict in BAD_VERDICTS
    )

    approved = major_issues == 0 and minor_issues <= MINOR_ISSUE_THRESHOLD

    return CriticDecision(
        raw=raw,
        approved=approved,
        major_issues=major_issues,
        minor_issues=minor_issues,
    )