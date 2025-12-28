"""YAMLHandler for YAML serialization/deserialization with Pydantic models.

This module provides YAML handling with:
    - Pydantic model serialization/deserialization
    - Comment and formatting preservation via ruamel.yaml
    - Schema validation through Pydantic model_validate
    - Graceful error handling mapped to AppException hierarchy

Example usage::

    from pathlib import Path
    from app.data.yaml_handler import YAMLHandler
    from app.data.file_handler import FileHandler
    from app.models.conversation import Conversation

    async def main():
        file_handler = FileHandler()
        yaml_handler = YAMLHandler(file_handler)

        # Load from file
        conv = await yaml_handler.load(Path("data.yaml"), Conversation)

        # Save to file
        await yaml_handler.save(conv, Path("output.yaml"))
"""

import logging
from io import StringIO
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from pydantic_core import PydanticSerializationError
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from app.core.exceptions import YAMLParseError
from app.data.file_handler import FileHandler

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class YAMLHandler:
    """Handles YAML serialization and deserialization with Pydantic models.

    This class provides:
        - Serialization of Pydantic models to YAML strings
        - Deserialization of YAML strings to Pydantic models
        - Async file save/load operations via FileHandler
        - Comment and formatting preservation using ruamel.yaml round-trip mode

    All file operations delegate to FileHandler, keeping this class focused
    on YAML transformation. File locking should be handled by the caller
    using FileHandler.locked() when needed.

    Example usage::

        handler = YAMLHandler(file_handler)

        # Serialize model to YAML string
        yaml_str = handler.serialize(conversation)

        # Deserialize YAML string to model
        conv = handler.deserialize(yaml_str, Conversation)

        # Save model to file
        await handler.save(conversation, Path("conv.yaml"))

        # Load model from file
        conv = await handler.load(Path("conv.yaml"), Conversation)
    """

    def __init__(self, file_handler: FileHandler) -> None:
        """Initialize YAMLHandler with a FileHandler dependency.

        Args:
            file_handler: FileHandler instance for file I/O operations.
        """
        self._file_handler = file_handler
        self._yaml = YAML()
        self._yaml.preserve_quotes = True
        self._yaml.default_flow_style = False
        self._yaml.allow_unicode = True
        self._yaml.width = 4096  # Prevent unwanted line wrapping

    def serialize(self, model: BaseModel) -> str:
        """Serialize a Pydantic model to a YAML string.

        Uses model_dump(mode="json") to ensure JSON-compatible types that
        serialize cleanly to YAML (e.g., datetime as ISO strings, UUIDs as
        strings, enums as values).

        Args:
            model: The Pydantic model instance to serialize.

        Returns:
            YAML-formatted string representation of the model.

        Raises:
            YAMLParseError: If serialization fails due to non-serializable data
                or YAML encoding issues.
        """
        try:
            data = model.model_dump(mode="json")
            stream = StringIO()
            self._yaml.dump(data, stream)
            return stream.getvalue()
        except PydanticSerializationError as e:
            raise YAMLParseError(
                message=(f"Failed to serialize {type(model).__name__}: " "model contains non-serializable data"),
                details={
                    "model_type": type(model).__name__,
                    "error": str(e),
                },
            ) from e
        except YAMLError as e:
            raise YAMLParseError(
                message=f"Failed to serialize model to YAML: {e}",
                details={"model_type": type(model).__name__, "error": str(e)},
            ) from e

    def deserialize(self, yaml_str: str, model_class: Type[T]) -> T:
        """Deserialize a YAML string to a Pydantic model instance.

        Parses the YAML string and validates it against the specified Pydantic
        model class using model_validate().

        Args:
            yaml_str: The YAML string to deserialize.
            model_class: The Pydantic model class to validate against.

        Returns:
            An instance of model_class populated with data from the YAML.

        Raises:
            YAMLParseError: If the YAML syntax is invalid or if the data
                fails Pydantic validation.
        """
        try:
            data = self._yaml.load(StringIO(yaml_str))
            if data is None:
                logger.debug(
                    "YAML parsed to None (empty or null content), " "using empty dict for %s validation",
                    model_class.__name__,
                )
                data = {}
            return model_class.model_validate(data)
        except YAMLError as e:
            raise YAMLParseError(
                message=f"Invalid YAML syntax: {e}",
                details={"error": str(e), "model_class": model_class.__name__},
            ) from e
        except PydanticValidationError as e:
            raise YAMLParseError(
                message=f"YAML data does not match {model_class.__name__} schema",
                details={
                    "model_class": model_class.__name__,
                    "validation_errors": e.errors(),
                },
            ) from e

    async def save(self, model: BaseModel, path: Path) -> None:
        """Save a Pydantic model to a YAML file.

        Serializes the model to YAML and writes to the specified path.
        Creates parent directories if they don't exist.

        Note:
            This method does not acquire file locks. Use FileHandler.locked()
            if you need exclusive access during save operations.

        Args:
            model: The Pydantic model instance to save.
            path: The file path to write to.

        Raises:
            YAMLParseError: If serialization fails.
            FileAccessError: If there's a permission error writing the file.
            FileOperationError: For other file operation errors.
        """
        yaml_str = self.serialize(model)
        await self._file_handler.write_file(path, yaml_str)

    async def load(self, path: Path, model_class: Type[T]) -> T:
        """Load a YAML file into a Pydantic model instance.

        Reads the file content and deserializes it to the specified model class.

        Note:
            This method does not acquire file locks. Use FileHandler.locked()
            if you need exclusive access during load operations.

        Args:
            path: The file path to read from.
            model_class: The Pydantic model class to validate against.

        Returns:
            An instance of model_class populated with data from the file.

        Raises:
            AppFileNotFoundError: If the file does not exist.
            FileAccessError: If there's a permission error reading the file.
            YAMLParseError: If the YAML is malformed or fails validation.
            FileOperationError: For other file operation errors.
        """
        yaml_str = await self._file_handler.read_file(path)
        return self.deserialize(yaml_str, model_class)
