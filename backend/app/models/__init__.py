"""Models - Pydantic data models for domain objects.

This package exports all domain models used in the AI Message Writer Assistant.
"""

from app.models.analysis import (
    ActionItems,
    ContextAnalysis,
    ConversationStage,
    JobFitScore,
    SentimentTrend,
)
from app.models.conversation import Conversation
from app.models.enums import ParticipantRole, Platform, ProcessStatus
from app.models.message import Message
from app.models.metrics import ResponseMetrics
from app.models.participant import Participant
from app.models.settings import UserSettings

__all__ = [
    # Enums
    "Platform",
    "ProcessStatus",
    "ParticipantRole",
    # Message models
    "Message",
    "Participant",
    # Analysis models
    "SentimentTrend",
    "ConversationStage",
    "ActionItems",
    "ContextAnalysis",
    "JobFitScore",
    # Metrics
    "ResponseMetrics",
    # Main models
    "Conversation",
    "UserSettings",
]
