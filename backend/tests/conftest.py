"""Pytest configuration and fixtures."""

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app.main import app


# ============================================
# API CLIENT FIXTURES
# ============================================


@pytest.fixture
def client() -> TestClient:
    """Create a synchronous test client."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an asynchronous test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_settings() -> Dict[str, Any]:
    """Provide test settings override."""
    return {
        "env": "test",
    }


# ============================================
# TIMESTAMP FIXTURES
# ============================================


@pytest.fixture
def fixed_datetime() -> datetime:
    """Provide a fixed datetime for deterministic testing.

    Returns:
        A timezone-aware datetime set to 2025-12-09T10:00:00Z.
    """
    return datetime(2025, 12, 9, 10, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def fixed_datetime_updated() -> datetime:
    """Provide a second fixed datetime for update testing.

    Returns:
        A timezone-aware datetime set to 2025-12-09T15:30:00Z.
    """
    return datetime(2025, 12, 9, 15, 30, 0, tzinfo=timezone.utc)


# ============================================
# UUID FIXTURES
# ============================================


@pytest.fixture
def fixed_uuid() -> UUID:
    """Provide a fixed UUID for deterministic testing.

    Returns:
        A fixed UUID value.
    """
    return UUID("550e8400-e29b-41d4-a716-446655440000")


@pytest.fixture
def fixed_uuid_str() -> str:
    """Provide a fixed UUID string for deterministic testing.

    Returns:
        A fixed UUID string value.
    """
    return "550e8400-e29b-41d4-a716-446655440000"


# ============================================
# MESSAGE FIXTURES
# ============================================


@pytest.fixture
def sample_message_data(fixed_datetime: datetime) -> Dict[str, Any]:
    """Provide sample message data for testing.

    Args:
        fixed_datetime: The fixed datetime fixture.

    Returns:
        Dictionary containing valid message data.
    """
    return {
        "timestamp": fixed_datetime,
        "from_name": "John Recruiter",
        "to_name": "Candidate Name",
        "subject": "Senior Engineer Position at Company A",
        "body": "Hi! I came across your profile and think you'd be a great fit.",
        "attachments": ["job_description.pdf"],
    }


@pytest.fixture
def sample_message_minimal_data(fixed_datetime: datetime) -> Dict[str, Any]:
    """Provide minimal valid message data (required fields only).

    Args:
        fixed_datetime: The fixed datetime fixture.

    Returns:
        Dictionary containing minimal valid message data.
    """
    return {
        "timestamp": fixed_datetime,
        "from_name": "Recruiter",
        "body": "Message body content.",
    }


# ============================================
# PARTICIPANT FIXTURES
# ============================================


@pytest.fixture
def sample_participant_data() -> Dict[str, Any]:
    """Provide sample participant data for testing.

    Returns:
        Dictionary containing valid participant data.
    """
    return {
        "name": "John Recruiter",
        "role": "recruiter",
        "email": "john.recruiter@company.com",
        "company": "TechCorp Inc.",
    }


@pytest.fixture
def sample_participant_minimal_data() -> Dict[str, Any]:
    """Provide minimal valid participant data.

    Returns:
        Dictionary containing minimal valid participant data.
    """
    return {
        "name": "Jane Candidate",
        "role": "candidate",
    }


# ============================================
# ANALYSIS FIXTURES
# ============================================


@pytest.fixture
def sample_sentiment_trend_data() -> Dict[str, Any]:
    """Provide sample sentiment trend data.

    Returns:
        Dictionary containing valid sentiment trend data.
    """
    return {
        "initial": "positive",
        "current": "positive",
        "direction": "stable",
        "indicators": [
            "Enthusiastic initial message",
            "Personalized outreach",
        ],
    }


@pytest.fixture
def sample_conversation_stage_data() -> Dict[str, Any]:
    """Provide sample conversation stage data.

    Returns:
        Dictionary containing valid conversation stage data.
    """
    return {
        "current": "initial_outreach",
        "progression_quality": "smooth",
    }


@pytest.fixture
def sample_action_items_data() -> Dict[str, Any]:
    """Provide sample action items data.

    Returns:
        Dictionary containing valid action items data.
    """
    return {
        "candidate_pending": [
            "Wait for recruiter's response with more details",
        ],
        "recruiter_pending": [
            "Provide job description and compensation range",
        ],
    }


@pytest.fixture
def sample_context_analysis_data(
    fixed_datetime: datetime,
    sample_sentiment_trend_data: Dict[str, Any],
    sample_conversation_stage_data: Dict[str, Any],
    sample_action_items_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Provide sample context analysis data.

    Args:
        fixed_datetime: The fixed datetime fixture.
        sample_sentiment_trend_data: Sentiment trend data fixture.
        sample_conversation_stage_data: Conversation stage data fixture.
        sample_action_items_data: Action items data fixture.

    Returns:
        Dictionary containing valid context analysis data.
    """
    return {
        "summary": "Initial recruiter outreach for senior engineering role.",
        "sentiment_trend": sample_sentiment_trend_data,
        "conversation_stage": sample_conversation_stage_data,
        "action_items": sample_action_items_data,
        "patterns_detected": ["Recruiter mentioned specific skills from profile"],
        "recommendations": ["Ask about H1B sponsorship in next message"],
        "last_analyzed": fixed_datetime,
    }


