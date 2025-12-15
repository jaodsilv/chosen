"""Tests for path validation security in models.

These tests verify that file path fields are restricted to the configured
data directory to prevent path traversal attacks.
"""

import os
import tempfile
from typing import Any, Dict
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.settings import UserSettings


class TestPathTraversalPrevention:
    """Test that path traversal patterns are rejected."""

    @pytest.fixture
    def temp_data_dir(self) -> str:
        """Create a temporary data directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def mock_settings(self, temp_data_dir: str) -> Any:
        """Mock get_settings to use temporary data directory."""

        class MockSettings:
            data_dir = temp_data_dir

        with patch("app.models.validators.get_settings", return_value=MockSettings()):
            yield MockSettings()

    @pytest.mark.parametrize(
        "unsafe_path",
        [
            "../etc/passwd",
            "..\\windows\\system32",
            "data/../../../etc/passwd",
            "./../secret.txt",
            "subdir/../../outside.txt",
            "..\\..\\..\\sensitive.txt",
        ],
    )
    def test_resume_path_rejects_traversal(
        self, mock_settings: Any, unsafe_path: str
    ) -> None:
        """UserSettings.resume_path rejects path traversal patterns."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_name="test",
                user_email="test@example.com",
                default_model="sonnet",
                resume_path=unsafe_path,
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    @pytest.mark.parametrize(
        "unsafe_path",
        [
            "/etc/passwd",
            "/home/user/documents/file.txt",
            "/var/log/secret.log",
        ],
    )
    @pytest.mark.skipif(os.name == "nt", reason="Unix absolute paths on Unix only")
    def test_resume_path_rejects_unix_absolute_paths(
        self, mock_settings: Any, unsafe_path: str
    ) -> None:
        """UserSettings.resume_path rejects absolute Unix paths outside data dir."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_name="test",
                user_email="test@example.com",
                default_model="sonnet",
                resume_path=unsafe_path,
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    @pytest.mark.parametrize(
        "unsafe_path",
        [
            "C:\\Windows\\system32\\config",
            "D:\\secret\\file.txt",
            "E:\\Users\\admin\\passwords.txt",
        ],
    )
    @pytest.mark.skipif(os.name != "nt", reason="Windows paths on Windows only")
    def test_resume_path_rejects_windows_absolute_paths(
        self, mock_settings: Any, unsafe_path: str
    ) -> None:
        """UserSettings.resume_path rejects absolute Windows paths outside data dir."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_name="test",
                user_email="test@example.com",
                default_model="sonnet",
                resume_path=unsafe_path,
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    @pytest.mark.parametrize(
        "safe_path",
        [
            "resume.pdf",
            "documents/resume.pdf",
            "./resume.pdf",
            "subdirectory/file.txt",
            "a/b/c/deeply/nested/file.txt",
        ],
    )
    def test_resume_path_accepts_safe_relative_paths(
        self, mock_settings: Any, safe_path: str
    ) -> None:
        """UserSettings.resume_path accepts relative paths within data dir."""
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path=safe_path,
        )
        assert settings.resume_path == safe_path

    def test_resume_path_accepts_none(self, mock_settings: Any) -> None:
        """UserSettings.resume_path accepts None value."""
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path=None,
        )
        assert settings.resume_path is None


