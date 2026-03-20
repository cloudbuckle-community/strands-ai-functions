from pydantic import BaseModel


class FileChange(BaseModel):
    file_path: str
    change_type: str  # added, modified, deleted, renamed
    summary: str


class PRSummary(BaseModel):
    title: str
    what_changed: list[FileChange]
    why_it_matters: str
    risk_level: str  # low, medium, high
    risk_reasoning: str
    testing_suggestions: list[str]
    suggested_reviewers: list[str]
