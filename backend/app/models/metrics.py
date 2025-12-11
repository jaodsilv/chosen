"""Response metrics model for the AI Message Writer Assistant.

This module contains the ResponseMetrics model for tracking
response time and message count metrics.
"""

from typing import Optional

from pydantic import BaseModel


class ResponseMetrics(BaseModel):
    """Metrics tracking response patterns in a conversation.

    Attributes:
        recruiter_avg_hours: Average hours for recruiter to respond.
        candidate_avg_hours: Average hours for candidate to respond.
        recruiter_message_count: Total messages sent by recruiter.
        candidate_message_count: Total messages sent by candidate.
    """

    recruiter_avg_hours: Optional[float] = None
    candidate_avg_hours: Optional[float] = None
    recruiter_message_count: int = 0
    candidate_message_count: int = 0