class TestConversationPathValidation:
    """Test path validation for Conversation filepath fields."""

    @pytest.fixture
    def temp_data_dir(self) -> str:
        """Create a temporary data directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def mock_settings(self, temp_data_dir: str) -> Any:
        """Mock get_settings to use temporary data directory."""

        class MockSettings:
            data_dir = temp_data_dir

        with patch("app.models.validators.get_settings", return_value=MockSettings()):
            yield MockSettings()

    @pytest.mark.parametrize(
        "unsafe_path",
        [
            "../etc/passwd",
            "..\\windows\\system32",
            "data/../../../secret.txt",
        ],
    )
    def test_job_description_filepath_rejects_traversal(
        self, mock_settings: Any, unsafe_path: str
    ) -> None:
        """Conversation.job_description_filepath rejects path traversal."""
        with pytest.raises(ValidationError) as exc_info:
            Conversation(
                platform="linkedin",
                recruiter_name="Test Recruiter",
                job_description_filepath=unsafe_path,
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    @pytest.mark.parametrize(
        "unsafe_path",
        [
            "../etc/passwd",
            "..\\windows\\system32",
            "data/../../../secret.txt",
        ],
    )
    def test_resume_filepath_rejects_traversal(
        self, mock_settings: Any, unsafe_path: str
    ) -> None:
        """Conversation.resume_filepath rejects path traversal."""
        with pytest.raises(ValidationError) as exc_info:
            Conversation(
                platform="linkedin",
                recruiter_name="Test Recruiter",
                resume_filepath=unsafe_path,
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    def test_filepath_accepts_safe_paths(self, mock_settings: Any) -> None:
        """Conversation filepath fields accept safe relative paths."""
        conversation = Conversation(
            platform="linkedin",
            recruiter_name="Test Recruiter",
            job_description_filepath="jobs/description.md",
            resume_filepath="resumes/my_resume.pdf",
        )
        assert conversation.job_description_filepath == "jobs/description.md"
        assert conversation.resume_filepath == "resumes/my_resume.pdf"

    def test_filepath_accepts_none(self, mock_settings: Any) -> None:
        """Conversation filepath fields accept None values."""
        conversation = Conversation(
            platform="linkedin",
            recruiter_name="Test Recruiter",
            job_description_filepath=None,
            resume_filepath=None,
        )
        assert conversation.job_description_filepath is None
        assert conversation.resume_filepath is None


class TestMessageAttachmentsValidation:
    """Test path validation for Message.attachments field."""

    @pytest.fixture
    def temp_data_dir(self) -> str:
        """Create a temporary data directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def mock_settings(self, temp_data_dir: str) -> Any:
        """Mock get_settings to use temporary data directory."""

        class MockSettings:
            data_dir = temp_data_dir

        with patch("app.models.validators.get_settings", return_value=MockSettings()):
            yield MockSettings()

    @pytest.fixture
    def fixed_datetime(self) -> Any:
        """Provide fixed datetime for message creation."""
        from datetime import datetime, timezone

        return datetime(2025, 12, 9, 10, 0, 0, tzinfo=timezone.utc)

    def test_attachments_rejects_traversal_in_any_item(
        self, mock_settings: Any, fixed_datetime: Any
    ) -> None:
        """Message.attachments rejects any item with path traversal."""
        with pytest.raises(ValidationError) as exc_info:
            Message(
                timestamp=fixed_datetime,
                from_name="Recruiter",
                body="Test message",
                attachments=[
                    "safe_file.pdf",
                    "../../../etc/passwd",  # Unsafe path
                    "another_safe.txt",
                ],
            )
        assert "outside allowed directory" in str(exc_info.value).lower()

    def test_attachments_accepts_safe_paths(
        self, mock_settings: Any, fixed_datetime: Any
    ) -> None:
        """Message.attachments accepts list of safe relative paths."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body="Test message",
            attachments=[
                "job_description.pdf",
                "company_info.docx",
                "documents/org_chart.png",
            ],
        )
        assert len(message.attachments) == 3
        assert message.attachments[0] == "job_description.pdf"

    def test_attachments_accepts_empty_list(
        self, mock_settings: Any, fixed_datetime: Any
    ) -> None:
        """Message.attachments accepts empty list."""
        message = Message(
            timestamp=fixed_datetime,
            from_name="Recruiter",
            body="Test message",
            attachments=[],
        )
        assert message.attachments == []


class TestPathValidationEdgeCases:
    """Test edge cases in path validation."""

    @pytest.fixture
    def temp_data_dir(self) -> str:
        """Create a temporary data directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def mock_settings(self, temp_data_dir: str) -> Any:
        """Mock get_settings to use temporary data directory."""

        class MockSettings:
            data_dir = temp_data_dir

        with patch("app.models.validators.get_settings", return_value=MockSettings()):
            yield MockSettings()

    @pytest.mark.parametrize(
        "encoded_traversal",
        [
            "..%2F..%2Fetc%2Fpasswd",  # URL encoded
            "..%5C..%5Cwindows",  # URL encoded backslash
        ],
    )
    def test_resume_path_with_encoded_traversal(
        self, mock_settings: Any, encoded_traversal: str
    ) -> None:
        """UserSettings.resume_path handles URL-encoded paths.

        Note: These should be handled at the API layer, but the model
        should still validate the literal string. Since '..' is not present
        as a literal substring, these may pass model validation but should
        be caught by URL decoding at the API layer.
        """
        # These don't contain literal '..' so they pass validation
        # but resolve to safe paths since %2F is not a real path separator
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path=encoded_traversal,
        )
        assert settings.resume_path == encoded_traversal

    def test_resume_path_with_symlink_in_name(self, mock_settings: Any) -> None:
        """UserSettings.resume_path accepts files that look like symlinks."""
        # This is just a filename, not an actual symlink traversal
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path="symlink_to_resume.pdf",
        )
        assert settings.resume_path == "symlink_to_resume.pdf"

    def test_resume_path_with_dots_in_filename(self, mock_settings: Any) -> None:
        """UserSettings.resume_path accepts filenames with dots."""
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path="resume.v2.final.2025.pdf",
        )
        assert settings.resume_path == "resume.v2.final.2025.pdf"

    def test_resume_path_single_dot_directory(self, mock_settings: Any) -> None:
        """UserSettings.resume_path accepts paths with single dot (current dir)."""
        settings = UserSettings(
            user_name="test",
            user_email="test@example.com",
            default_model="sonnet",
            resume_path="./resume.pdf",
        )
        assert settings.resume_path == "./resume.pdf"
