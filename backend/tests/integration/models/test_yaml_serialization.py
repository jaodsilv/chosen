"""Integration tests for YAML serialization of Pydantic models.

This module tests round-trip serialization through YAML,
which is critical for the file-based storage system.
"""

from datetime import datetime
from typing import Any, Dict

import pytest
import yaml

from app.models.analysis import ContextAnalysis, JobFitScore
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.metrics import ResponseMetrics
from app.models.settings import UserSettings


@pytest.mark.integration
class TestConversationYamlRoundTrip:
    """Test suite for Conversation YAML round-trip serialization."""

    def test_conversation_to_yaml_and_back(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test Conversation serializes to YAML and deserializes correctly."""
        original = Conversation(**sample_conversation_data)

        # Serialize to YAML
        data = original.model_dump(mode="json")  # JSON-compatible format
        yaml_str = yaml.dump(data, default_flow_style=False)

        # Deserialize from YAML
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.id == original.id
        assert restored.platform == original.platform
        assert restored.company == original.company
        assert restored.recruiter_name == original.recruiter_name

    def test_conversation_yaml_preserves_datetime(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test datetime fields survive YAML round-trip."""
        original = Conversation(**sample_conversation_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        # Timestamps should be preserved
        assert restored.created_at.year == original.created_at.year
        assert restored.created_at.month == original.created_at.month
        assert restored.created_at.day == original.created_at.day

    def test_conversation_yaml_preserves_uuid(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test UUID field survives YAML round-trip."""
        original = Conversation(**sample_conversation_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.id == original.id

    def test_conversation_yaml_preserves_enums(
        self, sample_conversation_data: Dict[str, Any]
    ) -> None:
        """Test enum fields survive YAML round-trip."""
        original = Conversation(**sample_conversation_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.platform == original.platform
        assert restored.process_status == original.process_status

    def test_conversation_yaml_preserves_nested_models(
        self,
        sample_conversation_minimal_data: Dict[str, Any],
        sample_context_analysis_data: Dict[str, Any],
    ) -> None:
        """Test nested models survive YAML round-trip."""
        conv_data = {
            **sample_conversation_minimal_data,
            "context_analysis": sample_context_analysis_data,
        }
        original = Conversation(**conv_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.context_analysis is not None
        assert restored.context_analysis.summary == original.context_analysis.summary
        assert (
            restored.context_analysis.sentiment_trend.initial
            == original.context_analysis.sentiment_trend.initial
        )

    def test_parse_existing_yaml_format(self, sample_yaml_conversation: str) -> None:
        """Test parsing existing YAML format from SYSTEM-DESIGN."""
        loaded_data = yaml.safe_load(sample_yaml_conversation)
        conv = Conversation.model_validate(loaded_data)

        assert conv.id == "550e8400-e29b-41d4-a716-446655440000"
        assert conv.platform == "linkedin"
        assert conv.company == "Company A"
        assert conv.recruiter_name == "John Recruiter"
        assert conv.process_status == "interested"
        assert len(conv.messages) == 1
        assert conv.archived is False


@pytest.mark.integration
class TestMessageYamlRoundTrip:
    """Test suite for Message YAML round-trip serialization."""

    def test_message_to_yaml_and_back(
        self, sample_message_data: Dict[str, Any]
    ) -> None:
        """Test Message serializes to YAML and deserializes correctly."""
        original = Message(**sample_message_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Message.model_validate(loaded_data)

        assert restored.from_name == original.from_name
        assert restored.to_name == original.to_name
        assert restored.subject == original.subject
        assert restored.body == original.body

    def test_message_multiline_body_in_yaml(self, fixed_datetime: datetime) -> None:
        """Test multiline body text preserves in YAML."""
        multiline_body = """Hi!

I came across your profile and wanted to reach out.

This is a multi-paragraph message with:
- Bullet points
- And special characters: "quotes", 'apostrophes'

Best regards,
Recruiter"""

        original = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body=multiline_body,
        )

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Message.model_validate(loaded_data)

        assert restored.body == multiline_body
        assert "\n" in restored.body
        assert "Bullet points" in restored.body

    def test_message_list_in_yaml(
        self, sample_message_data: Dict[str, Any], fixed_datetime: datetime
    ) -> None:
        """Test list of messages serializes correctly to YAML."""
        messages = [
            Message(**sample_message_data),
            Message(
                timestamp=fixed_datetime,
                from_name="Another Person",
                body="Another message",
            ),
        ]

        data = [m.model_dump(mode="json") for m in messages]
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = [Message.model_validate(d) for d in loaded_data]

        assert len(restored) == 2
        assert restored[0].from_name == messages[0].from_name
        assert restored[1].from_name == messages[1].from_name


@pytest.mark.integration
class TestAnalysisYamlRoundTrip:
    """Test suite for analysis models YAML round-trip."""

    def test_context_analysis_yaml_round_trip(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
        """Test ContextAnalysis YAML round-trip."""
        original = ContextAnalysis(**sample_context_analysis_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = ContextAnalysis.model_validate(loaded_data)

        assert restored.summary == original.summary
        assert restored.sentiment_trend.initial == original.sentiment_trend.initial
        assert (
            restored.conversation_stage.current == original.conversation_stage.current
        )
        assert restored.patterns_detected == original.patterns_detected

    def test_job_fit_score_yaml_round_trip(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test JobFitScore YAML round-trip."""
        original = JobFitScore(**sample_job_fit_score_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = JobFitScore.model_validate(loaded_data)

        assert restored.overall_score == original.overall_score
        assert restored.required_skills_score == original.required_skills_score
        assert restored.strengths == original.strengths
        assert restored.gaps == original.gaps
        assert restored.breakdown == original.breakdown

    def test_response_metrics_yaml_round_trip(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test ResponseMetrics YAML round-trip."""
        original = ResponseMetrics(**sample_response_metrics_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = ResponseMetrics.model_validate(loaded_data)

        assert restored.recruiter_avg_hours == original.recruiter_avg_hours
        assert restored.candidate_avg_hours == original.candidate_avg_hours
        assert restored.recruiter_message_count == original.recruiter_message_count


@pytest.mark.integration
class TestUserSettingsYamlRoundTrip:
    """Test suite for UserSettings YAML round-trip."""

    def test_user_settings_yaml_round_trip(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test UserSettings YAML round-trip."""
        original = UserSettings(**sample_user_settings_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = UserSettings.model_validate(loaded_data)

        assert restored.user_name == original.user_name
        assert restored.user_email == original.user_email
        assert restored.default_model == original.default_model
        assert restored.resume_path == original.resume_path
        assert restored.preferences == original.preferences


@pytest.mark.integration
class TestYamlSpecialCases:
    """Test suite for YAML special cases."""

    def test_yaml_with_none_values(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test YAML handles None values correctly."""
        original = Conversation(**sample_conversation_minimal_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.company is None
        assert restored.context_analysis is None

    def test_yaml_with_empty_lists(
        self, sample_conversation_minimal_data: Dict[str, Any]
    ) -> None:
        """Test YAML handles empty lists correctly."""
        original = Conversation(**sample_conversation_minimal_data)

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Conversation.model_validate(loaded_data)

        assert restored.messages == []
        assert restored.context == []

    def test_yaml_with_unicode(self, fixed_datetime: datetime) -> None:
        """Test YAML handles unicode characters correctly."""
        original = Message(
            timestamp=fixed_datetime,
            from_name="田中太郎",
            body="こんにちは！興味がありますか？🎉",
        )

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Message.model_validate(loaded_data)

        assert restored.from_name == "田中太郎"
        assert "🎉" in restored.body

    def test_yaml_with_special_yaml_characters(self, fixed_datetime: datetime) -> None:
        """Test YAML handles special YAML characters correctly."""
        original = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            subject="RE: Position - $150K - 10% bonus",
            body="Terms: yes/no, true/false, null, ~, |, >, *, &, !, %, @, #",
        )

        data = original.model_dump(mode="json")
        yaml_str = yaml.dump(data, default_flow_style=False)
        loaded_data = yaml.safe_load(yaml_str)
        restored = Message.model_validate(loaded_data)

        assert "$150K" in restored.subject
        assert "yes/no" in restored.body
        assert "true/false" in restored.body
