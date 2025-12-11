"""Unit tests for Conversation Pydantic model.

This module contains tests for:
    - Conversation: Full conversation model with all fields
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID

import pytest
from pydantic import ValidationError

from app.models.analysis import ContextAnalysis, JobFitScore
from app.models.conversation import Conversation
from app.models.enums import Platform, ProcessStatus
from app.models.message import Message
from app.models.metrics import ResponseMetrics


@pytest.mark.unit
class TestConversationCreation:
    """Test suite for Conversation model creation."""

    def test_conversation_with_all_fields(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test creating Conversation with all fields populated."""
        conv = Conversation(**sample_conversation_data)

        assert conv.id == sample_conversation_data["id"]
        assert conv.created_at == sample_conversation_data["created_at"]
        assert conv.updated_at == sample_conversation_data["updated_at"]
        assert conv.platform == Platform.LINKEDIN
        assert conv.company == sample_conversation_data["company"]
        assert conv.recruiter_name == sample_conversation_data["recruiter_name"]
        assert conv.process_status == ProcessStatus.NEW
        assert conv.context == sample_conversation_data["context"]
        assert len(conv.messages) == 1
        assert conv.archived == sample_conversation_data["archived"]

    def test_conversation_with_minimal_fields(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test creating Conversation with only required fields."""
        conv = Conversation(**sample_conversation_minimal_data)

        assert conv.platform == Platform.LINKEDIN
        assert conv.recruiter_name == sample_conversation_minimal_data["recruiter_name"]
        # Check defaults
        assert conv.id is not None  # Auto-generated
        assert conv.created_at is not None  # Auto-generated
        assert conv.process_status == ProcessStatus.NEW
        assert conv.messages == []
        assert conv.archived is False

    def test_conversation_missing_platform_raises_error(self) -> None:
        """Test missing platform raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Conversation(recruiter_name="Test Recruiter")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("platform",) for e in errors)

    def test_conversation_missing_recruiter_name_raises_error(self) -> None:
        """Test missing recruiter_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Conversation(platform="linkedin")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("recruiter_name",) for e in errors)


@pytest.mark.unit
class TestConversationDefaults:
    """Test suite for Conversation default values."""

    def test_company_defaults_to_none(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test company defaults to None."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.company is None

    def test_recruiting_company_defaults_to_none(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test recruiting_company defaults to None."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.recruiting_company is None

    def test_process_status_defaults_to_new(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test process_status defaults to ProcessStatus.NEW."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.process_status == ProcessStatus.NEW

    def test_context_defaults_to_empty_list(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test context defaults to empty list."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.context == []

    def test_messages_defaults_to_empty_list(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test messages defaults to empty list."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.messages == []

    def test_analysis_fields_default_to_none(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test context_analysis, fit_score, response_metrics default to None."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.context_analysis is None
        assert conv.fit_score is None
        assert conv.response_metrics is None

    def test_archived_defaults_to_false(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test archived defaults to False."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.archived is False

    def test_related_conversation_ids_defaults_to_empty_list(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test related_conversation_ids defaults to empty list."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.related_conversation_ids == []


@pytest.mark.unit
class TestConversationPlatformValidation:
    """Test suite for Conversation platform field validation."""

    @pytest.mark.parametrize("platform", ["linkedin", "email", "phone", "in_person"])
    def test_conversation_accepts_valid_platforms(self, platform: str) -> None:
        """Test Conversation accepts all valid platform values."""
        conv = Conversation(platform=platform, recruiter_name="Test Recruiter")
        assert conv.platform == platform

    def test_conversation_rejects_invalid_platform(
        self, invalid_platform_data: Dict[str, Any]
    ) -> None:
        """Test Conversation rejects invalid platform value."""
        with pytest.raises(ValidationError) as exc_info:
            Conversation(**invalid_platform_data)

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("platform",) for e in errors)


@pytest.mark.unit
class TestConversationStatusValidation:
    """Test suite for Conversation process_status field validation."""

    @pytest.mark.parametrize(
        "status",
        [
            "new",
            "reviewing",
            "interested",
            "not_interested",
            "applied",
            "awaiting_response",
            "interviewing",
            "offer",
            "negotiating",
            "accepted",
            "declined",
            "rejected",
            "withdrawn",
            "ghosted",
        ],
    )
    def test_conversation_accepts_valid_status(self, status: str) -> None:
        """Test Conversation accepts all valid status values."""
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test Recruiter",
            process_status=status,
        )
        assert conv.process_status == status

    def test_conversation_rejects_invalid_status(self) -> None:
        """Test Conversation rejects invalid status value."""
        with pytest.raises(ValidationError):
            Conversation(
                platform="linkedin",
                recruiter_name="Test Recruiter",
                process_status="invalid_status",
            )


@pytest.mark.unit
class TestConversationNestedModels:
    """Test suite for Conversation nested model handling."""

    def test_conversation_with_nested_messages(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test Conversation with nested Message models."""
        conv = Conversation(**sample_conversation_data)

        assert len(conv.messages) == 1
        assert isinstance(conv.messages[0], Message)
        assert conv.messages[0].from_name == "John Recruiter"

    def test_conversation_with_context_analysis(
        self,
        sample_conversation_minimal_data: Dict[str, Any],
        sample_context_analysis_data: Dict[str, Any],
    ) -> None:
        """Test Conversation with nested ContextAnalysis."""
        data = {
            **sample_conversation_minimal_data,
            "context_analysis": sample_context_analysis_data,
        }
        conv = Conversation(**data)

        assert isinstance(conv.context_analysis, ContextAnalysis)
        assert conv.context_analysis.summary == sample_context_analysis_data["summary"]

    def test_conversation_with_fit_score(
        self,
        sample_conversation_minimal_data: Dict[str, Any],
        sample_job_fit_score_data: Dict[str, Any],
    ) -> None:
        """Test Conversation with nested FitScore."""
        data = {
            **sample_conversation_minimal_data,
            "fit_score": sample_job_fit_score_data,
        }
        conv = Conversation(**data)

        assert isinstance(conv.fit_score, JobFitScore)
        assert (
            conv.fit_score.overall_score == sample_job_fit_score_data["overall_score"]
        )

    def test_conversation_with_response_metrics(
        self,
        sample_conversation_minimal_data: Dict[str, Any],
        sample_response_metrics_data: Dict[str, Any],
    ) -> None:
        """Test Conversation with nested ResponseMetrics."""
        data = {
            **sample_conversation_minimal_data,
            "response_metrics": sample_response_metrics_data,
        }
        conv = Conversation(**data)

        assert isinstance(conv.response_metrics, ResponseMetrics)
        assert (
            conv.response_metrics.recruiter_message_count
            == sample_response_metrics_data["recruiter_message_count"]
        )


