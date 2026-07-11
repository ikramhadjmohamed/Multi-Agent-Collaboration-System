"""
Schema for the Researcher agent's output.

Why Pydantic: it validates the LLM's JSON response against this structure.
If a field is missing or the wrong type, .model_validate_json() raises a
ValidationError immediately — that's our signal to retry the researcher
call with a correction prompt, instead of passing broken data to the Writer.
"""

from pydantic import BaseModel, Field


class Finding(BaseModel):
    """One atomic fact the researcher extracted from a source.

    Each finding is deliberately small (one claim, one piece of evidence)
    rather than a whole paragraph. Why? Because the Critic later needs to
    check claims one at a time. If a "finding" bundled 3 facts together,
    the critic couldn't cleanly mark one as unsupported without affecting
    the other two.
    """

    id: str = Field(..., description="Unique id, e.g. 'f1', 'f2' — lets Writer/Critic reference this exact finding")
    claim: str = Field(..., description="The factual statement itself")
    evidence: str = Field(..., description="The supporting text/quote/explanation from the source")
    source_id: str = Field(..., description="References an id in the sources list below")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Researcher's own confidence in this claim, 0-1")
    limitations: str = Field(
        default="", description="Why this SPECIFIC claim needs caution even though evidence exists "
                                 "(e.g. outdated source, vendor bias, small sample, contested finding). "
                                 "Different from open_questions: this claim IS supported, but imperfectly."
    )


class Source(BaseModel):
    """A source the researcher pulled findings from."""

    id: str = Field(..., description="Unique id, e.g. 's1' — Finding.source_id points here")
    title: str
    url: str


class ResearchOutput(BaseModel):
    """Full output of the Researcher agent for one user question."""

    findings: list[Finding]
    sources: list[Source]
    open_questions: list[str] = Field(
        default_factory=list,
        description="Things the researcher could NOT confirm — the Writer should avoid claiming these as fact"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence in the research as a whole")