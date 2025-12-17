"""Unit tests for analysis-related Pydantic models.

This module contains tests for:
    - SentimentTrend
    - ConversationStage
    - ActionItems
    - ContextAnalysis
"""

import json
from datetime import datetime
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.analysis import (
    ActionItems,
    ContextAnalysis,
    ConversationStage,
    SentimentTrend,
    SkillGap,
)


@pytest.mark.unit
class TestSentimentTrendCreation:
    """Test suite for SentimentTrend model."""

    def test_sentiment_trend_with_all_fields(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test creating SentimentTrend with all fields."""
        trend = SentimentTrend(**sample_sentiment_trend_data)

        assert trend.initial == sample_sentiment_trend_data["initial"]
        assert trend.current == sample_sentiment_trend_data["current"]
        assert trend.direction == sample_sentiment_trend_data["direction"]
        assert trend.indicators == sample_sentiment_trend_data["indicators"]

    def test_sentiment_trend_missing_initial_raises_error(self) -> None:
        """Test missing initial field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(  # type: ignore[call-arg]
                current="positive",
                direction="stable",
                indicators=("Test",),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("initial",) for e in errors)

    def test_sentiment_trend_missing_current_raises_error(self) -> None:
        """Test missing current field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(  # type: ignore[call-arg]
                initial="positive",
                direction="stable",
                indicators=("Test",),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("current",) for e in errors)

    def test_sentiment_trend_missing_direction_raises_error(self) -> None:
        """Test missing direction field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(  # type: ignore[call-arg]
                initial="positive",
                current="positive",
                indicators=("Test",),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("direction",) for e in errors)

    def test_sentiment_trend_missing_indicators_raises_error(self) -> None:
        """Test missing indicators field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(  # type: ignore[call-arg]
                initial="positive",
                current="positive",
                direction="stable",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("indicators",) for e in errors)

    def test_sentiment_trend_with_empty_indicators(self) -> None:
        """Test SentimentTrend with empty indicators tuple."""
        trend = SentimentTrend(
            initial="positive",
            current="positive",
            direction="stable",
            indicators=(),
        )
        assert trend.indicators == ()

    @pytest.mark.parametrize(
        "initial,current,direction",
        [
            ("positive", "positive", "stable"),
            ("neutral", "positive", "improving"),
            ("positive", "negative", "declining"),
            ("negative", "neutral", "improving"),
        ],
    )
    def test_sentiment_trend_various_combinations(self, initial: str, current: str, direction: str) -> None:
        """Test various sentiment combinations."""
        trend = SentimentTrend(
            initial=initial,  # type: ignore[arg-type]
            current=current,  # type: ignore[arg-type]
            direction=direction,  # type: ignore[arg-type]
            indicators=("Test indicator",),
        )
        assert trend.initial == initial
        assert trend.current == current
        assert trend.direction == direction


@pytest.mark.unit
class TestSentimentTrendSerialization:
    """Test suite for SentimentTrend serialization."""

    def test_sentiment_trend_to_dict(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test SentimentTrend.model_dump() produces correct dict."""
        trend = SentimentTrend(**sample_sentiment_trend_data)
        data = trend.model_dump()

        assert data["initial"] == sample_sentiment_trend_data["initial"]
        assert data["current"] == sample_sentiment_trend_data["current"]
        assert data["direction"] == sample_sentiment_trend_data["direction"]
        assert data["indicators"] == sample_sentiment_trend_data["indicators"]

    def test_sentiment_trend_round_trip(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = SentimentTrend(**sample_sentiment_trend_data)
        json_str = original.model_dump_json()
        restored = SentimentTrend.model_validate_json(json_str)

        assert restored.initial == original.initial
        assert restored.current == original.current
        assert restored.direction == original.direction
        assert restored.indicators == original.indicators


@pytest.mark.unit
class TestConversationStageCreation:
    """Test suite for ConversationStage model."""

    def test_conversation_stage_with_all_fields(self, sample_conversation_stage_data: Dict[str, Any]) -> None:
        """Test creating ConversationStage with all fields."""
        stage = ConversationStage(**sample_conversation_stage_data)

        assert stage.current == sample_conversation_stage_data["current"]
        assert stage.progression_quality == sample_conversation_stage_data["progression_quality"]

    def test_conversation_stage_missing_current_raises_error(self) -> None:
        """Test missing current field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConversationStage(progression_quality="smooth")  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("current",) for e in errors)

    def test_conversation_stage_missing_progression_quality_raises_error(self) -> None:
        """Test missing progression_quality raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConversationStage(current="initial_outreach")  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("progression_quality",) for e in errors)

    @pytest.mark.parametrize(
        "current",
        [
            "initial_outreach",
            "screening",
            "technical_interview",
            "final_round",
            "offer_stage",
            "negotiation",
        ],
    )
    def test_conversation_stage_various_stages(self, current: str) -> None:
        """Test various conversation stage values."""
        stage = ConversationStage(
            current=current,
            progression_quality="smooth",
        )
        assert stage.current == current


@pytest.mark.unit
class TestConversationStageSerialization:
    """Test suite for ConversationStage serialization."""

    def test_conversation_stage_to_dict(self, sample_conversation_stage_data: Dict[str, Any]) -> None:
        """Test ConversationStage.model_dump() produces correct dict."""
        stage = ConversationStage(**sample_conversation_stage_data)
        data = stage.model_dump()

        assert data["current"] == sample_conversation_stage_data["current"]
        assert data["progression_quality"] == sample_conversation_stage_data["progression_quality"]

    def test_conversation_stage_round_trip(self, sample_conversation_stage_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = ConversationStage(**sample_conversation_stage_data)
        json_str = original.model_dump_json()
        restored = ConversationStage.model_validate_json(json_str)

        assert restored.current == original.current
        assert restored.progression_quality == original.progression_quality


@pytest.mark.unit
class TestActionItemsCreation:
    """Test suite for ActionItems model."""

    def test_action_items_with_all_fields(self, sample_action_items_data: Dict[str, Any]) -> None:
        """Test creating ActionItems with all fields."""
        items = ActionItems(**sample_action_items_data)

        assert items.candidate_pending == sample_action_items_data["candidate_pending"]
        assert items.recruiter_pending == sample_action_items_data["recruiter_pending"]

    def test_action_items_defaults_to_empty_lists(self) -> None:
        """Test ActionItems defaults both lists to empty."""
        items = ActionItems()
        assert items.candidate_pending == []
        assert items.recruiter_pending == []

    def test_action_items_candidate_pending_only(self) -> None:
        """Test ActionItems with only candidate_pending."""
        items = ActionItems(candidate_pending=["Task 1", "Task 2"])
        assert items.candidate_pending == ["Task 1", "Task 2"]
        assert items.recruiter_pending == []

    def test_action_items_recruiter_pending_only(self) -> None:
        """Test ActionItems with only recruiter_pending."""
        items = ActionItems(recruiter_pending=["Task 1"])
        assert items.candidate_pending == []
        assert items.recruiter_pending == ["Task 1"]

    def test_action_items_with_multiple_items_each(self) -> None:
        """Test ActionItems with multiple items in each list."""
        items = ActionItems(
            candidate_pending=["Task A", "Task B", "Task C"],
            recruiter_pending=["Task X", "Task Y"],
        )
        assert len(items.candidate_pending) == 3
        assert len(items.recruiter_pending) == 2


@pytest.mark.unit
class TestActionItemsSerialization:
    """Test suite for ActionItems serialization."""

    def test_action_items_to_dict(self, sample_action_items_data: Dict[str, Any]) -> None:
        """Test ActionItems.model_dump() produces correct dict."""
        items = ActionItems(**sample_action_items_data)
        data = items.model_dump()

        assert data["candidate_pending"] == sample_action_items_data["candidate_pending"]
        assert data["recruiter_pending"] == sample_action_items_data["recruiter_pending"]

    def test_action_items_round_trip(self, sample_action_items_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = ActionItems(**sample_action_items_data)
        json_str = original.model_dump_json()
        restored = ActionItems.model_validate_json(json_str)

        assert restored.candidate_pending == original.candidate_pending
        assert restored.recruiter_pending == original.recruiter_pending


@pytest.mark.unit
class TestContextAnalysisCreation:
    """Test suite for ContextAnalysis model."""

    def test_context_analysis_with_all_fields(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test creating ContextAnalysis with all fields."""
        analysis = ContextAnalysis(**sample_context_analysis_data)

        assert analysis.summary == sample_context_analysis_data["summary"]
        assert analysis.patterns_detected == sample_context_analysis_data["patterns_detected"]
        assert analysis.recommendations == sample_context_analysis_data["recommendations"]
        assert analysis.last_analyzed == sample_context_analysis_data["last_analyzed"]

    def test_context_analysis_missing_summary_raises_error(
        self,
        sample_sentiment_trend_data: Dict[str, Any],
        sample_conversation_stage_data: Dict[str, Any],
        sample_action_items_data: Dict[str, Any],
        fixed_datetime: datetime,
    ) -> None:
        """Test missing summary raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ContextAnalysis(  # type: ignore[call-arg]
                sentiment_trend=SentimentTrend(**sample_sentiment_trend_data),
                conversation_stage=ConversationStage(**sample_conversation_stage_data),
                action_items=ActionItems(**sample_action_items_data),
                last_analyzed=fixed_datetime,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("summary",) for e in errors)

    def test_context_analysis_missing_sentiment_trend_raises_error(
        self,
        sample_conversation_stage_data: Dict[str, Any],
        sample_action_items_data: Dict[str, Any],
        fixed_datetime: datetime,
    ) -> None:
        """Test missing sentiment_trend raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ContextAnalysis(  # type: ignore[call-arg]
                summary="Test summary",
                conversation_stage=ConversationStage(**sample_conversation_stage_data),
                action_items=ActionItems(**sample_action_items_data),
                last_analyzed=fixed_datetime,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("sentiment_trend",) for e in errors)

    def test_context_analysis_missing_last_analyzed_raises_error(
        self,
        sample_sentiment_trend_data: Dict[str, Any],
        sample_conversation_stage_data: Dict[str, Any],
        sample_action_items_data: Dict[str, Any],
    ) -> None:
        """Test missing last_analyzed raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ContextAnalysis(  # type: ignore[call-arg]
                summary="Test summary",
                sentiment_trend=SentimentTrend(**sample_sentiment_trend_data),
                conversation_stage=ConversationStage(**sample_conversation_stage_data),
                action_items=ActionItems(**sample_action_items_data),
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("last_analyzed",) for e in errors)

    def test_context_analysis_defaults_for_lists(
        self,
        sample_sentiment_trend_data: Dict[str, Any],
        sample_conversation_stage_data: Dict[str, Any],
        sample_action_items_data: Dict[str, Any],
        fixed_datetime: datetime,
    ) -> None:
        """Test patterns_detected and recommendations default to empty lists."""
        analysis = ContextAnalysis(
            summary="Test summary",
            sentiment_trend=SentimentTrend(**sample_sentiment_trend_data),
            conversation_stage=ConversationStage(**sample_conversation_stage_data),
            action_items=ActionItems(**sample_action_items_data),
            last_analyzed=fixed_datetime,
        )
        assert analysis.patterns_detected == []
        assert analysis.recommendations == []


@pytest.mark.unit
class TestContextAnalysisNested:
    """Test suite for ContextAnalysis nested model handling."""

    def test_context_analysis_accepts_nested_dicts(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test ContextAnalysis accepts nested dictionaries for sub-models."""
        analysis = ContextAnalysis(**sample_context_analysis_data)

        # Nested models should be proper instances
        assert isinstance(analysis.sentiment_trend, SentimentTrend)
        assert isinstance(analysis.conversation_stage, ConversationStage)
        assert isinstance(analysis.action_items, ActionItems)

    def test_context_analysis_accepts_nested_models(
        self,
        sample_sentiment_trend_data: Dict[str, Any],
        sample_conversation_stage_data: Dict[str, Any],
        sample_action_items_data: Dict[str, Any],
        fixed_datetime: datetime,
    ) -> None:
        """Test ContextAnalysis accepts pre-created nested model instances."""
        sentiment = SentimentTrend(**sample_sentiment_trend_data)
        stage = ConversationStage(**sample_conversation_stage_data)
        items = ActionItems(**sample_action_items_data)

        analysis = ContextAnalysis(
            summary="Test summary",
            sentiment_trend=sentiment,
            conversation_stage=stage,
            action_items=items,
            last_analyzed=fixed_datetime,
        )

        assert analysis.sentiment_trend == sentiment
        assert analysis.conversation_stage == stage
        assert analysis.action_items == items

    def test_context_analysis_serializes_nested_models(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test ContextAnalysis serializes nested models correctly."""
        analysis = ContextAnalysis(**sample_context_analysis_data)
        data = analysis.model_dump()

        # Nested models should be dicts
        assert isinstance(data["sentiment_trend"], dict)
        assert isinstance(data["conversation_stage"], dict)
        assert isinstance(data["action_items"], dict)

        # Check nested values
        assert data["sentiment_trend"]["initial"] == "positive"
        assert data["conversation_stage"]["current"] == "initial_outreach"


@pytest.mark.unit
class TestContextAnalysisSerialization:
    """Test suite for ContextAnalysis serialization."""

    def test_context_analysis_to_dict(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test ContextAnalysis.model_dump() produces correct dict."""
        analysis = ContextAnalysis(**sample_context_analysis_data)
        data = analysis.model_dump()

        assert data["summary"] == sample_context_analysis_data["summary"]
        assert data["patterns_detected"] == sample_context_analysis_data["patterns_detected"]
        assert data["recommendations"] == sample_context_analysis_data["recommendations"]

    def test_context_analysis_to_json(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test ContextAnalysis.model_dump_json() produces valid JSON."""
        analysis = ContextAnalysis(**sample_context_analysis_data)
        json_str = analysis.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["summary"] == sample_context_analysis_data["summary"]

    def test_context_analysis_round_trip(self, sample_context_analysis_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = ContextAnalysis(**sample_context_analysis_data)
        json_str = original.model_dump_json()
        restored = ContextAnalysis.model_validate_json(json_str)

        assert restored.summary == original.summary
        assert restored.sentiment_trend.initial == original.sentiment_trend.initial
        assert restored.conversation_stage.current == original.conversation_stage.current
        assert restored.patterns_detected == original.patterns_detected
        assert restored.recommendations == original.recommendations


@pytest.mark.unit
class TestSentimentTrendLiteralValidation:
    """Test suite for SentimentTrend Literal type validation."""

    @pytest.mark.parametrize(
        "field,invalid_value",
        [
            ("initial", "invalid_sentiment"),
            ("initial", "happy"),
            ("initial", "POSITIVE"),
            ("current", "bad"),
            ("current", ""),
            ("direction", "up"),
            ("direction", "down"),
            ("direction", "STABLE"),
        ],
    )
    def test_invalid_literal_values_rejected(self, field: str, invalid_value: str) -> None:
        """Test that invalid Literal values are rejected."""
        valid_data = {
            "initial": "positive",
            "current": "neutral",
            "direction": "stable",
            "indicators": ["Test"],
        }
        valid_data[field] = invalid_value

        with pytest.raises(ValidationError):
            SentimentTrend(**valid_data)  # type: ignore[arg-type]


@pytest.mark.unit
class TestConversationStageLiteralValidation:
    """Test suite for ConversationStage Literal type validation."""

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "invalid_quality",
            "good",
            "bad",
            "SMOOTH",
            "",
        ],
    )
    def test_invalid_progression_quality_rejected(self, invalid_value: str) -> None:
        """Test that invalid progression_quality values are rejected."""
        with pytest.raises(ValidationError):
            ConversationStage(
                current="initial_outreach",
                progression_quality=invalid_value,  # type: ignore[arg-type]
            )

    @pytest.mark.parametrize(
        "valid_value",
        [
            "smooth",
            "stalled",
            "problematic",
            "unknown",
        ],
    )
    def test_valid_progression_quality_accepted(self, valid_value: str) -> None:
        """Test that valid progression_quality values are accepted."""
        stage = ConversationStage(
            current="initial_outreach",
            progression_quality=valid_value,  # type: ignore[arg-type]
        )
        assert stage.progression_quality == valid_value


@pytest.mark.unit
class TestSkillGapCreation:
    """Test suite for SkillGap model creation."""

    def test_skill_gap_with_all_fields(self) -> None:
        """Test creating SkillGap with all fields."""
        gap = SkillGap(
            skill="Kubernetes",
            severity="medium",
            mitigation="Can learn quickly",
        )
        assert gap.skill == "Kubernetes"
        assert gap.severity == "medium"
        assert gap.mitigation == "Can learn quickly"

    def test_skill_gap_with_minimal_fields(self) -> None:
        """Test creating SkillGap with minimal fields (no mitigation)."""
        gap = SkillGap(
            skill="Docker",
            severity="low",
        )
        assert gap.skill == "Docker"
        assert gap.severity == "low"
        assert gap.mitigation is None

    def test_skill_gap_missing_skill_raises_error(self) -> None:
        """Test missing skill field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SkillGap(severity="high")  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("skill",) for e in errors)

    def test_skill_gap_missing_severity_raises_error(self) -> None:
        """Test missing severity field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SkillGap(skill="Python")  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("severity",) for e in errors)

    @pytest.mark.parametrize(
        "severity",
        ["low", "medium", "high"],
    )
    def test_skill_gap_valid_severity_values(self, severity: str) -> None:
        """Test valid severity values are accepted."""
        gap = SkillGap(skill="Test", severity=severity)  # type: ignore[arg-type]
        assert gap.severity == severity

    @pytest.mark.parametrize(
        "invalid_severity",
        ["invalid", "critical", "LOW", "Medium", ""],
    )
    def test_skill_gap_invalid_severity_rejected(self, invalid_severity: str) -> None:
        """Test invalid severity values are rejected."""
        with pytest.raises(ValidationError):
            SkillGap(skill="Test", severity=invalid_severity)  # type: ignore[arg-type]


@pytest.mark.unit
class TestSkillGapSerialization:
    """Test suite for SkillGap serialization."""

    def test_skill_gap_to_dict(self) -> None:
        """Test SkillGap.model_dump() produces correct dict."""
        gap = SkillGap(
            skill="Kubernetes",
            severity="medium",
            mitigation="Can learn quickly",
        )
        data = gap.model_dump()

        assert data["skill"] == "Kubernetes"
        assert data["severity"] == "medium"
        assert data["mitigation"] == "Can learn quickly"

    def test_skill_gap_round_trip(self) -> None:
        """Test serialization/deserialization round trip."""
        original = SkillGap(
            skill="Docker",
            severity="low",
            mitigation="Has container experience",
        )
        json_str = original.model_dump_json()
        restored = SkillGap.model_validate_json(json_str)

        assert restored.skill == original.skill
        assert restored.severity == original.severity
        assert restored.mitigation == original.mitigation


@pytest.mark.unit
class TestFrozenValueObjects:
    """Test suite for frozen (immutable) value objects."""

    def test_sentiment_trend_is_immutable(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test SentimentTrend cannot be modified after creation."""
        trend = SentimentTrend(**sample_sentiment_trend_data)

        with pytest.raises(ValidationError) as exc_info:
            trend.current = "negative"

        assert "frozen" in str(exc_info.value).lower()

    def test_conversation_stage_is_immutable(self, sample_conversation_stage_data: Dict[str, Any]) -> None:
        """Test ConversationStage cannot be modified after creation."""
        stage = ConversationStage(**sample_conversation_stage_data)

        with pytest.raises(ValidationError) as exc_info:
            stage.current = "screening"

        assert "frozen" in str(exc_info.value).lower()

    def test_skill_gap_is_immutable(self) -> None:
        """Test SkillGap cannot be modified after creation."""
        gap = SkillGap(skill="Python", severity="low")

        with pytest.raises(ValidationError) as exc_info:
            gap.severity = "high"

        assert "frozen" in str(exc_info.value).lower()

    def test_sentiment_trend_is_hashable(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test SentimentTrend is hashable and can be used in sets/dicts."""
        trend1 = SentimentTrend(**sample_sentiment_trend_data)
        trend2 = SentimentTrend(**sample_sentiment_trend_data)

        # Should be hashable
        assert hash(trend1) is not None
        assert hash(trend2) is not None

        # Can be used in sets
        trends_set = {trend1, trend2}
        assert len(trends_set) == 1  # Same values hash to same value

        # Can be used as dict keys
        trends_dict = {trend1: "first", trend2: "second"}
        assert trends_dict[trend1] == "second"  # Second overwrites first

    def test_conversation_stage_is_hashable(self, sample_conversation_stage_data: Dict[str, Any]) -> None:
        """Test ConversationStage is hashable and can be used in sets/dicts."""
        stage1 = ConversationStage(**sample_conversation_stage_data)
        stage2 = ConversationStage(**sample_conversation_stage_data)

        # Should be hashable
        assert hash(stage1) is not None

        # Can be used in sets
        stages_set = {stage1, stage2}
        assert len(stages_set) == 1

        # Can be used as dict keys
        stages_dict = {stage1: "value"}
        assert stages_dict[stage2] == "value"

    def test_skill_gap_is_hashable(self) -> None:
        """Test SkillGap is hashable and can be used in sets/dicts."""
        gap1 = SkillGap(skill="Python", severity="low", mitigation="Learning")
        gap2 = SkillGap(skill="Python", severity="low", mitigation="Learning")
        gap3 = SkillGap(skill="Docker", severity="medium")

        # Should be hashable
        assert hash(gap1) is not None

        # Can be used in sets
        gaps_set = {gap1, gap2, gap3}
        assert len(gaps_set) == 2  # gap1 and gap2 are identical

        # Can be used as dict keys
        gaps_dict = {gap1: "first", gap3: "second"}
        assert len(gaps_dict) == 2

    def test_frozen_models_support_copy_with_modifications(self, sample_sentiment_trend_data: Dict[str, Any]) -> None:
        """Test frozen models can create modified copies using model_copy."""
        original = SentimentTrend(**sample_sentiment_trend_data)

        # Create a modified copy
        modified = original.model_copy(update={"current": "negative"})

        # Original should be unchanged
        assert original.current == sample_sentiment_trend_data["current"]
        # Modified should have new value
        assert modified.current == "negative"
        # Other fields should be the same
        assert modified.initial == original.initial
