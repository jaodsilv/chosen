"""Unit tests for Message Pydantic model.

This module contains tests for the Message model which represents
individual messages in a conversation with fields:
    - timestamp (datetime, required)
    - from_name (str, required)
    - to_name (str, optional)
    - subject (str, optional)
    - body (str, required)
    - attachments (List[str], default empty list)
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.message import Message


@pytest.mark.unit
class TestMessageCreation:
    """Test suite for Message model creation."""

    def test_message_with_all_fields(self, sample_message_data: Dict[str, Any]) -> None:
        """Test creating Message with all fields populated."""
        message = Message(**sample_message_data)

        assert message.timestamp == sample_message_data["timestamp"]
        assert message.from_name == sample_message_data["from_name"]
        assert message.to_name == sample_message_data["to_name"]
        assert message.subject == sample_message_data["subject"]
        assert message.body == sample_message_data["body"]
        assert message.attachments == sample_message_data["attachments"]

    def test_message_with_required_fields_only(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test creating Message with only required fields."""
        message = Message(**sample_message_minimal_data)

        assert message.timestamp == sample_message_minimal_data["timestamp"]
        assert message.from_name == sample_message_minimal_data["from_name"]
        assert message.body == sample_message_minimal_data["body"]
        assert message.to_name is None
        assert message.subject is None
        assert message.attachments == []

    def test_message_missing_timestamp_raises_error(self) -> None:
        """Test that missing timestamp raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Message(from_name="Recruiter", body="Message body")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("timestamp",) for e in errors)

    def test_message_missing_from_name_raises_error(
        self, fixed_datetime: datetime
    ) -> None:
        """Test that missing from_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Message(timestamp=fixed_datetime, body="Message body")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("from_name",) for e in errors)

    def test_message_missing_body_raises_error(self, fixed_datetime: datetime) -> None:
        """Test that missing body raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Message(timestamp=fixed_datetime, from_name="Recruiter")

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("body",) for e in errors)


@pytest.mark.unit
class TestMessageDefaults:
    """Test suite for Message model default values."""

    def test_to_name_defaults_to_none(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test that to_name defaults to None when not provided."""
        message = Message(**sample_message_minimal_data)
        assert message.to_name is None

    def test_subject_defaults_to_none(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test that subject defaults to None when not provided."""
        message = Message(**sample_message_minimal_data)
        assert message.subject is None

    def test_attachments_defaults_to_empty_list(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test that attachments defaults to empty list when not provided."""
        message = Message(**sample_message_minimal_data)
        assert message.attachments == []
        assert isinstance(message.attachments, list)

    def test_attachments_default_is_new_list_per_instance(
        self, fixed_datetime: datetime
    ) -> None:
        """Test that attachments default creates new list per instance."""
        message1 = Message(
            timestamp=fixed_datetime, from_name="Recruiter", body="Body 1"
        )
        message2 = Message(
            timestamp=fixed_datetime, from_name="Recruiter", body="Body 2"
        )

        # Modify one instance's attachments
        message1.attachments.append("file.pdf")

        # Ensure the other instance is not affected
        assert message1.attachments == ["file.pdf"]
        assert message2.attachments == []


@pytest.mark.unit
class TestMessageValidation:
    """Test suite for Message field validation."""

    def test_timestamp_accepts_datetime(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test timestamp accepts datetime object."""
        message = Message(**sample_message_minimal_data)
        assert isinstance(message.timestamp, datetime)

    def test_timestamp_accepts_iso_string(self) -> None:
        """Test timestamp accepts ISO format string."""
        message = Message(
            timestamp="2025-12-09T10:00:00Z",
            from_name="Recruiter",
            body="Message body",
        )
        assert isinstance(message.timestamp, datetime)
        assert message.timestamp.year == 2025
        assert message.timestamp.month == 12
        assert message.timestamp.day == 9

    def test_timestamp_rejects_invalid_format(self) -> None:
        """Test timestamp rejects invalid datetime format."""
        with pytest.raises(ValidationError):
            Message(
                timestamp="not-a-date",
                from_name="Recruiter",
                body="Message body",
            )

    def test_from_name_accepts_string(
        self, sample_message_minimal_data: Dict[str, Any]
    ) -> None:
        """Test from_name accepts string value."""
        message = Message(**sample_message_minimal_data)
        assert isinstance(message.from_name, str)

    def test_body_accepts_multiline_string(self, fixed_datetime: datetime) -> None:
        """Test body accepts multiline string content."""
        multiline_body = """Hi!

        I came across your profile and think you'd be a great fit.

        Best regards,
        Recruiter"""

        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body=multiline_body,
        )
        assert "\n" in message.body
        assert "Best regards" in message.body

    def test_attachments_accepts_list_of_strings(
        self, sample_message_data: Dict[str, Any]
    ) -> None:
        """Test attachments accepts list of string paths."""
        message = Message(**sample_message_data)
        assert all(isinstance(a, str) for a in message.attachments)

    def test_attachments_rejects_non_string_items(
        self, fixed_datetime: datetime
    ) -> None:
        """Test attachments rejects list with non-string items."""
        with pytest.raises(ValidationError):
            Message(
                timestamp=fixed_datetime,
                from_name="Recruiter",
                body="Body",
                attachments=[123, 456],  # type: ignore
            )


@pytest.mark.unit
class TestMessageSerialization:
    """Test suite for Message serialization."""

    def test_message_to_dict(self, sample_message_data: Dict[str, Any]) -> None:
        """Test Message.model_dump() produces correct dict."""
        message = Message(**sample_message_data)
        data = message.model_dump()

        assert data["from_name"] == sample_message_data["from_name"]
        assert data["to_name"] == sample_message_data["to_name"]
        assert data["subject"] == sample_message_data["subject"]
        assert data["body"] == sample_message_data["body"]
        assert data["attachments"] == sample_message_data["attachments"]

    def test_message_to_json(self, sample_message_data: Dict[str, Any]) -> None:
        """Test Message.model_dump_json() produces valid JSON."""
        message = Message(**sample_message_data)
        json_str = message.model_dump_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["from_name"] == sample_message_data["from_name"]
        assert parsed["body"] == sample_message_data["body"]

    def test_message_from_dict(self, sample_message_data: Dict[str, Any]) -> None:
        """Test creating Message from dictionary."""
        message = Message.model_validate(sample_message_data)

        assert message.from_name == sample_message_data["from_name"]
        assert message.body == sample_message_data["body"]

    def test_message_from_json(self, sample_message_data: Dict[str, Any]) -> None:
        """Test Message.model_validate_json() parses JSON correctly."""
        # First create and serialize
        message = Message(**sample_message_data)
        json_str = message.model_dump_json()

        # Then parse back
        restored = Message.model_validate_json(json_str)
        assert restored.from_name == message.from_name
        assert restored.body == message.body

    def test_message_timestamp_serializes_to_iso_format(
        self, sample_message_data: Dict[str, Any]
    ) -> None:
        """Test timestamp serializes to ISO format string in JSON."""
        message = Message(**sample_message_data)
        json_str = message.model_dump_json()
        parsed = json.loads(json_str)

        # Should be ISO format string
        assert isinstance(parsed["timestamp"], str)
        # Should be parseable back to datetime
        datetime.fromisoformat(parsed["timestamp"].replace("Z", "+00:00"))

    def test_message_round_trip(self, sample_message_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = Message(**sample_message_data)
        json_str = original.model_dump_json()
        restored = Message.model_validate_json(json_str)

        assert restored.from_name == original.from_name
        assert restored.to_name == original.to_name
        assert restored.subject == original.subject
        assert restored.body == original.body
        assert restored.attachments == original.attachments


@pytest.mark.unit
class TestMessageEdgeCases:
    """Test suite for Message edge cases."""

    def test_message_with_empty_attachments_list(
        self, fixed_datetime: datetime
    ) -> None:
        """Test explicitly passing empty attachments list."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body="Body",
            attachments=[],
        )
        assert message.attachments == []

    def test_message_with_very_long_body(self, fixed_datetime: datetime) -> None:
        """Test Message handles very long body text."""
        long_body = "x" * 100000  # 100KB of text
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body=long_body,
        )
        assert len(message.body) == 100000

    def test_message_with_unicode_characters(self, fixed_datetime: datetime) -> None:
        """Test Message handles unicode in body and names."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="田中太郎",
            body="こんにちは！興味がありますか？🎉",
        )
        assert message.from_name == "田中太郎"
        assert "🎉" in message.body

    def test_message_with_special_characters_in_subject(
        self, fixed_datetime: datetime
    ) -> None:
        """Test subject with special characters."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body="Body",
            subject='RE: "Senior Engineer" [URGENT] <action required>',
        )
        assert '"' in message.subject
        assert "[" in message.subject
        assert "<" in message.subject

    def test_message_with_timezone_aware_datetime(self) -> None:
        """Test Message with timezone-aware datetime."""
        tz_aware = datetime(2025, 12, 9, 10, 0, 0, tzinfo=timezone.utc)
        message = Message(
            timestamp=tz_aware,
            from_name="Recruiter",
            body="Body",
        )
        assert message.timestamp.tzinfo is not None

    def test_message_with_naive_datetime(self) -> None:
        """Test Message with naive (no timezone) datetime."""
        naive = datetime(2025, 12, 9, 10, 0, 0)
        message = Message(
            timestamp=naive,
            from_name="Recruiter",
            body="Body",
        )
        assert message.timestamp.year == 2025
