"""RepositoryBase abstract class for data access.

This module provides the abstract base class for all repositories,
defining the standard CRUD interface for file-based storage.

Example usage::

    from pathlib import Path
    from app.data.repository_base import RepositoryBase
    from app.data.yaml_handler import YAMLHandler
    from app.models.conversation import Conversation

    class ConversationRepository(RepositoryBase[Conversation]):
        def __init__(self, data_dir: Path, yaml_handler: YAMLHandler):
            super().__init__(
                data_dir=data_dir / "conversations",
                model_class=Conversation,
                yaml_handler=yaml_handler,
            )

        async def get(self, id: str) -> Optional[Conversation]:
            # Implementation...
            pass
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel

from app.data.yaml_handler import YAMLHandler

T = TypeVar("T", bound=BaseModel)


class RepositoryBase(ABC, Generic[T]):
    """Abstract base class for data repositories.

    Provides a standard CRUD interface for file-based storage using YAML
    serialization. Concrete implementations must define the abstract methods
    to handle entity-specific logic such as ID extraction and filtering.

    Type Parameters:
        T: The Pydantic model type this repository manages, bound to BaseModel.

    Attributes:
        data_dir: Directory where entity files are stored.
        model_class: The Pydantic model class for type validation.
        yaml_handler: YAMLHandler instance for serialization/deserialization.

    Example::

        class ConversationRepository(RepositoryBase[Conversation]):
            async def get(self, id: str) -> Optional[Conversation]:
                path = self._get_entity_path(id)
                if not await self._file_exists(path):
                    return None
                return await self.yaml_handler.load(path, self.model_class)
    """

    def __init__(
        self,
        data_dir: Path,
        model_class: Type[T],
        yaml_handler: YAMLHandler,
    ) -> None:
        """Initialize the repository.

        Creates the data directory if it does not exist.

        Args:
            data_dir: Directory where entity files will be stored.
            model_class: The Pydantic model class for type validation.
            yaml_handler: YAMLHandler instance for file I/O operations.
        """
        self.data_dir = data_dir
        self.model_class = model_class
        self.yaml_handler = yaml_handler

        # Ensure directory exists (sync, but quick operation)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # Abstract CRUD Methods
    # =========================================================================

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get an entity by its ID.

        Args:
            id: The unique identifier of the entity.

        Returns:
            The entity if found, None otherwise.

        Raises:
            FileAccessError: If there's a permission error reading the file.
            YAMLParseError: If the file contains invalid YAML or fails
                validation.
            FileOperationError: For other file operation errors.
        """
        pass

    @abstractmethod
    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[T]:
        """List entities with optional filtering and pagination.

        Args:
            filters: Optional dictionary of field-value pairs to filter by.
            limit: Maximum number of entities to return (default: 100).
            offset: Number of entities to skip for pagination (default: 0).

        Returns:
            List of entities matching the filters, respecting pagination.

        Raises:
            FileAccessError: If there's a permission error reading files.
            YAMLParseError: If any file contains invalid YAML or fails
                validation.
            FileOperationError: For other file operation errors.
        """
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save (create or update) an entity.

        Args:
            entity: The entity to save.

        Returns:
            The saved entity (may be modified, e.g., updated timestamp).

        Raises:
            FileAccessError: If there's a permission error writing the file.
            YAMLParseError: If serialization fails.
            FileOperationError: For other file operation errors.
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete an entity by its ID.

        Args:
            id: The unique identifier of the entity to delete.

        Returns:
            True if the entity was deleted, False if it didn't exist.

        Raises:
            FileAccessError: If there's a permission error deleting the file.
            FileOperationError: For other file operation errors.
        """
        pass

    # =========================================================================
    # Protected Helper Methods
    # =========================================================================

    def _get_entity_path(self, id: str) -> Path:
        """Get the file path for an entity by ID.

        Default implementation uses ID as filename with .yaml extension.
        Override in subclasses for custom naming conventions.

        Args:
            id: The unique identifier of the entity.

        Returns:
            Path to the entity's YAML file.
        """
        return self.data_dir / f"{id}.yaml"

    async def _file_exists(self, path: Path) -> bool:
        """Check if a file exists.

        Delegates to YAMLHandler's underlying FileHandler.

        Args:
            path: Path to check.

        Returns:
            True if the file exists, False otherwise.
        """
        return await self.yaml_handler._file_handler.file_exists(path)
