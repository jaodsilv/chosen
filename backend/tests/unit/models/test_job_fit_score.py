"""Unit tests for JobFitScore Pydantic model.

This module contains tests for JobFitScore:
    - overall_score (float, 0-100)
    - required_skills_score (float, 0-100)
    - preferred_skills_score (float, 0-100)
    - experience_match (float, 0-100)
    - strengths (List[str])
    - gaps (List[Dict[str, Any]])
    - breakdown (Dict[str, float])
"""

import json
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.analysis import JobFitScore


@pytest.mark.unit
class TestJobFitScoreCreation:
    """Test suite for JobFitScore model creation."""

    def test_job_fit_score_with_all_fields(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test creating JobFitScore with all fields."""
        score = JobFitScore(**sample_job_fit_score_data)

        assert score.overall_score == sample_job_fit_score_data["overall_score"]
        assert (
            score.required_skills_score
            == sample_job_fit_score_data["required_skills_score"]
        )
        assert (
            score.preferred_skills_score
            == sample_job_fit_score_data["preferred_skills_score"]
        )
        assert score.experience_match == sample_job_fit_score_data["experience_match"]
        assert score.strengths == sample_job_fit_score_data["strengths"]
        assert score.gaps == sample_job_fit_score_data["gaps"]
        assert score.breakdown == sample_job_fit_score_data["breakdown"]

    def test_job_fit_score_missing_overall_score_raises_error(self) -> None:
        """Test missing overall_score raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            JobFitScore(
                required_skills_score=90.0,
                preferred_skills_score=75.0,
                experience_match=85.0,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("overall_score",) for e in errors)

    def test_job_fit_score_missing_required_skills_score_raises_error(self) -> None:
        """Test missing required_skills_score raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            JobFitScore(
                overall_score=85.0,
                preferred_skills_score=75.0,
                experience_match=85.0,
            )
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("required_skills_score",) for e in errors)

    def test_job_fit_score_with_minimal_required_fields(self) -> None:
        """Test JobFitScore with only required fields."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
        )
        assert score.overall_score == 85.0
        assert score.strengths == []
        assert score.gaps == []
        assert score.breakdown == {}


@pytest.mark.unit
class TestJobFitScoreRangeValidation:
    """Test suite for JobFitScore range validation (0-100)."""

    @pytest.mark.parametrize(
        "field,value",
        [
            ("overall_score", 0.0),
            ("overall_score", 50.0),
            ("overall_score", 100.0),
            ("required_skills_score", 0.0),
            ("required_skills_score", 100.0),
            ("preferred_skills_score", 0.0),
            ("preferred_skills_score", 100.0),
            ("experience_match", 0.0),
            ("experience_match", 100.0),
        ],
    )
    def test_score_accepts_valid_range(
        self, sample_job_fit_score_data: Dict[str, Any], field: str, value: float
    ) -> None:
        """Test score fields accept values in 0-100 range."""
        data = sample_job_fit_score_data.copy()
        data[field] = value
        score = JobFitScore(**data)
        assert getattr(score, field) == value

    @pytest.mark.parametrize(
        "field,invalid_value",
        [
            ("overall_score", -1.0),
            ("overall_score", 101.0),
            ("overall_score", 150.0),
            ("required_skills_score", -10.0),
            ("required_skills_score", 200.0),
            ("preferred_skills_score", -0.1),
            ("experience_match", 100.1),
        ],
    )
    def test_score_rejects_out_of_range(
        self,
        sample_job_fit_score_data: Dict[str, Any],
        field: str,
        invalid_value: float,
    ) -> None:
        """Test score fields reject values outside 0-100 range."""
        data = sample_job_fit_score_data.copy()
        data[field] = invalid_value
        with pytest.raises(ValidationError):
            JobFitScore(**data)

    def test_invalid_score_data_fixture(
        self, invalid_score_data: Dict[str, Any]
    ) -> None:
        """Test that invalid_score_data fixture is rejected."""
        with pytest.raises(ValidationError):
            JobFitScore(**invalid_score_data)


@pytest.mark.unit
class TestJobFitScoreDefaults:
    """Test suite for JobFitScore default values."""

    def test_strengths_defaults_to_empty_list(self) -> None:
        """Test strengths defaults to empty list."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
        )
        assert score.strengths == []

    def test_gaps_defaults_to_empty_list(self) -> None:
        """Test gaps defaults to empty list."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
        )
        assert score.gaps == []

    def test_breakdown_defaults_to_empty_dict(self) -> None:
        """Test breakdown defaults to empty dict."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
        )
        assert score.breakdown == {}


@pytest.mark.unit
class TestJobFitScoreGapsStructure:
    """Test suite for JobFitScore gaps field structure."""

    def test_gaps_accepts_valid_dict_structure(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test gaps accepts list of dicts with skill/severity/mitigation."""
        score = JobFitScore(**sample_job_fit_score_data)
        assert len(score.gaps) == 1
        assert score.gaps[0]["skill"] == "Kubernetes"
        assert score.gaps[0]["severity"] == "medium"
        assert "mitigation" in score.gaps[0]

    def test_gaps_with_multiple_entries(self) -> None:
        """Test gaps with multiple gap entries."""
        score = JobFitScore(
            overall_score=70.0,
            required_skills_score=60.0,
            preferred_skills_score=50.0,
            experience_match=75.0,
            gaps=[
                {"skill": "Kubernetes", "severity": "high"},
                {"skill": "GraphQL", "severity": "medium"},
                {"skill": "Terraform", "severity": "low"},
            ],
        )
        assert len(score.gaps) == 3

    def test_gaps_with_empty_list(self) -> None:
        """Test gaps with empty list."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
            gaps=[],
        )
        assert score.gaps == []

    def test_gaps_serialization(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test gaps serializes correctly to JSON/dict."""
        score = JobFitScore(**sample_job_fit_score_data)
        data = score.model_dump()

        assert isinstance(data["gaps"], list)
        assert len(data["gaps"]) == 1
        assert data["gaps"][0]["skill"] == "Kubernetes"


