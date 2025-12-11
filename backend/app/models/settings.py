"""User settings model for the AI Message Writer Assistant.

This module contains the UserSettings model for storing user
preferences and configuration.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class UserSettings(BaseModel):
    """User settings and preferences.

    Attributes:
        user_name: The user's display name.
        user_email: The user's email address.
        default_model: Default Claude model to use (sonnet/haiku/opus).
        resume_path: Path to the user's resume file.
        preferences: Additional user preferences as key-value pairs.
    """

    user_name: str
    user_email: str
    default_model: str
    resume_path: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
