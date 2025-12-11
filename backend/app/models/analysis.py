"""Analysis models for the AI Message Writer Assistant.

This module contains models for conversation analysis:
    - SentimentTrend: Tracks sentiment changes over conversation
    - ConversationStage: Current stage and progression quality
    - ActionItems: Pending actions for candidate and recruiter
    - ContextAnalysis: Complete analysis of conversation context
    - JobFitScore: Scoring of job fit with breakdowns
"""

from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator


class SentimentTrend(BaseModel):
    """Tracks sentiment changes throughout a conversation.

    Attributes:
        initial: The sentiment at the start of the conversation.
        current: The current sentiment state.
        direction: Whether sentiment is improving, stable, or declining.
        indicators: List of specific indicators that inform the analysis.
    """

    initial: str
    current: str
    direction: str
    indicators: List[str]


class ConversationStage(BaseModel):
    """Tracks the current stage of a conversation.

    Attributes:
        current: The current conversation stage (e.g., initial_outreach).
        progression_quality: Assessment of how well the conversation is progressing.
    """

    current: str
    progression_quality: str


class ActionItems(BaseModel):
    """Pending action items for participants.

    Attributes:
        candidate_pending: Actions the candidate needs to take.
        recruiter_pending: Actions the recruiter needs to take.
    """

    candidate_pending: List[str] = Field(default_factory=list)
    recruiter_pending: List[str] = Field(default_factory=list)


class ContextAnalysis(BaseModel):
    """Complete analysis of a conversation's context.

    Attributes:
        summary: Brief summary of the conversation.
        sentiment_trend: Sentiment analysis over time.
        conversation_stage: Current stage and progression.
        action_items: Pending actions for participants.
        patterns_detected: Communication patterns identified.
        recommendations: Suggested next steps.
        last_analyzed: When this analysis was performed.
    """

    summary: str
    sentiment_trend: SentimentTrend
    conversation_stage: ConversationStage
    action_items: ActionItems
    patterns_detected: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    last_analyzed: datetime


class JobFitScore(BaseModel):
    """Assessment of job fit with detailed scoring.

    All score fields must be in the range 0-100.

    Attributes:
        overall_score: Overall job fit score (0-100).
        required_skills_score: Match on required skills (0-100).
        preferred_skills_score: Match on preferred skills (0-100).
        experience_match: Experience level match (0-100).
        strengths: List of identified strengths.
        gaps: List of identified gaps with skill, severity, and mitigation.
        breakdown: Detailed score breakdown by category.
    """

    overall_score: float
    required_skills_score: float
    preferred_skills_score: float
    experience_match: float
    strengths: List[str] = Field(default_factory=list)
    gaps: List[Dict[str, Any]] = Field(default_factory=list)
    breakdown: Dict[str, float] = Field(default_factory=dict)

    @field_validator(
        "overall_score",
        "required_skills_score",
        "preferred_skills_score",
        "experience_match",
    )
    @classmethod
    def validate_score_range(cls, v: float) -> float:
        """Validate that score is within 0-100 range."""
        if not 0 <= v <= 100:
            raise ValueError("Score must be between 0 and 100")
        return float(v)