@pytest.mark.unit
class TestJobFitScoreBreakdown:
    """Test suite for JobFitScore breakdown field."""

    def test_breakdown_accepts_dict_with_float_values(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test breakdown accepts dict with float values."""
        score = JobFitScore(**sample_job_fit_score_data)

        assert score.breakdown["technical_skills"] == 88.0
        assert score.breakdown["experience_level"] == 92.0
        assert score.breakdown["domain_knowledge"] == 75.0

    def test_breakdown_with_various_categories(self) -> None:
        """Test breakdown with various category keys."""
        score = JobFitScore(
            overall_score=80.0,
            required_skills_score=85.0,
            preferred_skills_score=70.0,
            experience_match=80.0,
            breakdown={
                "python": 95.0,
                "fastapi": 90.0,
                "postgresql": 70.0,
                "leadership": 85.0,
            },
        )
        assert len(score.breakdown) == 4
        assert score.breakdown["python"] == 95.0

    def test_breakdown_empty_dict(self) -> None:
        """Test breakdown with empty dict."""
        score = JobFitScore(
            overall_score=85.0,
            required_skills_score=90.0,
            preferred_skills_score=75.0,
            experience_match=85.0,
            breakdown={},
        )
        assert score.breakdown == {}


@pytest.mark.unit
class TestJobFitScoreSerialization:
    """Test suite for JobFitScore serialization."""

    def test_job_fit_score_to_dict(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test JobFitScore.model_dump() produces correct dict."""
        score = JobFitScore(**sample_job_fit_score_data)
        data = score.model_dump()

        assert data["overall_score"] == sample_job_fit_score_data["overall_score"]
        assert data["strengths"] == sample_job_fit_score_data["strengths"]
        assert data["gaps"] == sample_job_fit_score_data["gaps"]
        assert data["breakdown"] == sample_job_fit_score_data["breakdown"]

    def test_job_fit_score_to_json(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test JobFitScore.model_dump_json() produces valid JSON."""
        score = JobFitScore(**sample_job_fit_score_data)
        json_str = score.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["overall_score"] == sample_job_fit_score_data["overall_score"]

    def test_job_fit_score_from_dict(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test creating JobFitScore from dictionary."""
        score = JobFitScore.model_validate(sample_job_fit_score_data)

        assert score.overall_score == sample_job_fit_score_data["overall_score"]

    def test_job_fit_score_round_trip(
        self, sample_job_fit_score_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = JobFitScore(**sample_job_fit_score_data)
        json_str = original.model_dump_json()
        restored = JobFitScore.model_validate_json(json_str)

        assert restored.overall_score == original.overall_score
        assert restored.required_skills_score == original.required_skills_score
        assert restored.preferred_skills_score == original.preferred_skills_score
        assert restored.experience_match == original.experience_match
        assert restored.strengths == original.strengths
        assert restored.gaps == original.gaps
        assert restored.breakdown == original.breakdown


@pytest.mark.unit
class TestJobFitScoreEdgeCases:
    """Test suite for JobFitScore edge cases."""

    def test_score_boundary_zero(self) -> None:
        """Test all scores at zero boundary."""
        score = JobFitScore(
            overall_score=0.0,
            required_skills_score=0.0,
            preferred_skills_score=0.0,
            experience_match=0.0,
        )
        assert score.overall_score == 0.0
        assert score.required_skills_score == 0.0

    def test_score_boundary_hundred(self) -> None:
        """Test all scores at 100 boundary."""
        score = JobFitScore(
            overall_score=100.0,
            required_skills_score=100.0,
            preferred_skills_score=100.0,
            experience_match=100.0,
        )
        assert score.overall_score == 100.0
        assert score.required_skills_score == 100.0

    def test_score_with_integer_values(self) -> None:
        """Test scores with integer values (should be coerced to float)."""
        score = JobFitScore(
            overall_score=85,  # type: ignore
            required_skills_score=90,  # type: ignore
            preferred_skills_score=75,  # type: ignore
            experience_match=85,  # type: ignore
        )
        assert score.overall_score == 85.0
        assert isinstance(score.overall_score, float)

    def test_score_with_decimal_precision(self) -> None:
        """Test scores with high decimal precision."""
        score = JobFitScore(
            overall_score=85.123456789,
            required_skills_score=90.5,
            preferred_skills_score=75.25,
            experience_match=85.75,
        )
        assert abs(score.overall_score - 85.123456789) < 0.0001
