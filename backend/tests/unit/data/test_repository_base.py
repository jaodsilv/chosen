"""Unit tests for RepositoryBase abstract class.

This module contains comprehensive tests for:
    - RepositoryBase initialization and directory creation
    - Abstract method signatures
    - Protected helper methods
    - Subclassing behavior
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel

from app.data.file_handler import FileHandler
from app.data.repository_base import RepositoryBase
from app.data.yaml_handler import YAMLHandler


# =============================================================================
# Test Model and Concrete Implementation
# =============================================================================


class SampleEntity(BaseModel):
    """Sample entity model for unit tests."""

    id: str
    name: str
    value: int = 0


class ConcreteRepository(RepositoryBase[SampleEntity]):
    """Concrete implementation for testing abstract base class."""

    async def get(self, id: str) -> Optional[SampleEntity]:
        """Get entity by ID - test implementation."""
        path = self._get_entity_path(id)
        if not await self._file_exists(path):
            return None
        return await self.yaml_handler.load(path, self.model_class)

    async def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[SampleEntity]:
        """List entities - test implementation."""
        return []

    async def save(self, entity: SampleEntity) -> SampleEntity:
        """Save entity - test implementation."""
        path = self._get_entity_path(entity.id)
        await self.yaml_handler.save(entity, path)
        return entity

    async def delete(self, id: str) -> bool:
        """Delete entity - test implementation."""
        path = self._get_entity_path(id)
        if not await self._file_exists(path):
            return False
        await self.yaml_handler._file_handler.delete_file(path)
        return True


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_file_handler() -> MagicMock:
    """Create a mock FileHandler."""
    handler = MagicMock(spec=FileHandler)
    handler.file_exists = AsyncMock(return_value=False)
    handler.delete_file = AsyncMock(return_value=True)
    return handler


@pytest.fixture
def mock_yaml_handler(mock_file_handler: MagicMock) -> MagicMock:
    """Create a mock YAMLHandler with mocked FileHandler."""
    handler = MagicMock(spec=YAMLHandler)
    handler._file_handler = mock_file_handler
    handler.load = AsyncMock()
    handler.save = AsyncMock()
    return handler


@pytest.fixture
def repository(
    tmp_path: Path,
    mock_yaml_handler: MagicMock,
) -> ConcreteRepository:
    """Create a ConcreteRepository instance for testing."""
    return ConcreteRepository(
        data_dir=tmp_path / "entities",
        model_class=SampleEntity,
        yaml_handler=mock_yaml_handler,
    )


# =============================================================================
# Initialization Tests
# =============================================================================


@pytest.mark.unit
class TestRepositoryBaseInit:
    """Test suite for RepositoryBase initialization."""

    def test_init_creates_data_directory(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that __init__ creates the data directory."""
        data_dir = tmp_path / "new_entities"
        assert not data_dir.exists()

        ConcreteRepository(
            data_dir=data_dir,
            model_class=SampleEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert data_dir.exists()
        assert data_dir.is_dir()

    def test_init_creates_nested_directories(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that __init__ creates nested parent directories."""
        data_dir = tmp_path / "deep" / "nested" / "path"
        assert not data_dir.exists()

        ConcreteRepository(
            data_dir=data_dir,
            model_class=SampleEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert data_dir.exists()

    def test_init_accepts_existing_directory(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that __init__ works with existing directory."""
        data_dir = tmp_path / "existing"
        data_dir.mkdir()

        # Should not raise
        repo = ConcreteRepository(
            data_dir=data_dir,
            model_class=SampleEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert repo.data_dir == data_dir

    def test_init_stores_model_class(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that model_class is stored correctly."""
        repo = ConcreteRepository(
            data_dir=tmp_path,
            model_class=SampleEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert repo.model_class is SampleEntity

    def test_init_stores_yaml_handler(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that yaml_handler is stored correctly."""
        repo = ConcreteRepository(
            data_dir=tmp_path,
            model_class=SampleEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert repo.yaml_handler is mock_yaml_handler


# =============================================================================
# Helper Method Tests
# =============================================================================


@pytest.mark.unit
class TestRepositoryBaseHelpers:
    """Test suite for RepositoryBase helper methods."""

    def test_get_entity_path_default_implementation(
        self,
        repository: ConcreteRepository,
    ) -> None:
        """Test _get_entity_path returns correct path."""
        path = repository._get_entity_path("test-id-123")

        assert path == repository.data_dir / "test-id-123.yaml"

    def test_get_entity_path_with_uuid(
        self,
        repository: ConcreteRepository,
    ) -> None:
        """Test _get_entity_path handles UUID-like IDs."""
        uuid_id = "550e8400-e29b-41d4-a716-446655440000"
        path = repository._get_entity_path(uuid_id)

        assert path == repository.data_dir / f"{uuid_id}.yaml"

    @pytest.mark.asyncio
    async def test_file_exists_delegates_to_file_handler(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test _file_exists delegates to FileHandler."""
        mock_file_handler.file_exists.return_value = True
        test_path = Path("/some/path.yaml")

        result = await repository._file_exists(test_path)

        assert result is True
        mock_file_handler.file_exists.assert_called_once_with(test_path)

    @pytest.mark.asyncio
    async def test_file_exists_returns_false_when_not_found(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test _file_exists returns False when file doesn't exist."""
        mock_file_handler.file_exists.return_value = False
        test_path = Path("/nonexistent/path.yaml")

        result = await repository._file_exists(test_path)

        assert result is False


# =============================================================================
# CRUD Operation Tests (via Concrete Implementation)
# =============================================================================


@pytest.mark.unit
class TestRepositoryBaseCRUD:
    """Test suite for CRUD operations via concrete implementation."""

    @pytest.mark.asyncio
    async def test_get_returns_none_when_not_found(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test get returns None when entity doesn't exist."""
        mock_file_handler.file_exists.return_value = False

        result = await repository.get("nonexistent-id")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_loads_entity_when_found(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test get loads entity when file exists."""
        mock_file_handler.file_exists.return_value = True
        expected_entity = SampleEntity(id="test-123", name="Test", value=42)
        mock_yaml_handler.load.return_value = expected_entity

        result = await repository.get("test-123")

        assert result == expected_entity
        mock_yaml_handler.load.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_delegates_to_yaml_handler(
        self,
        repository: ConcreteRepository,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test save delegates to YAMLHandler."""
        entity = SampleEntity(id="test-123", name="Test", value=42)

        result = await repository.save(entity)

        assert result == entity
        mock_yaml_handler.save.assert_called_once()
        call_args = mock_yaml_handler.save.call_args
        assert call_args[0][0] == entity

    @pytest.mark.asyncio
    async def test_delete_returns_false_when_not_found(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test delete returns False when entity doesn't exist."""
        mock_file_handler.file_exists.return_value = False

        result = await repository.delete("nonexistent-id")

        assert result is False
        mock_file_handler.delete_file.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_delegates_to_file_handler(
        self,
        repository: ConcreteRepository,
        mock_file_handler: MagicMock,
    ) -> None:
        """Test delete delegates to FileHandler."""
        mock_file_handler.file_exists.return_value = True
        mock_file_handler.delete_file.return_value = True

        result = await repository.delete("test-123")

        assert result is True
        mock_file_handler.delete_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_returns_empty_list(
        self,
        repository: ConcreteRepository,
    ) -> None:
        """Test list returns empty list (stub implementation)."""
        result = await repository.list()

        assert result == []


# =============================================================================
# Abstract Class Behavior Tests
# =============================================================================


@pytest.mark.unit
class TestRepositoryBaseAbstract:
    """Test suite for abstract class behavior."""

    def test_cannot_instantiate_directly(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that RepositoryBase cannot be instantiated directly."""
        with pytest.raises(TypeError) as exc_info:
            RepositoryBase(  # type: ignore[abstract]
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )

        assert "abstract" in str(exc_info.value).lower()

    def test_subclass_must_implement_get(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that subclass must implement get()."""

        class IncompleteRepo(RepositoryBase[SampleEntity]):
            async def list(
                self,
                filters: Optional[Dict[str, Any]] = None,
                limit: int = 100,
                offset: int = 0,
            ) -> List[SampleEntity]:
                return []

            async def save(self, entity: SampleEntity) -> SampleEntity:
                return entity

            async def delete(self, id: str) -> bool:
                return True

        with pytest.raises(TypeError):
            IncompleteRepo(
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )

    def test_subclass_must_implement_list(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that subclass must implement list()."""

        class IncompleteRepo(RepositoryBase[SampleEntity]):
            async def get(self, id: str) -> Optional[SampleEntity]:
                return None

            async def save(self, entity: SampleEntity) -> SampleEntity:
                return entity

            async def delete(self, id: str) -> bool:
                return True

        with pytest.raises(TypeError):
            IncompleteRepo(
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )

    def test_subclass_must_implement_save(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that subclass must implement save()."""

        class IncompleteRepo(RepositoryBase[SampleEntity]):
            async def get(self, id: str) -> Optional[SampleEntity]:
                return None

            async def list(
                self,
                filters: Optional[Dict[str, Any]] = None,
                limit: int = 100,
                offset: int = 0,
            ) -> List[SampleEntity]:
                return []

            async def delete(self, id: str) -> bool:
                return True

        with pytest.raises(TypeError):
            IncompleteRepo(
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )

    def test_subclass_must_implement_delete(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that subclass must implement delete()."""

        class IncompleteRepo(RepositoryBase[SampleEntity]):
            async def get(self, id: str) -> Optional[SampleEntity]:
                return None

            async def list(
                self,
                filters: Optional[Dict[str, Any]] = None,
                limit: int = 100,
                offset: int = 0,
            ) -> List[SampleEntity]:
                return []

            async def save(self, entity: SampleEntity) -> SampleEntity:
                return entity

        with pytest.raises(TypeError):
            IncompleteRepo(
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )

    def test_subclass_must_implement_all_methods(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that subclass must implement all abstract methods."""

        class EmptyRepo(RepositoryBase[SampleEntity]):
            pass

        with pytest.raises(TypeError):
            EmptyRepo(  # type: ignore[abstract]
                data_dir=tmp_path,
                model_class=SampleEntity,
                yaml_handler=mock_yaml_handler,
            )


# =============================================================================
# Type Safety Tests
# =============================================================================


@pytest.mark.unit
class TestRepositoryBaseTypeSafety:
    """Test suite for type safety and generics."""

    def test_model_class_type_preserved(
        self,
        repository: ConcreteRepository,
    ) -> None:
        """Test that model_class type is preserved."""
        assert repository.model_class is SampleEntity
        # This allows proper type inference in concrete implementations

    def test_generic_type_parameter(
        self,
        tmp_path: Path,
        mock_yaml_handler: MagicMock,
    ) -> None:
        """Test that generic type parameter works correctly."""

        class AnotherEntity(BaseModel):
            id: str
            data: str

        class AnotherRepository(RepositoryBase[AnotherEntity]):
            async def get(self, id: str) -> Optional[AnotherEntity]:
                return None

            async def list(
                self,
                filters: Optional[Dict[str, Any]] = None,
                limit: int = 100,
                offset: int = 0,
            ) -> List[AnotherEntity]:
                return []

            async def save(self, entity: AnotherEntity) -> AnotherEntity:
                return entity

            async def delete(self, id: str) -> bool:
                return True

        repo = AnotherRepository(
            data_dir=tmp_path,
            model_class=AnotherEntity,
            yaml_handler=mock_yaml_handler,
        )

        assert repo.model_class is AnotherEntity
