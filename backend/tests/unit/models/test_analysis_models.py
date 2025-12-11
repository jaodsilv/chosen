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
)


@pytest.mark.unit
class TestSentimentTrendCreation:
    """Test suite for SentimentTrend model."""

    def test_sentiment_trend_with_all_fields(
        self, sample_sentiment_trend_data: Dict[str, Any]
    ) -> None:
        """Test creating SentimentTrend with all fields."""
        trend = SentimentTrend(**sample_sentiment_trend_data)

        assert trend.initial == sample_sentiment_trend_data["initial"]
        assert trend.current == sample_sentiment_trend_data["current"]
        assert trend.direction == sample_sentiment_trend_data["direction"]
        assert trend.indicators == sample_sentiment_trend_data["indicators"]

    def test_sentiment_trend_missing_initial_raises_error(self) -> None:
        """Test missing initial field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(
                current="positive",
                direction="stable",
                indicators=["Test"],
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("initial",) for e in errors)

    def test_sentiment_trend_missing_current_raises_error(self) -> None:
        """Test missing current field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(
                initial="positive",
                direction="stable",
                indicators=["Test"],
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("current",) for e in errors)

    def test_sentiment_trend_missing_direction_raises_error(self) -> None:
        """Test missing direction field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(
                initial="positive",
                current="positive",
                indicators=["Test"],
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("direction",) for e in errors)

    def test_sentiment_trend_missing_indicators_raises_error(self) -> None:
        """Test missing indicators field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            SentimentTrend(
                initial="positive",
                current="positive",
                direction="stable",
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("indicators",) for e in errors)

    def test_sentiment_trend_with_empty_indicators(self) -> None:
        """Test SentimentTrend with empty indicators list."""
        trend = SentimentTrend(
            initial="positive",
            current="positive",
            direction="stable",
            indicators=[],
        )
        assert trend.indicators == []

    @pytest.mark.parametrize(
        "initial,current,direction",
        [
            ("positive", "positive", "stable"),
            ("neutral", "positive", "improving"),
            ("positive", "negative", "declining"),
            ("negative", "neutral", "improving"),
        ],
    )
    def test_sentiment_trend_various_combinations(
        self, initial: str, current: str, direction: str
    ) -> None:
        """Test various sentiment combinations."""
        trend = SentimentTrend(
            initial=initial,
            current=current,
            direction=direction,
            indicators=["Test indicator"],
        )
        assert trend.initial == initial
        assert trend.current == current
        assert trend.direction == direction


