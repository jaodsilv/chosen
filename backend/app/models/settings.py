"""User settings model for CHOSEN.

This module contains the UserSettings model for storing user
preferences and configuration.
"""

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.validators import validate_path_in_data_dir


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
    user_email: EmailStr
    default_model: Literal["sonnet", "haiku", "opus"]
    resume_path: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("resume_path")
    @classmethod
    def validate_resume_path(cls, v: Optional[str]) -> Optional[str]:
        """Validate that resume_path is within the data directory."""
        return validate_path_in_data_dir(v)
