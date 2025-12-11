"""Message model for the AI Message Writer Assistant.

This module contains the Message model representing individual messages
in a conversation thread.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in a conversation thread.

    Attributes:
        timestamp: When the message was sent.
        from_name: Name of the message sender.
        to_name: Name of the recipient (optional).
        subject: Message subject line (optional, mainly for emails).
        body: The message content.
        attachments: List of attachment file paths.
    """

    timestamp: datetime
    from_name: str
    to_name: Optional[str] = None
    subject: Optional[str] = None
    body: str
    attachments: List[str] = Field(default_factory=list)
