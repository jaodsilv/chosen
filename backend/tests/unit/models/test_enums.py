"""Unit tests for Pydantic v2 enum models.

This module contains tests for:
    - Platform enum (linkedin, email, phone, in_person)
    - ProcessStatus enum (14 status values)
    - ParticipantRole enum (recruiter, candidate, hiring_manager)
"""

import pytest

from app.models.enums import ParticipantRole, Platform, ProcessStatus


@pytest.mark.unit
class TestPlatformEnum:
    """Test suite for Platform enum.

    The Platform enum defines communication channels:
        - linkedin: LinkedIn messages
        - email: Email communication
        - phone: Phone calls
        - in_person: In-person meetings
    """

    def test_platform_linkedin_value(self) -> None:
        """Test that linkedin platform has correct string value."""
        assert Platform.LINKEDIN.value == "linkedin"

    def test_platform_email_value(self) -> None:
        """Test that email platform has correct string value."""
        assert Platform.EMAIL.value == "email"

    def test_platform_phone_value(self) -> None:
        """Test that phone platform has correct string value."""
        assert Platform.PHONE.value == "phone"

    def test_platform_in_person_value(self) -> None:
        """Test that in_person platform has correct string value."""
        assert Platform.IN_PERSON.value == "in_person"

    def test_platform_all_members(self) -> None:
        """Test that Platform enum has exactly 4 members."""
        members = list(Platform)
        assert len(members) == 4
        assert set(m.value for m in members) == {
            "linkedin",
            "email",
            "phone",
            "in_person",
        }

    def test_platform_str_inheritance(self) -> None:
        """Test that Platform inherits from str."""
        assert isinstance(Platform.LINKEDIN, str)
        assert Platform.LINKEDIN == "linkedin"

    def test_platform_from_string_valid(self) -> None:
        """Test creating Platform from valid string value."""
        platform = Platform("linkedin")
        assert platform == Platform.LINKEDIN

    def test_platform_from_string_invalid(self) -> None:
        """Test creating Platform from invalid string raises ValueError."""
        with pytest.raises(ValueError):
            Platform("invalid_platform")

    def test_platform_case_sensitivity(self) -> None:
        """Test that platform values are case-sensitive."""
        with pytest.raises(ValueError):
            Platform("LINKEDIN")
        with pytest.raises(ValueError):
            Platform("LinkedIn")


@pytest.mark.unit
class TestProcessStatusEnum:
    """Test suite for ProcessStatus enum.

    The ProcessStatus enum defines 14 job application stages:
        new, reviewing, interested, not_interested, applied,
        awaiting_response, interviewing, offer, negotiating,
        accepted, declined, rejected, withdrawn, ghosted
    """

    @pytest.mark.parametrize(
        "status_name,expected_value",
        [
            ("NEW", "new"),
            ("REVIEWING", "reviewing"),
            ("INTERESTED", "interested"),
            ("NOT_INTERESTED", "not_interested"),
            ("APPLIED", "applied"),
            ("AWAITING_RESPONSE", "awaiting_response"),
            ("INTERVIEWING", "interviewing"),
            ("OFFER", "offer"),
            ("NEGOTIATING", "negotiating"),
            ("ACCEPTED", "accepted"),
            ("DECLINED", "declined"),
            ("REJECTED", "rejected"),
            ("WITHDRAWN", "withdrawn"),
            ("GHOSTED", "ghosted"),
        ],
    )
    def test_process_status_values(self, status_name: str, expected_value: str) -> None:
        """Test each ProcessStatus enum member has correct value.

        Args:
            status_name: The enum member name (e.g., "NEW").
            expected_value: The expected string value (e.g., "new").
        """
        status = getattr(ProcessStatus, status_name)
        assert status.value == expected_value

    def test_process_status_all_members_count(self) -> None:
        """Test that ProcessStatus has exactly 14 members."""
        members = list(ProcessStatus)
        assert len(members) == 14

    def test_process_status_str_inheritance(self) -> None:
        """Test that ProcessStatus inherits from str."""
        assert isinstance(ProcessStatus.NEW, str)
        assert ProcessStatus.NEW == "new"

    def test_process_status_from_string_valid(self) -> None:
        """Test creating ProcessStatus from valid string value."""
        status = ProcessStatus("interviewing")
        assert status == ProcessStatus.INTERVIEWING

    def test_process_status_from_string_invalid(self) -> None:
        """Test creating ProcessStatus from invalid string raises ValueError."""
        with pytest.raises(ValueError):
            ProcessStatus("invalid_status")

    def test_process_status_json_serialization(self) -> None:
        """Test ProcessStatus can be used as dict key and value."""
        data = {"status": ProcessStatus.OFFER}
        assert data["status"] == "offer"


@pytest.mark.unit
class TestParticipantRoleEnum:
    """Test suite for ParticipantRole enum.

    The ParticipantRole enum defines conversation participants:
        - recruiter: The recruiting person/agency
        - candidate: The job seeker (user)
        - hiring_manager: Company hiring manager
    """

    def test_participant_role_recruiter(self) -> None:
        """Test recruiter role has correct value."""
        assert ParticipantRole.RECRUITER.value == "recruiter"

    def test_participant_role_candidate(self) -> None:
        """Test candidate role has correct value."""
        assert ParticipantRole.CANDIDATE.value == "candidate"

    def test_participant_role_hiring_manager(self) -> None:
        """Test hiring_manager role has correct value."""
        assert ParticipantRole.HIRING_MANAGER.value == "hiring_manager"

    def test_participant_role_all_members(self) -> None:
        """Test ParticipantRole has exactly 3 members."""
        members = list(ParticipantRole)
        assert len(members) == 3
        assert set(m.value for m in members) == {
            "recruiter",
            "candidate",
            "hiring_manager",
        }

    def test_participant_role_str_inheritance(self) -> None:
        """Test that ParticipantRole inherits from str."""
        assert isinstance(ParticipantRole.RECRUITER, str)
        assert ParticipantRole.RECRUITER == "recruiter"

    def test_participant_role_from_string_valid(self) -> None:
        """Test creating ParticipantRole from valid string value."""
        role = ParticipantRole("candidate")
        assert role == ParticipantRole.CANDIDATE

    def test_participant_role_from_string_invalid(self) -> None:
        """Test creating ParticipantRole from invalid string raises ValueError."""
        with pytest.raises(ValueError):
            ParticipantRole("invalid_role")
