"""Enum definitions for the AI Message Writer Assistant.

This module contains all enumeration types used across the application:
    - Platform: Communication platforms (linkedin, email, phone, in_person)
    - ProcessStatus: Job application stages (14 statuses)
    - ParticipantRole: Conversation participant types
"""

from enum import Enum


class Platform(str, Enum):
    """Communication platforms for recruiter conversations.

    Attributes:
        LINKEDIN: LinkedIn direct messages.
        EMAIL: Email communication.
        PHONE: Phone calls or voicemails.
        IN_PERSON: In-person meetings or conversations.
    """

    LINKEDIN = "linkedin"
    EMAIL = "email"
    PHONE = "phone"
    IN_PERSON = "in_person"


class ProcessStatus(str, Enum):
    """Job application process stages.

    Tracks the progression of a job opportunity from initial contact
    through final resolution.

    Attributes:
        NEW: Initial contact, not yet reviewed.
        REVIEWING: Currently reviewing the opportunity.
        INTERESTED: Expressed interest in the position.
        NOT_INTERESTED: Declined to pursue the opportunity.
        APPLIED: Submitted formal application.
        AWAITING_RESPONSE: Waiting for recruiter/company response.
        INTERVIEWING: In active interview process.
        OFFER: Received job offer.
        NEGOTIATING: Negotiating offer terms.
        ACCEPTED: Accepted the offer.
        DECLINED: Declined the offer.
        REJECTED: Rejected by the company.
        WITHDRAWN: Withdrew from consideration.
        GHOSTED: No response after reasonable time.
    """

    NEW = "new"
    REVIEWING = "reviewing"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    APPLIED = "applied"
    AWAITING_RESPONSE = "awaiting_response"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    NEGOTIATING = "negotiating"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    GHOSTED = "ghosted"


class ParticipantRole(str, Enum):
    """Roles of participants in a conversation.

    Attributes:
        RECRUITER: The recruiting person or agency representative.
        CANDIDATE: The job seeker (typically the user).
        HIRING_MANAGER: The company's hiring manager.
    """

    RECRUITER = "recruiter"
    CANDIDATE = "candidate"
    HIRING_MANAGER = "hiring_manager"