# ============================================
# JOB FIT SCORE FIXTURES
# ============================================


@pytest.fixture
def sample_job_fit_score_data() -> Dict[str, Any]:
    """Provide sample job fit score data.

    Returns:
        Dictionary containing valid job fit score data.
    """
    return {
        "overall_score": 85.0,
        "required_skills_score": 90.0,
        "preferred_skills_score": 75.0,
        "experience_match": 85.0,
        "strengths": [
            "Strong match on Python and distributed systems",
            "Relevant leadership experience",
        ],
        "gaps": [
            {
                "skill": "Kubernetes",
                "severity": "medium",
                "mitigation": "Can learn quickly, have Docker experience",
            },
        ],
        "breakdown": {
            "technical_skills": 88.0,
            "experience_level": 92.0,
            "domain_knowledge": 75.0,
        },
    }


@pytest.fixture
def invalid_score_data() -> Dict[str, Any]:
    """Provide data with out-of-range score values.

    Returns:
        Dictionary containing invalid score data.
    """
    return {
        "overall_score": 150.0,  # Should be 0-100
        "required_skills_score": -10.0,  # Should be 0-100
        "preferred_skills_score": 75.0,
        "experience_match": 85.0,
        "strengths": [],
        "gaps": [],
        "breakdown": {},
    }


# ============================================
# RESPONSE METRICS FIXTURES
# ============================================


@pytest.fixture
def sample_response_metrics_data() -> Dict[str, Any]:
    """Provide sample response metrics data.

    Returns:
        Dictionary containing valid response metrics data.
    """
    return {
        "recruiter_avg_hours": 24.5,
        "candidate_avg_hours": 5.5,
        "recruiter_message_count": 3,
        "candidate_message_count": 2,
    }


@pytest.fixture
def sample_response_metrics_partial_data() -> Dict[str, Any]:
    """Provide sample response metrics data with None values.

    Returns:
        Dictionary containing response metrics data with some None values.
    """
    return {
        "recruiter_avg_hours": None,
        "candidate_avg_hours": 5.5,
        "recruiter_message_count": 1,
        "candidate_message_count": 1,
    }


# ============================================
# CONVERSATION FIXTURES
# ============================================


@pytest.fixture
def sample_conversation_data(
    fixed_uuid_str: str,
    fixed_datetime: datetime,
    sample_message_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Provide sample conversation data.

    Args:
        fixed_uuid_str: The fixed UUID string fixture.
        fixed_datetime: The fixed datetime fixture.
        sample_message_data: Sample message data fixture.

    Returns:
        Dictionary containing valid conversation data.
    """
    return {
        "id": fixed_uuid_str,
        "created_at": fixed_datetime,
        "updated_at": fixed_datetime,
        "platform": "linkedin",
        "company": "Company A",
        "recruiting_company": None,
        "recruiter_name": "John Recruiter",
        "process_status": "new",
        "context": ["$150,000 yearly is in the lower range"],
        "messages": [sample_message_data],
        "context_analysis": None,
        "fit_score": None,
        "response_metrics": None,
        "job_description": None,
        "job_description_filepath": None,
        "resume_filepath": None,
        "archived": False,
        "archived_at": None,
        "archive_reason": None,
        "related_conversation_ids": [],
    }


@pytest.fixture
def sample_conversation_minimal_data() -> Dict[str, Any]:
    """Provide minimal valid conversation data.

    Returns:
        Dictionary containing minimal valid conversation data.
    """
    return {
        "platform": "linkedin",
        "recruiter_name": "Jane Recruiter",
    }


@pytest.fixture
def invalid_platform_data() -> Dict[str, Any]:
    """Provide data with invalid platform value.

    Returns:
        Dictionary containing invalid platform data.
    """
    return {
        "platform": "invalid_platform",
        "recruiter_name": "Test Recruiter",
    }


# ============================================
# USER SETTINGS FIXTURES
# ============================================


@pytest.fixture
def sample_user_settings_data() -> Dict[str, Any]:
    """Provide sample user settings data.

    Returns:
        Dictionary containing valid user settings data.
    """
    return {
        "user_name": "John Doe",
        "user_email": "john.doe@example.com",
        "default_model": "sonnet",
        "resume_path": "./data/settings/resume.md",
        "preferences": {
            "auto_analyze": True,
            "notification_enabled": False,
        },
    }


# ============================================
# YAML SERIALIZATION FIXTURES
# ============================================


@pytest.fixture
def sample_yaml_conversation() -> str:
    """Provide sample YAML conversation content.

    Returns:
        String containing valid YAML conversation data.
    """
    return """
id: "550e8400-e29b-41d4-a716-446655440000"
created_at: 2025-12-09T10:00:00+00:00
updated_at: 2025-12-09T15:30:00+00:00

platform: linkedin
company: Company A
recruiter_name: John Recruiter
process_status: interested

context:
  - "$150,000 yearly is in the lower range of my acceptable range"

messages:
  - timestamp: 2025-12-09T10:00:00+00:00
    from_name: John Recruiter
    subject: "Senior Engineer Position at Company A"
    body: |
      Hi! I came across your profile and think you'd be a great fit
      for our Senior Software Engineer position.
    attachments: []

archived: false
related_conversation_ids: []
"""
