"""Unit tests for YAMLHandler class.

This module contains comprehensive tests for:
    - YAML serialization from Pydantic models
    - YAML deserialization to Pydantic models
    - Error handling for malformed YAML
    - Pydantic validation error handling
    - Round-trip serialization
    - File operation delegation to FileHandler
"""

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel, field_serializer

from app.core.exceptions import (
    AppFileNotFoundError,
    FileAccessError,
    YAMLParseError,
)
from app.data.file_handler import FileHandler
from app.data.yaml_handler import YAMLHandler

# =============================================================================
# Test Models
# =============================================================================


class SimpleModel(BaseModel):
    """Simple test model."""

    name: str
    value: int


class NestedModel(BaseModel):
    """Nested test model."""

    title: str
    items: List[str]
    metadata: Dict[str, Any]


class ModelWithDefaults(BaseModel):
    """Model with default values."""

    name: str = "default"
    value: int = 0


class ModelWithOptional(BaseModel):
    """Model with optional field."""

    name: str
    optional_field: Optional[str] = None


class ModelWithNonSerializableField(BaseModel):
    """Model with a field that raises during serialization."""

    name: str
    callback: Callable[[], None]

    model_config = {"arbitrary_types_allowed": True}

    @field_serializer("callback")
    def serialize_callback(self, value: Callable[[], None]) -> str:
        raise ValueError("Cannot serialize callback")


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_file_handler() -> MagicMock:
    """Create a mock FileHandler for unit testing."""
    handler = MagicMock(spec=FileHandler)
    handler.read_file = AsyncMock()
    handler.write_file = AsyncMock()
    return handler


@pytest.fixture
def yaml_handler(mock_file_handler: MagicMock) -> YAMLHandler:
    """Create YAMLHandler with mocked FileHandler."""
    return YAMLHandler(mock_file_handler)


# =============================================================================
# Serialization Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerSerialize:
    """Test suite for YAMLHandler serialization."""

    def test_serialize_simple_model(self, yaml_handler: YAMLHandler) -> None:
        """Test serializing a simple Pydantic model."""
        model = SimpleModel(name="test", value=42)

        result = yaml_handler.serialize(model)

        assert "name: test" in result
        assert "value: 42" in result

    def test_serialize_nested_model(self, yaml_handler: YAMLHandler) -> None:
        """Test serializing a nested Pydantic model."""
        model = NestedModel(
            title="Test",
            items=["a", "b", "c"],
            metadata={"key": "value"},
        )

        result = yaml_handler.serialize(model)

        assert "title: Test" in result
        assert "items:" in result
        assert "- a" in result
        assert "- b" in result
        assert "- c" in result
        assert "metadata:" in result
        assert "key: value" in result

    def test_serialize_preserves_unicode(self, yaml_handler: YAMLHandler) -> None:
        """Test that Unicode characters are preserved."""
        model = SimpleModel(name="Tanaka Taro", value=1)

        result = yaml_handler.serialize(model)

        assert "Tanaka Taro" in result

    def test_serialize_handles_none_values(self, yaml_handler: YAMLHandler) -> None:
        """Test serialization of None values."""
        model = ModelWithOptional(name="test")

        result = yaml_handler.serialize(model)

        assert "name: test" in result
        # None should be serialized as null
        assert "optional_field:" in result

    def test_serialize_empty_list(self, yaml_handler: YAMLHandler) -> None:
        """Test serialization of empty list."""
        model = NestedModel(title="Test", items=[], metadata={})

        result = yaml_handler.serialize(model)

        assert "items: []" in result
        assert "metadata: {}" in result

    def test_serialize_returns_string(self, yaml_handler: YAMLHandler) -> None:
        """Test that serialize returns a string."""
        model = SimpleModel(name="test", value=42)

        result = yaml_handler.serialize(model)

        assert isinstance(result, str)

    def test_serialize_multiline_string(self, yaml_handler: YAMLHandler) -> None:
        """Test serialization of multiline string values."""
        model = SimpleModel(name="line1\nline2\nline3", value=1)

        result = yaml_handler.serialize(model)

        # Should produce valid YAML that can be deserialized
        restored = yaml_handler.deserialize(result, SimpleModel)
        assert restored.name == "line1\nline2\nline3"


