"""Unit tests for ResponseMetrics Pydantic model.

This module contains tests for ResponseMetrics:
    - recruiter_avg_hours (float, optional)
    - candidate_avg_hours (float, optional)
    - recruiter_message_count (int)
    - candidate_message_count (int)
"""

import json
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.metrics import ResponseMetrics


@pytest.mark.unit
class TestResponseMetricsCreation:
    """Test suite for ResponseMetrics model creation."""

    def test_response_metrics_with_all_fields(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test creating ResponseMetrics with all fields."""
        metrics = ResponseMetrics(**sample_response_metrics_data)

        assert (
            metrics.recruiter_avg_hours
            == sample_response_metrics_data["recruiter_avg_hours"]
        )
        assert (
            metrics.candidate_avg_hours
            == sample_response_metrics_data["candidate_avg_hours"]
        )
        assert (
            metrics.recruiter_message_count
            == sample_response_metrics_data["recruiter_message_count"]
        )
        assert (
            metrics.candidate_message_count
            == sample_response_metrics_data["candidate_message_count"]
        )

    def test_response_metrics_with_none_avg_hours(
        self, sample_response_metrics_partial_data: Dict[str, Any]
    ) -> None:
        """Test ResponseMetrics with None for avg_hours fields."""
        metrics = ResponseMetrics(**sample_response_metrics_partial_data)

        assert metrics.recruiter_avg_hours is None
        assert metrics.candidate_avg_hours == 5.5

    def test_response_metrics_minimal(self) -> None:
        """Test ResponseMetrics with default values."""
        metrics = ResponseMetrics()

        assert metrics.recruiter_avg_hours is None
        assert metrics.candidate_avg_hours is None
        assert metrics.recruiter_message_count == 0
        assert metrics.candidate_message_count == 0


@pytest.mark.unit
class TestResponseMetricsDefaults:
    """Test suite for ResponseMetrics default values."""

    def test_recruiter_avg_hours_defaults_to_none(self) -> None:
        """Test recruiter_avg_hours defaults to None."""
        metrics = ResponseMetrics()
        assert metrics.recruiter_avg_hours is None

    def test_candidate_avg_hours_defaults_to_none(self) -> None:
        """Test candidate_avg_hours defaults to None."""
        metrics = ResponseMetrics()
        assert metrics.candidate_avg_hours is None

    def test_recruiter_message_count_default(self) -> None:
        """Test recruiter_message_count defaults to 0."""
        metrics = ResponseMetrics()
        assert metrics.recruiter_message_count == 0

    def test_candidate_message_count_default(self) -> None:
        """Test candidate_message_count defaults to 0."""
        metrics = ResponseMetrics()
        assert metrics.candidate_message_count == 0


@pytest.mark.unit
class TestResponseMetricsValidation:
    """Test suite for ResponseMetrics validation."""

    def test_avg_hours_accepts_positive_float(self) -> None:
        """Test avg_hours accepts positive float values."""
        metrics = ResponseMetrics(
            recruiter_avg_hours=24.5,
            candidate_avg_hours=12.0,
        )
        assert metrics.recruiter_avg_hours == 24.5
        assert metrics.candidate_avg_hours == 12.0

    def test_avg_hours_accepts_zero(self) -> None:
        """Test avg_hours accepts zero."""
        metrics = ResponseMetrics(
            recruiter_avg_hours=0.0,
            candidate_avg_hours=0.0,
        )
        assert metrics.recruiter_avg_hours == 0.0
        assert metrics.candidate_avg_hours == 0.0

    def test_message_count_accepts_positive_int(self) -> None:
        """Test message_count accepts positive integers."""
        metrics = ResponseMetrics(
            recruiter_message_count=10,
            candidate_message_count=8,
        )
        assert metrics.recruiter_message_count == 10
        assert metrics.candidate_message_count == 8

    def test_message_count_accepts_zero(self) -> None:
        """Test message_count accepts zero."""
        metrics = ResponseMetrics(
            recruiter_message_count=0,
            candidate_message_count=0,
        )
        assert metrics.recruiter_message_count == 0
        assert metrics.candidate_message_count == 0

    def test_message_count_accepts_large_values(self) -> None:
        """Test message_count accepts large values."""
        metrics = ResponseMetrics(
            recruiter_message_count=1000,
            candidate_message_count=999,
        )
        assert metrics.recruiter_message_count == 1000
        assert metrics.candidate_message_count == 999


@pytest.mark.unit
class TestResponseMetricsSerialization:
    """Test suite for ResponseMetrics serialization."""

    def test_response_metrics_to_dict(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test ResponseMetrics.model_dump() produces correct dict."""
        metrics = ResponseMetrics(**sample_response_metrics_data)
        data = metrics.model_dump()

        assert (
            data["recruiter_avg_hours"]
            == sample_response_metrics_data["recruiter_avg_hours"]
        )
        assert (
            data["candidate_avg_hours"]
            == sample_response_metrics_data["candidate_avg_hours"]
        )
        assert (
            data["recruiter_message_count"]
            == sample_response_metrics_data["recruiter_message_count"]
        )
        assert (
            data["candidate_message_count"]
            == sample_response_metrics_data["candidate_message_count"]
        )

    def test_response_metrics_to_json(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test ResponseMetrics.model_dump_json() produces valid JSON."""
        metrics = ResponseMetrics(**sample_response_metrics_data)
        json_str = metrics.model_dump_json()

        parsed = json.loads(json_str)
        assert (
            parsed["recruiter_avg_hours"]
            == sample_response_metrics_data["recruiter_avg_hours"]
        )

    def test_response_metrics_none_values_in_json(
        self, sample_response_metrics_partial_data: Dict[str, Any]
    ) -> None:
        """Test None values serialize correctly in JSON."""
        metrics = ResponseMetrics(**sample_response_metrics_partial_data)
        json_str = metrics.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["recruiter_avg_hours"] is None
        assert parsed["candidate_avg_hours"] == 5.5

    def test_response_metrics_from_dict(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test creating ResponseMetrics from dictionary."""
        metrics = ResponseMetrics.model_validate(sample_response_metrics_data)

        assert (
            metrics.recruiter_avg_hours
            == sample_response_metrics_data["recruiter_avg_hours"]
        )

    def test_response_metrics_round_trip(
        self, sample_response_metrics_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = ResponseMetrics(**sample_response_metrics_data)
        json_str = original.model_dump_json()
        restored = ResponseMetrics.model_validate_json(json_str)

        assert restored.recruiter_avg_hours == original.recruiter_avg_hours
        assert restored.candidate_avg_hours == original.candidate_avg_hours
        assert restored.recruiter_message_count == original.recruiter_message_count
        assert restored.candidate_message_count == original.candidate_message_count


@pytest.mark.unit
class TestResponseMetricsEdgeCases:
    """Test suite for ResponseMetrics edge cases."""

    def test_metrics_with_very_large_hours(self) -> None:
        """Test metrics with very large hour values."""
        metrics = ResponseMetrics(
            recruiter_avg_hours=10000.0,
            candidate_avg_hours=5000.0,
        )
        assert metrics.recruiter_avg_hours == 10000.0

    def test_metrics_with_fractional_hours(self) -> None:
        """Test metrics with fractional hour values."""
        metrics = ResponseMetrics(
            recruiter_avg_hours=0.5,  # 30 minutes
            candidate_avg_hours=0.25,  # 15 minutes
        )
        assert metrics.recruiter_avg_hours == 0.5
        assert metrics.candidate_avg_hours == 0.25

    def test_metrics_with_high_precision_hours(self) -> None:
        """Test metrics with high precision decimal hours."""
        metrics = ResponseMetrics(
            recruiter_avg_hours=24.123456789,
            candidate_avg_hours=12.987654321,
        )
        assert abs(metrics.recruiter_avg_hours - 24.123456789) < 0.0001

    def test_metrics_asymmetric_counts(self) -> None:
        """Test metrics with very different message counts."""
        metrics = ResponseMetrics(
            recruiter_message_count=100,
            candidate_message_count=1,
        )
        assert metrics.recruiter_message_count == 100
        assert metrics.candidate_message_count == 1