@pytest.mark.unit
class TestConversationUUIDGeneration:
    """Test suite for Conversation UUID auto-generation."""

    def test_conversation_auto_generates_id(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test Conversation auto-generates UUID id."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.id is not None
        assert len(conv.id) > 0

    def test_conversation_id_is_valid_uuid(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test auto-generated id is valid UUID."""
        conv = Conversation(**sample_conversation_minimal_data)
        # Should not raise
        UUID(conv.id)

    def test_conversation_respects_provided_id(self, fixed_uuid_str: str) -> None:
        """Test Conversation uses provided id when given."""
        conv = Conversation(
            id=fixed_uuid_str,
            platform="linkedin",
            recruiter_name="Test",
        )
        assert conv.id == fixed_uuid_str

    def test_multiple_conversations_get_unique_ids(self) -> None:
        """Test each new Conversation gets unique id."""
        conv1 = Conversation(platform="linkedin", recruiter_name="Test 1")
        conv2 = Conversation(platform="linkedin", recruiter_name="Test 2")

        assert conv1.id != conv2.id


@pytest.mark.unit
class TestConversationTimestampGeneration:
    """Test suite for Conversation timestamp auto-generation."""

    def test_conversation_auto_generates_created_at(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test Conversation auto-generates created_at timestamp."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.created_at is not None
        assert isinstance(conv.created_at, datetime)

    def test_conversation_auto_generates_updated_at(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test Conversation auto-generates updated_at timestamp."""
        conv = Conversation(**sample_conversation_minimal_data)
        assert conv.updated_at is not None
        assert isinstance(conv.updated_at, datetime)

    def test_conversation_respects_provided_timestamps(
        self, fixed_datetime: datetime
    ) -> None:
        """Test Conversation uses provided timestamps when given."""
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test",
            created_at=fixed_datetime,
            updated_at=fixed_datetime,
        )
        assert conv.created_at == fixed_datetime
        assert conv.updated_at == fixed_datetime


@pytest.mark.unit
class TestConversationSerialization:
    """Test suite for Conversation serialization."""

    def test_conversation_to_dict(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test Conversation.model_dump() produces correct dict."""
        conv = Conversation(**sample_conversation_data)
        data = conv.model_dump()

        assert data["id"] == sample_conversation_data["id"]
        assert data["company"] == sample_conversation_data["company"]
        assert data["recruiter_name"] == sample_conversation_data["recruiter_name"]

    def test_conversation_to_json(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test Conversation.model_dump_json() produces valid JSON."""
        conv = Conversation(**sample_conversation_data)
        json_str = conv.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["id"] == sample_conversation_data["id"]
        assert parsed["company"] == sample_conversation_data["company"]

    def test_conversation_enums_serialize_as_strings(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test platform and process_status serialize as string values."""
        conv = Conversation(**sample_conversation_data)
        data = conv.model_dump()

        # Should be string values, not enum objects
        assert data["platform"] == "linkedin"
        assert data["process_status"] == "new"

    def test_conversation_from_dict(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test creating Conversation from dictionary."""
        conv = Conversation.model_validate(sample_conversation_data)

        assert conv.id == sample_conversation_data["id"]
        assert conv.platform == Platform.LINKEDIN

    def test_conversation_nested_models_serialize(
        self,
        sample_conversation_minimal_data: Dict[str, Any],
        sample_context_analysis_data: Dict[str, Any],
    ) -> None:
        """Test nested models serialize correctly."""
        data = {
            **sample_conversation_minimal_data,
            "context_analysis": sample_context_analysis_data,
        }
        conv = Conversation(**data)
        serialized = conv.model_dump()

        assert isinstance(serialized["context_analysis"], dict)
        assert (
            serialized["context_analysis"]["summary"]
            == sample_context_analysis_data["summary"]
        )

    def test_conversation_round_trip(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = Conversation(**sample_conversation_data)
        json_str = original.model_dump_json()
        restored = Conversation.model_validate_json(json_str)

        assert restored.id == original.id
        assert restored.platform == original.platform
        assert restored.company == original.company
        assert restored.recruiter_name == original.recruiter_name
        assert restored.process_status == original.process_status
        assert restored.archived == original.archived


@pytest.mark.unit
class TestConversationConfigOptions:
    """Test suite for Conversation Config (use_enum_values, etc)."""

    def test_use_enum_values_enabled(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test use_enum_values=True in Config."""
        conv = Conversation(**sample_conversation_data)
        data = conv.model_dump()

        # Enums should serialize as values
        assert data["platform"] == "linkedin"
        assert data["process_status"] == "new"


@pytest.mark.unit
class TestConversationEdgeCases:
    """Test suite for Conversation edge cases."""

    def test_conversation_with_many_messages(self, fixed_datetime: datetime) -> None:
        """Test Conversation with many messages."""
        messages = [
            {
                "timestamp": fixed_datetime,
                "from_name": f"Person {i}",
                "body": f"Message {i}",
            }
            for i in range(100)
        ]
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test",
            messages=messages,
        )
        assert len(conv.messages) == 100

    def test_conversation_with_long_context_list(self) -> None:
        """Test Conversation with many context notes."""
        context = [f"Context note {i}" for i in range(50)]
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test",
            context=context,
        )
        assert len(conv.context) == 50

    def test_conversation_with_unicode_in_fields(self) -> None:
        """Test Conversation with unicode characters."""
        conv = Conversation(
            platform="linkedin",
            recruiter_name="田中太郎",
            company="日本株式会社",
            context=["給与は相談可能 🤝"],
        )
        assert conv.recruiter_name == "田中太郎"
        assert conv.company == "日本株式会社"
        assert "🤝" in conv.context[0]

    def test_conversation_archived_with_reason(self, fixed_datetime: datetime) -> None:
        """Test Conversation with archived status and reason."""
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test",
            archived=True,
            archived_at=fixed_datetime,
            archive_reason="Position filled",
        )
        assert conv.archived is True
        assert conv.archived_at == fixed_datetime
        assert conv.archive_reason == "Position filled"

    def test_conversation_with_related_conversations(self) -> None:
        """Test Conversation with related conversation IDs."""
        conv = Conversation(
            platform="linkedin",
            recruiter_name="Test",
            related_conversation_ids=[
                "uuid-1",
                "uuid-2",
                "uuid-3",
            ],
        )
        assert len(conv.related_conversation_ids) == 3
