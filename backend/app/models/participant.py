"""Participant model for CHOSEN.

This module contains the Participant model representing a person
involved in a conversation.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import ParticipantRole


class Participant(BaseModel):
    """A participant in a conversation.

    This is an immutable value object representing a participant's identity.
    Once created, it cannot be modified - use a new instance for updates.

    Attributes:
        name: Full name of the participant.
        role: The participant's role in the conversation.
        email: Email address (optional).
        company: Company or organization (optional).
    """

    model_config = ConfigDict(use_enum_values=True, frozen=True)

    name: str
    role: ParticipantRole
    email: Optional[EmailStr] = None
    company: Optional[str] = None
