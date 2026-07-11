"""
Wraps a Writer draft with metadata, so it can be saved/loaded like the
Researcher's output. The draft text itself is free-form (not structured
JSON from the LLM), but WE still want structure around it for storage:
which revision number is this, what question/research does it belong to.
"""

from pydantic import BaseModel, Field


class Draft(BaseModel):
    text: str = Field(..., description="The Writer's summary, with [f_id] citations inline")
    revision: int = Field(default=0, description="0 = first draft, 1 = after first revision, etc.")