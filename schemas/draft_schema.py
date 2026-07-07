from pydantic import BaseModel, Field


class Draft(BaseModel):
    text: str = Field(..., description="The Writer's summary, with [f_id] citations inline")
    revision: int = Field(default=0, description="0 = first draft, 1 = after first revision, etc.")