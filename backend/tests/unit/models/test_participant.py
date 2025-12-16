"""Unit tests for Participant Pydantic model.

This module contains tests for the Participant model:
    - name (str, required)
    - role (ParticipantRole, required)
    - email (str, optional)
    - company (str, optional)
"""

import json
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.enums import ParticipantRole
from app.models.participant import Participant


@pytest.mark.unit
class TestParticipantCreation:
    """Test suite for Participant model creation."""

    def test_participant_with_all_fields(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test creating Participant with all fields."""
        participant = Participant(**sample_participant_data)

        assert participant.name == sample_participant_data["name"]
        assert participant.role == ParticipantRole.RECRUITER
        assert participant.email == sample_participant_data["email"]
        assert participant.company == sample_participant_data["company"]

    def test_participant_with_required_fields_only(self, sample_participant_minimal_data: Dict[str, Any]) -> None:
        """Test creating Participant with only required fields."""
        participant = Participant(**sample_participant_minimal_data)

        assert participant.name == sample_participant_minimal_data["name"]
        assert participant.role == ParticipantRole.CANDIDATE
        assert participant.email is None
        assert participant.company is None

    def test_participant_missing_name_raises_error(self) -> None:
        """Test missing name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Participant(role=ParticipantRole.RECRUITER)  # type: ignore[call-arg]

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("name",) for e in errors)

    def test_participant_missing_role_raises_error(self) -> None:
        """Test missing role raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Participant(name="John Doe")  # type: ignore[call-arg]

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("role",) for e in errors)


@pytest.mark.unit
class TestParticipantRoleValidation:
    """Test suite for Participant role field validation."""

    @pytest.mark.parametrize(
        "role",
        [
            ParticipantRole.RECRUITER,
            ParticipantRole.CANDIDATE,
            ParticipantRole.HIRING_MANAGER,
        ],
    )
    def test_participant_accepts_valid_role_string(self, role: ParticipantRole) -> None:
        """Test Participant accepts valid role values."""
        participant = Participant(name="Test Person", role=role)
        assert participant.role == role

    def test_participant_accepts_role_enum(self) -> None:
        """Test Participant accepts ParticipantRole enum directly."""
        participant = Participant(name="Test Person", role=ParticipantRole.HIRING_MANAGER)
        assert participant.role == "hiring_manager"

    def test_participant_rejects_invalid_role(self) -> None:
        """Test Participant rejects invalid role value."""
        with pytest.raises(ValidationError) as exc_info:
            Participant(
                name="Test Person",
                role="invalid_role",  # type: ignore[arg-type]
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("role",) for e in errors)


@pytest.mark.unit
class TestParticipantDefaults:
    """Test suite for Participant default values."""

    def test_email_defaults_to_none(self, sample_participant_minimal_data: Dict[str, Any]) -> None:
        """Test email defaults to None."""
        participant = Participant(**sample_participant_minimal_data)
        assert participant.email is None

    def test_company_defaults_to_none(self, sample_participant_minimal_data: Dict[str, Any]) -> None:
        """Test company defaults to None."""
        participant = Participant(**sample_participant_minimal_data)
        assert participant.company is None


@pytest.mark.unit
class TestParticipantSerialization:
    """Test suite for Participant serialization."""

    def test_participant_to_dict(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test Participant.model_dump() produces correct dict."""
        participant = Participant(**sample_participant_data)
        data = participant.model_dump()

        assert data["name"] == sample_participant_data["name"]
        assert data["email"] == sample_participant_data["email"]
        assert data["company"] == sample_participant_data["company"]

    def test_participant_role_serializes_as_string(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test role serializes as string value not enum name."""
        participant = Participant(**sample_participant_data)
        data = participant.model_dump()

        # Should be the string value, not enum
        assert data["role"] == "recruiter"

    def test_participant_to_json(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test Participant.model_dump_json() produces valid JSON."""
        participant = Participant(**sample_participant_data)
        json_str = participant.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["name"] == sample_participant_data["name"]
        assert parsed["role"] == "recruiter"

    def test_participant_from_dict(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test creating Participant from dictionary."""
        participant = Participant.model_validate(sample_participant_data)

        assert participant.name == sample_participant_data["name"]
        assert participant.role == ParticipantRole.RECRUITER

    def test_participant_round_trip(self, sample_participant_data: Dict[str, Any]) -> None:
        """Test serialization/deserialization round trip."""
        original = Participant(**sample_participant_data)
        json_str = original.model_dump_json()
        restored = Participant.model_validate_json(json_str)

        assert restored.name == original.name
        assert restored.role == original.role
        assert restored.email == original.email
        assert restored.company == original.company


@pytest.mark.unit
class TestParticipantEdgeCases:
    """Test suite for Participant edge cases."""

    def test_participant_with_unicode_name(self) -> None:
        """Test Participant with unicode characters in name."""
        participant = Participant(
            name="田中太郎",
            role=ParticipantRole.RECRUITER,
        )
        assert participant.name == "田中太郎"

    def test_participant_with_long_email(self) -> None:
        """Test Participant with long email address."""
        long_email = "very.long.email.address" + ".subdomain" * 10 + "@company.com"
        participant = Participant(
            name="Test",
            role=ParticipantRole.RECRUITER,
            email=long_email,
        )
        assert participant.email == long_email

    def test_participant_with_special_chars_in_company(self) -> None:
        """Test Participant with special characters in company name."""
        participant = Participant(
            name="Test",
            role=ParticipantRole.RECRUITER,
            company="Company & Co. (Inc.) - Division #1",
        )
        assert participant.company is not None
        assert "&" in participant.company
        assert "#" in participant.company


@pytest.mark.unit
class TestParticipantEmailValidation:
    """Test suite for Participant email validation."""

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "not-an-email",
            "@missing-local.com",
            "missing-at-sign.com",
            "missing.domain@",
            "spaces in@email.com",
            "user@.com",
        ],
    )
    def test_invalid_email_rejected(self, invalid_email: str) -> None:
        """Test that invalid email addresses are rejected."""
        with pytest.raises(ValidationError):
            Participant(
                name="Test",
                role=ParticipantRole.RECRUITER,
                email=invalid_email,
            )

    @pytest.mark.parametrize(
        "valid_email",
        [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.com",
            "user@subdomain.example.com",
        ],
    )
    def test_valid_email_accepted(self, valid_email: str) -> None:
        """Test that valid email addresses are accepted."""
        participant = Participant(
            name="Test",
            role=ParticipantRole.RECRUITER,
            email=valid_email,
        )
        assert participant.email == valid_email

    def test_none_email_accepted(self) -> None:
        """Test that None email is accepted (optional field)."""
        participant = Participant(
            name="Test",
            role=ParticipantRole.RECRUITER,
            email=None,
        )
        assert participant.email is None


@pytest.mark.unit
class TestParticipantFrozen:
    """Test suite for Participant frozen (immutable) behavior."""

    def test_participant_is_immutable(
        self, sample_participant_data: Dict[str, Any]
    ) -> None:
        """Test Participant cannot be modified after creation."""
        participant = Participant(**sample_participant_data)

        with pytest.raises(ValidationError) as exc_info:
            participant.name = "New Name"  # type: ignore[misc]

        assert "frozen" in str(exc_info.value).lower()

    def test_participant_role_is_immutable(
        self, sample_participant_data: Dict[str, Any]
    ) -> None:
        """Test Participant role cannot be modified after creation."""
        participant = Participant(**sample_participant_data)

        with pytest.raises(ValidationError) as exc_info:
            participant.role = ParticipantRole.CANDIDATE  # type: ignore[misc]

        assert "frozen" in str(exc_info.value).lower()

    def test_participant_is_hashable(
        self, sample_participant_data: Dict[str, Any]
    ) -> None:
        """Test Participant is hashable and can be used in sets/dicts."""
        participant1 = Participant(**sample_participant_data)
        participant2 = Participant(**sample_participant_data)

        # Should be hashable
        assert hash(participant1) is not None
        assert hash(participant2) is not None

        # Can be used in sets
        participants_set = {participant1, participant2}
        assert len(participants_set) == 1  # Same values hash to same value

        # Can be used as dict keys
        participants_dict = {participant1: "first", participant2: "second"}
        assert participants_dict[participant1] == "second"

    def test_participant_different_values_hash_differently(self) -> None:
        """Test different Participant instances have different hashes."""
        participant1 = Participant(name="John", role=ParticipantRole.RECRUITER)
        participant2 = Participant(name="Jane", role=ParticipantRole.CANDIDATE)

        # Different values should have different hashes (usually)
        participants_set = {participant1, participant2}
        assert len(participants_set) == 2

    def test_participant_supports_copy_with_modifications(
        self, sample_participant_data: Dict[str, Any]
    ) -> None:
        """Test Participant can create modified copies using model_copy."""
        original = Participant(**sample_participant_data)

        # Create a modified copy
        modified = original.model_copy(update={"name": "New Name"})

        # Original should be unchanged
        assert original.name == sample_participant_data["name"]
        # Modified should have new value
        assert modified.name == "New Name"
        # Other fields should be the same
        assert modified.role == original.role
        assert modified.email == original.email
