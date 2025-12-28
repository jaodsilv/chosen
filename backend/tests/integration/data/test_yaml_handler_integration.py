"""Integration tests for YAMLHandler class.

This module contains integration tests that verify YAMLHandler operations
with real filesystem interactions and the actual Pydantic models used
in the application.
"""

import asyncio
from pathlib import Path
from typing import Any, Dict

import pytest

from app.data.file_handler import FileHandler
from app.data.yaml_handler import YAMLHandler
from app.models.analysis import ContextAnalysis, JobFitScore
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.metrics import ResponseMetrics
from app.models.settings import UserSettings

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def file_handler() -> FileHandler:
    """Create a real FileHandler instance."""
    return FileHandler()


@pytest.fixture
def yaml_handler(file_handler: FileHandler) -> YAMLHandler:
    """Create YAMLHandler with real FileHandler."""
    return YAMLHandler(file_handler)


# =============================================================================
# Tests with Real Application Models
# =============================================================================


@pytest.mark.integration
class TestYAMLHandlerWithRealModels:
    """Integration tests using actual application models."""

    async def test_conversation_save_and_load(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        sample_conversation_data: Dict[str, Any],
    ) -> None:
        """Test saving and loading a Conversation model."""
        original = Conversation(**sample_conversation_data)
        file_path = tmp_path / "conversation.yaml"

        await yaml_handler.save(original, file_path)
        loaded = await yaml_handler.load(file_path, Conversation)

        assert loaded.id == original.id
        assert loaded.platform == original.platform
        assert loaded.company == original.company
        assert loaded.recruiter_name == original.recruiter_name
        assert len(loaded.messages) == len(original.messages)

    async def test_conversation_minimal_save_and_load(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        sample_conversation_minimal_data: Dict[str, Any],
    ) -> None:
        """Test saving and loading a minimal Conversation model."""
        original = Conversation(**sample_conversation_minimal_data)
        file_path = tmp_path / "conversation_minimal.yaml"

        await yaml_handler.save(original, file_path)
        loaded = await yaml_handler.load(file_path, Conversation)

        assert loaded.platform == original.platform
        assert loaded.recruiter_name == original.recruiter_name
        assert loaded.company is None
        assert loaded.messages == []

    def test_message_round_trip(
        self,
        yaml_handler: YAMLHandler,
        sample_message_data: Dict[str, Any],
    ) -> None:
        """Test Message model round-trip through YAML."""
        original = Message(**sample_message_data)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, Message)

        assert restored.from_name == original.from_name
        assert restored.to_name == original.to_name
        assert restored.subject == original.subject
        assert restored.body == original.body
        assert restored.attachments == original.attachments

    def test_context_analysis_round_trip(
        self,
        yaml_handler: YAMLHandler,
        sample_context_analysis_data: Dict[str, Any],
    ) -> None:
        """Test ContextAnalysis with frozen nested models."""
        original = ContextAnalysis(**sample_context_analysis_data)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, ContextAnalysis)

        assert restored.summary == original.summary
        assert restored.sentiment_trend.initial == original.sentiment_trend.initial
        assert restored.sentiment_trend.current == original.sentiment_trend.current
        assert restored.conversation_stage.current == original.conversation_stage.current
        assert restored.patterns_detected == original.patterns_detected
        assert restored.recommendations == original.recommendations

    def test_job_fit_score_round_trip(
        self,
        yaml_handler: YAMLHandler,
        sample_job_fit_score_data: Dict[str, Any],
    ) -> None:
        """Test JobFitScore with nested frozen models."""
        original = JobFitScore(**sample_job_fit_score_data)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, JobFitScore)

        assert restored.overall_score == original.overall_score
        assert restored.required_skills_score == original.required_skills_score
        assert restored.preferred_skills_score == original.preferred_skills_score
        assert restored.experience_match == original.experience_match
        assert restored.strengths == original.strengths
        assert len(restored.gaps) == len(original.gaps)
        assert restored.breakdown == original.breakdown

    def test_response_metrics_round_trip(
        self,
        yaml_handler: YAMLHandler,
        sample_response_metrics_data: Dict[str, Any],
    ) -> None:
        """Test ResponseMetrics round-trip."""
        original = ResponseMetrics(**sample_response_metrics_data)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, ResponseMetrics)

        assert restored.recruiter_avg_hours == original.recruiter_avg_hours
        assert restored.candidate_avg_hours == original.candidate_avg_hours
        assert restored.recruiter_message_count == original.recruiter_message_count
        assert restored.candidate_message_count == original.candidate_message_count

    def test_user_settings_round_trip(
        self,
        yaml_handler: YAMLHandler,
        sample_user_settings_data: Dict[str, Any],
    ) -> None:
        """Test UserSettings model round-trip."""
        original = UserSettings(**sample_user_settings_data)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, UserSettings)

        assert restored.user_name == original.user_name
        assert restored.user_email == original.user_email
        assert restored.default_model == original.default_model
        assert restored.resume_path == original.resume_path
        assert restored.preferences == original.preferences


