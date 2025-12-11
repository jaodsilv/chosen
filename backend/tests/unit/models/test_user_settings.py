"""Unit tests for UserSettings Pydantic model.

This module contains tests for UserSettings:
    - user_name (str)
    - user_email (str)
    - default_model (str)
    - resume_path (str, optional)
    - preferences (dict)
"""

import json
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.models.settings import UserSettings


@pytest.mark.unit
class TestUserSettingsCreation:
    """Test suite for UserSettings model creation."""

    def test_user_settings_with_all_fields(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test creating UserSettings with all fields."""
        settings = UserSettings(**sample_user_settings_data)

        assert settings.user_name == sample_user_settings_data["user_name"]
        assert settings.user_email == sample_user_settings_data["user_email"]
        assert settings.default_model == sample_user_settings_data["default_model"]
        assert settings.resume_path == sample_user_settings_data["resume_path"]
        assert settings.preferences == sample_user_settings_data["preferences"]

    def test_user_settings_minimal(self) -> None:
        """Test UserSettings with minimal required fields."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
        )

        assert settings.user_name == "John Doe"
        assert settings.user_email == "john@example.com"
        assert settings.default_model == "sonnet"
        assert settings.resume_path is None
        assert settings.preferences == {}

    def test_user_settings_missing_user_name_raises_error(self) -> None:
        """Test missing user_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_email="john@example.com",
                default_model="sonnet",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("user_name",) for e in errors)

    def test_user_settings_missing_user_email_raises_error(self) -> None:
        """Test missing user_email raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_name="John Doe",
                default_model="sonnet",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("user_email",) for e in errors)

    def test_user_settings_missing_default_model_raises_error(self) -> None:
        """Test missing default_model raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            UserSettings(
                user_name="John Doe",
                user_email="john@example.com",
            )

        errors = exc_info.value.errors()
        assert any(e["loc"] == ("default_model",) for e in errors)


@pytest.mark.unit
class TestUserSettingsDefaults:
    """Test suite for UserSettings default values."""

    def test_resume_path_defaults_to_none(self) -> None:
        """Test resume_path defaults to None."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
        )
        assert settings.resume_path is None

    def test_preferences_defaults_to_empty_dict(self) -> None:
        """Test preferences defaults to empty dict."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
        )
        assert settings.preferences == {}


@pytest.mark.unit
class TestUserSettingsValidation:
    """Test suite for UserSettings validation."""

    def test_user_email_accepts_valid_format(self) -> None:
        """Test user_email accepts valid email format."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john.doe@example.com",
            default_model="sonnet",
        )
        assert settings.user_email == "john.doe@example.com"

    def test_user_email_accepts_complex_format(self) -> None:
        """Test user_email accepts complex email format."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john+tag@subdomain.example.co.uk",
            default_model="sonnet",
        )
        assert settings.user_email == "john+tag@subdomain.example.co.uk"

    @pytest.mark.parametrize("model", ["sonnet", "haiku", "opus"])
    def test_default_model_valid_values(self, model: str) -> None:
        """Test default_model accepts valid Claude model names."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model=model,
        )
        assert settings.default_model == model

    def test_resume_path_accepts_relative_path(self) -> None:
        """Test resume_path accepts relative file paths."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            resume_path="./data/resume.md",
        )
        assert settings.resume_path == "./data/resume.md"

    def test_resume_path_accepts_absolute_path(self) -> None:
        """Test resume_path accepts absolute file paths."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            resume_path="/home/user/documents/resume.md",
        )
        assert settings.resume_path == "/home/user/documents/resume.md"

    def test_resume_path_accepts_windows_path(self) -> None:
        """Test resume_path accepts Windows file paths."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            resume_path="C:\\Users\\John\\Documents\\resume.md",
        )
        assert "C:" in settings.resume_path


@pytest.mark.unit
class TestUserSettingsPreferences:
    """Test suite for UserSettings preferences field."""

    def test_preferences_accepts_dict(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test preferences accepts dictionary."""
        settings = UserSettings(**sample_user_settings_data)

        assert settings.preferences["auto_analyze"] is True
        assert settings.preferences["notification_enabled"] is False

    def test_preferences_with_nested_values(self) -> None:
        """Test preferences with nested dict values."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            preferences={
                "notifications": {
                    "email": True,
                    "browser": False,
                },
                "theme": "dark",
            },
        )
        assert settings.preferences["notifications"]["email"] is True
        assert settings.preferences["theme"] == "dark"

    def test_preferences_with_various_types(self) -> None:
        """Test preferences with various value types."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            preferences={
                "string_val": "test",
                "int_val": 42,
                "float_val": 3.14,
                "bool_val": True,
                "list_val": [1, 2, 3],
                "none_val": None,
            },
        )
        assert settings.preferences["string_val"] == "test"
        assert settings.preferences["int_val"] == 42
        assert settings.preferences["float_val"] == 3.14
        assert settings.preferences["bool_val"] is True
        assert settings.preferences["list_val"] == [1, 2, 3]
        assert settings.preferences["none_val"] is None

    def test_preferences_empty_dict(self) -> None:
        """Test preferences with empty dict."""
        settings = UserSettings(
            user_name="John Doe",
            user_email="john@example.com",
            default_model="sonnet",
            preferences={},
        )
        assert settings.preferences == {}


