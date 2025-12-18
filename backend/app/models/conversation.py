"""Conversation model for CHOSEN.

This module contains the Conversation model representing a full
conversation thread with a recruiter.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.analysis import ContextAnalysis, JobFitScore
from app.models.enums import Platform, ProcessStatus
from app.models.message import Message
from app.models.metrics import ResponseMetrics
from app.models.validators import validate_path_in_data_dir


class Conversation(BaseModel):
    """A complete conversation thread with a recruiter.

    Attributes:
        id: Unique identifier (auto-generated UUID).
        created_at: When the conversation was created.
        updated_at: When the conversation was last updated.
        platform: The communication platform.
        company: Target company name.
        recruiting_company: Recruiting firm name (if different from company).
        recruiter_name: Name of the recruiter.
        process_status: Current status in the application process.
        context: User notes about the conversation.
        messages: List of messages in the conversation.
        context_analysis: AI-generated context analysis.
        fit_score: AI-generated job fit score.
        response_metrics: Response time and count metrics.
        job_description: Job description text.
        job_description_filepath: Path to job description file.
        resume_filepath: Path to resume used for this application.
        archived: Whether the conversation is archived.
        archived_at: When the conversation was archived (auto-populated when archived=True).
        archive_reason: Reason for archiving.
        related_conversation_ids: IDs of related conversations.

    Archive Behavior:
        When archived=True: archived_at is auto-populated with current UTC timestamp
            if not explicitly provided.
        When archived=False: archived_at and archive_reason are automatically cleared
            to maintain data consistency.
    """

    model_config = ConfigDict(use_enum_values=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    platform: Platform
    company: Optional[str] = None
    recruiting_company: Optional[str] = None
    recruiter_name: str
    process_status: ProcessStatus = ProcessStatus.NEW
    context: List[str] = Field(default_factory=list)
    messages: List[Message] = Field(default_factory=list)
    context_analysis: Optional[ContextAnalysis] = None
    fit_score: Optional[JobFitScore] = None
    response_metrics: Optional[ResponseMetrics] = None
    job_description: Optional[str] = None
    job_description_filepath: Optional[str] = None
    resume_filepath: Optional[str] = None
    archived: bool = False
    archived_at: Optional[datetime] = None
    archive_reason: Optional[str] = None
    related_conversation_ids: List[str] = Field(default_factory=list)

    @field_validator("job_description_filepath", "resume_filepath")
    @classmethod
    def validate_filepath(cls, v: Optional[str]) -> Optional[str]:
        """Validate that filepaths are within the data directory."""
        return validate_path_in_data_dir(v)

    @model_validator(mode="after")
    def validate_archive_consistency(self) -> "Conversation":
        """Ensure archive fields are consistent.

        When archived=True: archived_at is auto-populated with current UTC
            timestamp if not explicitly provided.
        When archived=False: archived_at and archive_reason are cleared to
            maintain data consistency.

        Returns:
            The validated Conversation instance.
        """
        if self.archived:
            if self.archived_at is None:
                object.__setattr__(self, "archived_at", datetime.now(timezone.utc))
        else:
            if self.archived_at is not None:
                object.__setattr__(self, "archived_at", None)
            if self.archive_reason is not None:
                object.__setattr__(self, "archive_reason", None)
        return self