# =============================================================================
# File Lifecycle Tests
# =============================================================================


@pytest.mark.integration
class TestYAMLHandlerFileLifecycle:
    """Integration tests for complete file lifecycle."""

    async def test_full_yaml_file_lifecycle(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        sample_conversation_data: Dict[str, Any],
    ) -> None:
        """Test create, read, update cycle."""
        file_path = tmp_path / "lifecycle.yaml"

        # Create
        original = Conversation(**sample_conversation_data)
        await yaml_handler.save(original, file_path)
        assert file_path.exists()

        # Read
        loaded = await yaml_handler.load(file_path, Conversation)
        assert loaded.id == original.id

        # Update (using model_copy for immutable update)
        updated = loaded.model_copy(update={"company": "Updated Company"})
        await yaml_handler.save(updated, file_path)

        # Verify update
        reloaded = await yaml_handler.load(file_path, Conversation)
        assert reloaded.company == "Updated Company"
        assert reloaded.id == original.id  # Other fields preserved

    async def test_yaml_file_content_is_human_readable(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        file_handler: FileHandler,
        sample_conversation_data: Dict[str, Any],
    ) -> None:
        """Test that saved YAML files are human-readable."""
        original = Conversation(**sample_conversation_data)
        file_path = tmp_path / "readable.yaml"

        await yaml_handler.save(original, file_path)

        # Read raw content
        content = await file_handler.read_file(file_path)

        # Verify YAML structure is human-readable
        assert "platform:" in content
        assert "recruiter_name:" in content
        assert "messages:" in content
        assert "Company A" in content
        assert "John Recruiter" in content

    async def test_yaml_file_uses_block_style(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        file_handler: FileHandler,
        sample_conversation_data: Dict[str, Any],
    ) -> None:
        """Test that YAML uses block style, not flow style."""
        original = Conversation(**sample_conversation_data)
        file_path = tmp_path / "block_style.yaml"

        await yaml_handler.save(original, file_path)
        content = await file_handler.read_file(file_path)

        # Block style should have newlines and indentation
        assert "\n" in content
        # Flow style would have inline braces like {key: value}
        # Block style should not have that for complex structures

    async def test_subdirectory_creation(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        sample_conversation_minimal_data: Dict[str, Any],
    ) -> None:
        """Test that save creates parent directories if needed."""
        file_path = tmp_path / "subdir1" / "subdir2" / "conversation.yaml"
        original = Conversation(**sample_conversation_minimal_data)

        # Should not raise - creates directories
        await yaml_handler.save(original, file_path)

        assert file_path.exists()
        loaded = await yaml_handler.load(file_path, Conversation)
        assert loaded.recruiter_name == original.recruiter_name


# =============================================================================
# Edge Cases Tests
# =============================================================================