@pytest.mark.unit
class TestUserSettingsSerialization:
    """Test suite for UserSettings serialization."""

    def test_user_settings_to_dict(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test UserSettings.model_dump() produces correct dict."""
        settings = UserSettings(**sample_user_settings_data)
        data = settings.model_dump()

        assert data["user_name"] == sample_user_settings_data["user_name"]
        assert data["user_email"] == sample_user_settings_data["user_email"]
        assert data["default_model"] == sample_user_settings_data["default_model"]
        assert data["resume_path"] == sample_user_settings_data["resume_path"]
        assert data["preferences"] == sample_user_settings_data["preferences"]

    def test_user_settings_to_json(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test UserSettings.model_dump_json() produces valid JSON."""
        settings = UserSettings(**sample_user_settings_data)
        json_str = settings.model_dump_json()

        parsed = json.loads(json_str)
        assert parsed["user_name"] == sample_user_settings_data["user_name"]
        assert parsed["preferences"] == sample_user_settings_data["preferences"]

    def test_user_settings_from_dict(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test creating UserSettings from dictionary."""
        settings = UserSettings.model_validate(sample_user_settings_data)

        assert settings.user_name == sample_user_settings_data["user_name"]
        assert settings.user_email == sample_user_settings_data["user_email"]

    def test_user_settings_round_trip(
        self, sample_user_settings_data: Dict[str, Any]
    ) -> None:
        """Test serialization/deserialization round trip."""
        original = UserSettings(**sample_user_settings_data)
        json_str = original.model_dump_json()
        restored = UserSettings.model_validate_json(json_str)

        assert restored.user_name == original.user_name
        assert restored.user_email == original.user_email
        assert restored.default_model == original.default_model
        assert restored.resume_path == original.resume_path
        assert restored.preferences == original.preferences


@pytest.mark.unit
class TestUserSettingsEdgeCases:
    """Test suite for UserSettings edge cases."""

    def test_user_settings_with_unicode_name(self) -> None:
        """Test UserSettings with unicode characters in name."""
        settings = UserSettings(
            user_name="田中太郎",
            user_email="tanaka@example.com",
            default_model="sonnet",
        )
        assert settings.user_name == "田中太郎"

    def test_user_settings_with_long_email(self) -> None:
        """Test UserSettings with long email address."""
        long_email = "very.long.email" + ".part" * 10 + "@example.com"
        settings = UserSettings(
            user_name="John Doe",
            user_email=long_email,
            default_model="sonnet",
        )
        assert settings.user_email == long_email

    def test_user_settings_with_special_chars_in_name(self) -> None:
        """Test UserSettings with special characters in name."""
        settings = UserSettings(
            user_name="John O'Brien-Smith, Jr.",
            user_email="john@example.com",
            default_model="sonnet",
        )
        assert "O'Brien" in settings.user_name

    def test_user_settings_preferences_mutable_default(self) -> None:
        """Test that preferences default doesn't share state between instances."""
        settings1 = UserSettings(
            user_name="John",
            user_email="john@example.com",
            default_model="sonnet",
        )
        settings2 = UserSettings(
            user_name="Jane",
            user_email="jane@example.com",
            default_model="haiku",
        )

        # Modify one instance
        settings1.preferences["key"] = "value"

        # Other instance should not be affected
        assert "key" not in settings2.preferences
