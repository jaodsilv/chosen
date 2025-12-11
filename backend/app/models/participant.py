"""Participant model for the AI Message Writer Assistant.

This module contains the Participant model representing a person
involved in a conversation.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import ParticipantRole


class Participant(BaseModel):
    """A participant in a conversation.

    Attributes:
        name: Full name of the participant.
        role: The participant's role in the conversation.
        email: Email address (optional).
        company: Company or organization (optional).
    """

    model_config = ConfigDict(use_enum_values=True)

    name: str
    role: ParticipantRole
    email: Optional[str] = None
    company: Optional[str] = None