@pytest.mark.integration
class TestYAMLHandlerEdgeCases:
    """Integration tests for edge cases."""

    async def test_conversation_with_all_optional_fields(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        sample_conversation_data: Dict[str, Any],
        sample_context_analysis_data: Dict[str, Any],
        sample_job_fit_score_data: Dict[str, Any],
        sample_response_metrics_data: Dict[str, Any],
    ) -> None:
        """Test conversation with all optional fields populated."""
        full_data = {
            **sample_conversation_data,
            "context_analysis": sample_context_analysis_data,
            "fit_score": sample_job_fit_score_data,
            "response_metrics": sample_response_metrics_data,
        }
        original = Conversation(**full_data)
        file_path = tmp_path / "full_conversation.yaml"

        await yaml_handler.save(original, file_path)
        loaded = await yaml_handler.load(file_path, Conversation)

        assert loaded.context_analysis is not None
        assert loaded.fit_score is not None
        assert loaded.response_metrics is not None
        assert original.context_analysis is not None
        assert original.fit_score is not None
        assert loaded.context_analysis.summary == original.context_analysis.summary
        assert loaded.fit_score.overall_score == original.fit_score.overall_score

    def test_parse_existing_yaml_format(
        self,
        yaml_handler: YAMLHandler,
        sample_yaml_conversation: str,
    ) -> None:
        """Test parsing existing YAML format from SYSTEM-DESIGN."""
        conv = yaml_handler.deserialize(sample_yaml_conversation, Conversation)

        assert conv.id == "550e8400-e29b-41d4-a716-446655440000"
        assert conv.platform == "linkedin"
        assert conv.company == "Company A"
        assert conv.recruiter_name == "John Recruiter"
        assert conv.process_status == "interested"
        assert len(conv.messages) == 1
        assert conv.archived is False

    async def test_unicode_content_preserved(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        fixed_datetime: Any,
    ) -> None:
        """Test that Unicode content is preserved through save/load."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Tanaka Taro",
            body="Hello World! Japanese: Test",
        )
        file_path = tmp_path / "unicode.yaml"

        await yaml_handler.save(message, file_path)
        loaded = await yaml_handler.load(file_path, Message)

        assert loaded.from_name == "Tanaka Taro"
        assert "Japanese" in loaded.body

    async def test_multiline_message_body_preserved(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        fixed_datetime: Any,
    ) -> None:
        """Test that multiline message body is preserved."""
        multiline_body = """Hello!

This is a multi-paragraph message.

With multiple lines.

Best regards,
Recruiter"""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body=multiline_body,
        )
        file_path = tmp_path / "multiline.yaml"

        await yaml_handler.save(message, file_path)
        loaded = await yaml_handler.load(file_path, Message)

        assert loaded.body == multiline_body
        assert "\n\n" in loaded.body

    async def test_special_yaml_characters_preserved(
        self,
        tmp_path: Path,
        yaml_handler: YAMLHandler,
        fixed_datetime: Any,
    ) -> None:
        """Test that special YAML characters are preserved."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            subject="RE: Position - $150K - 10% bonus",
            body="Terms: yes/no, true/false, null, ~, |, >, *, &, !, %, @, #",
        )
        file_path = tmp_path / "special_chars.yaml"

        await yaml_handler.save(message, file_path)
        loaded = await yaml_handler.load(file_path, Message)

        assert loaded.subject is not None
        assert "$150K" in loaded.subject
        assert "yes/no" in loaded.body
        assert "true/false" in loaded.body

    async def test_concurrent_save_with_file_locking(
        self,
        tmp_path: Path,
        file_handler: FileHandler,
        sample_conversation_minimal_data: Dict[str, Any],
    ) -> None:
        """Test concurrent saves with file locking pattern.

        Demonstrates the recommended pattern for concurrent access:
        use FileHandler.locked() to acquire exclusive access before
        save operations.
        """
        file_path = tmp_path / "concurrent.yaml"
        yaml_handler = YAMLHandler(file_handler)

        async def save_with_lock(company_name: str) -> None:
            """Save with lock to demonstrate safe concurrent pattern."""
            async with file_handler.locked(file_path):
                conv = Conversation(**{**sample_conversation_minimal_data, "company": company_name})
                await yaml_handler.save(conv, file_path)

        # Run multiple concurrent saves with locking
        await asyncio.gather(
            save_with_lock("Company A"),
            save_with_lock("Company B"),
            save_with_lock("Company C"),
        )

        # Verify file exists and contains valid YAML
        loaded = await yaml_handler.load(file_path, Conversation)
        assert loaded.company in ["Company A", "Company B", "Company C"]
