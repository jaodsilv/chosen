"""Response metrics model for CHOSEN.

This module contains the ResponseMetrics model for tracking
response time and message count metrics.
"""

from typing import Optional

from pydantic import BaseModel, Field


class ResponseMetrics(BaseModel):
    """Metrics tracking response patterns in a conversation.

    Attributes:
        recruiter_avg_hours: Average hours for recruiter to respond
            (must be >= 0).
        candidate_avg_hours: Average hours for candidate to respond
            (must be >= 0).
        recruiter_message_count: Total messages sent by recruiter
            (must be >= 0).
        candidate_message_count: Total messages sent by candidate
            (must be >= 0).
    """

    recruiter_avg_hours: Optional[float] = Field(default=None, ge=0)
    candidate_avg_hours: Optional[float] = Field(default=None, ge=0)
    recruiter_message_count: int = Field(default=0, ge=0)
    candidate_message_count: int = Field(default=0, ge=0)