@pytest.mark.unit
class TestSentimentTrendSerialization:
    """Test suite for SentimentTrend serialization."""

    def test_sentiment_trend_to_dict(
        self, sample_sentiment_trend_data: Dict[str, Any]
    ) -> None:
        """Test SentimentTrend.model_dump() produces correct dict."""
        trend = SentimentTrend(**sample_sentiment_trend_data)
        data = trend.model_dump()

        assert data["initial"] == sample_sentiment_trend_data["initial"]
        assert data["current"] == sample_sentiment_trend_data["current"]
        assert data["direction"] == sample_sentiment_trend_data["direction"]
        assert data["indicators"] == sample_sentiment_trend_data["indicators"]

    def test_sentiment_trend_round_trip(
        self, sample_sentiment_trend_data: Dict[str, Any]
    ) -> None:
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

    def test_conversation_stage_with_all_fields(
        self, sample_conversation_stage_data: Dict[str, Any]
    ) -> None:
        """Test creating ConversationStage with all fields."""
        stage = ConversationStage(**sample_conversation_stage_data)

        assert stage.current == sample_conversation_stage_data["current"]
        assert (
            stage.progression_quality
            == sample_conversation_stage_data["progression_quality"]
        )

    def test_conversation_stage_missing_current_raises_error(self) -> None:
        """Test missing current field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConversationStage(progression_quality="smooth")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("current",) for e in errors)

    def test_conversation_stage_missing_progression_quality_raises_error(self) -> None:
        """Test missing progression_quality raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ConversationStage(current="initial_outreach")
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

    def test_conversation_stage_to_dict(
        self, sample_conversation_stage_data: Dict[str, Any]
    ) -> None:
        """Test ConversationStage.model_dump() produces correct dict."""
        stage = ConversationStage(**sample_conversation_stage_data)
        data = stage.model_dump()

        assert data["current"] == sample_conversation_stage_data["current"]
        assert (
            data["progression_quality"]
            == sample_conversation_stage_data["progression_quality"]
        )

    def test_conversation_stage_round_trip(
        self, sample_conversation_stage_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = ConversationStage(**sample_conversation_stage_data)
        json_str = original.model_dump_json()
        restored = ConversationStage.model_validate_json(json_str)

        assert restored.current == original.current
        assert restored.progression_quality == original.progression_quality


@pytest.mark.unit
class TestActionItemsCreation:
    """Test suite for ActionItems model."""

    def test_action_items_with_all_fields(
        self, sample_action_items_data: Dict[str, Any]
    ) -> None:
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

    def test_action_items_to_dict(
        self, sample_action_items_data: Dict[str, Any]
    ) -> None:
        """Test ActionItems.model_dump() produces correct dict."""
        items = ActionItems(**sample_action_items_data)
        data = items.model_dump()

        assert (
            data["candidate_pending"] == sample_action_items_data["candidate_pending"]
        )
        assert (
            data["recruiter_pending"] == sample_action_items_data["recruiter_pending"]
        )

    def test_action_items_round_trip(
        self, sample_action_items_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = ActionItems(**sample_action_items_data)
        json_str = original.model_dump_json()
        restored = ActionItems.model_validate_json(json_str)

        assert restored.candidate_pending == original.candidate_pending
        assert restored.recruiter_pending == original.recruiter_pending


@pytest.mark.unit
class TestContextAnalysisCreation:
    """Test suite for ContextAnalysis model."""

    def test_context_analysis_with_all_fields(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
        """Test creating ContextAnalysis with all fields."""
        analysis = ContextAnalysis(**sample_context_analysis_data)

        assert analysis.summary == sample_context_analysis_data["summary"]
        assert (
            analysis.patterns_detected
            == sample_context_analysis_data["patterns_detected"]
        )
        assert (
            analysis.recommendations == sample_context_analysis_data["recommendations"]
        )
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
            ContextAnalysis(
                sentiment_trend=sample_sentiment_trend_data,
                conversation_stage=sample_conversation_stage_data,
                action_items=sample_action_items_data,
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
            ContextAnalysis(
                summary="Test summary",
                conversation_stage=sample_conversation_stage_data,
                action_items=sample_action_items_data,
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
            ContextAnalysis(
                summary="Test summary",
                sentiment_trend=sample_sentiment_trend_data,
                conversation_stage=sample_conversation_stage_data,
                action_items=sample_action_items_data,
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
            sentiment_trend=sample_sentiment_trend_data,
            conversation_stage=sample_conversation_stage_data,
            action_items=sample_action_items_data,
            last_analyzed=fixed_datetime,
        )
        assert analysis.patterns_detected == []
        assert analysis.recommendations == []


@pytest.mark.unit
class TestContextAnalysisNested:
    """Test suite for ContextAnalysis nested model handling."""

    def test_context_analysis_accepts_nested_dicts(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
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

    def test_context_analysis_serializes_nested_models(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
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

    def test_context_analysis_to_dict(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
        """Test ContextAnalysis.model_dump() produces correct dict."""
        analysis = ContextAnalysis(**sample_context_analysis_data)
        data = analysis.model_dump()

        assert data["summary"] == sample_context_analysis_data["summary"]
        assert (
            data["patterns_detected"]
            == sample_context_analysis_data["patterns_detected"]
        )
        assert (
            data["recommendations"] == sample_context_analysis_data["recommendations"]
        )

    def test_context_analysis_to_json(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
        """Test ContextAnalysis.model_dump_json() produces valid JSON."""
        analysis = ContextAnalysis(**sample_context_analysis_data)
        json_str = analysis.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["summary"] == sample_context_analysis_data["summary"]

    def test_context_analysis_round_trip(
        self, sample_context_analysis_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = ContextAnalysis(**sample_context_analysis_data)
        json_str = original.model_dump_json()
        restored = ContextAnalysis.model_validate_json(json_str)

        assert restored.summary == original.summary
        assert restored.sentiment_trend.initial == original.sentiment_trend.initial
        assert (
            restored.conversation_stage.current == original.conversation_stage.current
        )
        assert restored.patterns_detected == original.patterns_detected
        assert restored.recommendations == original.recommendations