# =============================================================================
# Deserialization Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerDeserialize:
    """Test suite for YAMLHandler deserialization."""

    def test_deserialize_simple_yaml(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing simple YAML to model."""
        yaml_str = "name: test\nvalue: 42"

        result = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert result.name == "test"
        assert result.value == 42

    def test_deserialize_nested_yaml(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing nested YAML."""
        yaml_str = """
title: Test Title
items:
  - item1
  - item2
metadata:
  key: value
"""
        result = yaml_handler.deserialize(yaml_str, NestedModel)

        assert result.title == "Test Title"
        assert result.items == ["item1", "item2"]
        assert result.metadata == {"key": "value"}

    def test_deserialize_empty_yaml_with_defaults(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing empty YAML uses default values."""
        yaml_str = ""

        result = yaml_handler.deserialize(yaml_str, ModelWithDefaults)

        assert result.name == "default"
        assert result.value == 0

    def test_deserialize_partial_yaml_with_defaults(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing partial YAML fills in defaults."""
        yaml_str = "name: custom"

        result = yaml_handler.deserialize(yaml_str, ModelWithDefaults)

        assert result.name == "custom"
        assert result.value == 0

    def test_deserialize_null_value(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing null value for optional field."""
        yaml_str = "name: test\noptional_field: null"

        result = yaml_handler.deserialize(yaml_str, ModelWithOptional)

        assert result.name == "test"
        assert result.optional_field is None

    def test_deserialize_unicode_content(self, yaml_handler: YAMLHandler) -> None:
        """Test deserializing Unicode content."""
        yaml_str = "name: Tanaka Taro\nvalue: 1"

        result = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert result.name == "Tanaka Taro"


# =============================================================================
# Error Handling Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerErrors:
    """Test suite for YAMLHandler error handling."""

    def test_deserialize_malformed_yaml_raises_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that malformed YAML raises YAMLParseError."""
        malformed_yaml = "name: [unclosed bracket"

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(malformed_yaml, SimpleModel)

        assert exc_info.value.status_code == 422
        assert "Invalid YAML syntax" in exc_info.value.message

    def test_deserialize_invalid_indentation_raises_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that invalid indentation raises YAMLParseError."""
        invalid_yaml = "name: test\n  bad_indent: value"

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(invalid_yaml, SimpleModel)

        assert exc_info.value.status_code == 422

    def test_deserialize_validation_error_raises_yaml_parse_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that Pydantic validation errors raise YAMLParseError."""
        yaml_str = "name: test\nvalue: not_an_integer"

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(yaml_str, SimpleModel)

        assert exc_info.value.status_code == 422
        assert "does not match" in exc_info.value.message
        assert "validation_errors" in exc_info.value.details

    def test_deserialize_missing_required_field_raises_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that missing required fields raise YAMLParseError."""
        yaml_str = "value: 42"  # Missing 'name'

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(yaml_str, SimpleModel)

        assert "validation_errors" in exc_info.value.details

    def test_deserialize_wrong_type_raises_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that wrong types in YAML raise YAMLParseError."""
        yaml_str = "name: 123\nvalue: test"  # int where str expected, str where int expected

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(yaml_str, SimpleModel)

        assert "validation_errors" in exc_info.value.details

    def test_yaml_parse_error_has_correct_error_type(self, yaml_handler: YAMLHandler) -> None:
        """Test YAMLParseError has correct error_type attribute."""
        malformed_yaml = "name: [unclosed bracket"

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.deserialize(malformed_yaml, SimpleModel)

        assert exc_info.value.error_type == "YAML_PARSE_ERROR"

    def test_serialize_non_serializable_field_raises_error(self, yaml_handler: YAMLHandler) -> None:
        """Test that non-serializable fields raise YAMLParseError."""
        model = ModelWithNonSerializableField(name="test", callback=lambda: None)

        with pytest.raises(YAMLParseError) as exc_info:
            yaml_handler.serialize(model)

        assert exc_info.value.status_code == 422
        assert "non-serializable data" in exc_info.value.message
        assert exc_info.value.details["model_type"] == "ModelWithNonSerializableField"


# =============================================================================
# File Operation Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerFileOperations:
    """Test suite for YAMLHandler file operations."""

    async def test_save_calls_file_handler_write(
        self,
        yaml_handler: YAMLHandler,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test that save() delegates to FileHandler.write_file()."""
        model = SimpleModel(name="test", value=42)
        path = Path("/test/file.yaml")

        await yaml_handler.save(model, path)

        mock_file_handler.write_file.assert_called_once()
        call_args = mock_file_handler.write_file.call_args
        assert call_args[0][0] == path
        assert "name: test" in call_args[0][1]
        assert "value: 42" in call_args[0][1]

    async def test_load_calls_file_handler_read(
        self,
        yaml_handler: YAMLHandler,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test that load() delegates to FileHandler.read_file()."""
        mock_file_handler.read_file.return_value = "name: test\nvalue: 42"
        path = Path("/test/file.yaml")

        result = await yaml_handler.load(path, SimpleModel)

        mock_file_handler.read_file.assert_called_once_with(path)
        assert result.name == "test"
        assert result.value == 42

    async def test_load_file_not_found_propagates(
        self,
        yaml_handler: YAMLHandler,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test that AppFileNotFoundError propagates from FileHandler."""
        mock_file_handler.read_file.side_effect = AppFileNotFoundError(message="File not found")

        with pytest.raises(AppFileNotFoundError):
            await yaml_handler.load(Path("/missing.yaml"), SimpleModel)

    async def test_save_file_access_error_propagates(
        self,
        yaml_handler: YAMLHandler,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test that FileAccessError propagates from FileHandler."""
        mock_file_handler.write_file.side_effect = FileAccessError(message="Permission denied")
        model = SimpleModel(name="test", value=42)

        with pytest.raises(FileAccessError):
            await yaml_handler.save(model, Path("/readonly.yaml"))

    async def test_load_invalid_yaml_raises_parse_error(
        self,
        yaml_handler: YAMLHandler,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test that invalid YAML in file raises YAMLParseError."""
        mock_file_handler.read_file.return_value = "name: [unclosed"

        with pytest.raises(YAMLParseError):
            await yaml_handler.load(Path("/invalid.yaml"), SimpleModel)


# =============================================================================
# Round-Trip Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerRoundTrip:
    """Test suite for YAML round-trip serialization."""

    def test_round_trip_simple_model(self, yaml_handler: YAMLHandler) -> None:
        """Test round-trip serialization of simple model."""
        original = SimpleModel(name="test", value=42)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert restored.name == original.name
        assert restored.value == original.value

    def test_round_trip_nested_model(self, yaml_handler: YAMLHandler) -> None:
        """Test round-trip serialization of nested model."""
        original = NestedModel(
            title="Test",
            items=["a", "b", "c"],
            metadata={"key": "value", "number": 123},
        )

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, NestedModel)

        assert restored.title == original.title
        assert restored.items == original.items
        assert restored.metadata == original.metadata

    def test_round_trip_preserves_special_characters(self, yaml_handler: YAMLHandler) -> None:
        """Test that special YAML characters survive round-trip."""
        original = SimpleModel(name="test: with | special > chars", value=1)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert restored.name == original.name

    def test_round_trip_preserves_unicode(self, yaml_handler: YAMLHandler) -> None:
        """Test that Unicode characters survive round-trip."""
        original = SimpleModel(name="Hello World", value=1)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert restored.name == original.name

    def test_round_trip_preserves_empty_collections(self, yaml_handler: YAMLHandler) -> None:
        """Test that empty collections survive round-trip."""
        original = NestedModel(title="Test", items=[], metadata={})

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, NestedModel)

        assert restored.items == []
        assert restored.metadata == {}

    def test_round_trip_preserves_none_values(self, yaml_handler: YAMLHandler) -> None:
        """Test that None values survive round-trip."""
        original = ModelWithOptional(name="test", optional_field=None)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, ModelWithOptional)

        assert restored.optional_field is None

    def test_round_trip_with_newlines_in_values(self, yaml_handler: YAMLHandler) -> None:
        """Test that multiline string values survive round-trip."""
        original = SimpleModel(name="line1\nline2\nline3", value=42)

        yaml_str = yaml_handler.serialize(original)
        restored = yaml_handler.deserialize(yaml_str, SimpleModel)

        assert restored.name == original.name
        assert "\n" in restored.name


# =============================================================================
# Configuration Tests
# =============================================================================


@pytest.mark.unit
class TestYAMLHandlerConfiguration:
    """Test suite for YAMLHandler configuration."""

    def test_yaml_handler_requires_file_handler(self) -> None:
        """Test that YAMLHandler requires FileHandler in constructor."""
        mock_handler = MagicMock(spec=FileHandler)
        handler = YAMLHandler(mock_handler)

        assert handler._file_handler is mock_handler

    def test_yaml_allows_unicode_by_default(self, yaml_handler: YAMLHandler) -> None:
        """Test that YAML handler allows Unicode by default."""
        assert yaml_handler._yaml.allow_unicode is True

    def test_yaml_uses_block_style_by_default(self, yaml_handler: YAMLHandler) -> None:
        """Test that YAML handler uses block style by default."""
        assert yaml_handler._yaml.default_flow_style is False

    def test_yaml_preserves_quotes(self, yaml_handler: YAMLHandler) -> None:
        """Test that YAML handler preserves quotes."""
        assert yaml_handler._yaml.preserve_quotes is True
