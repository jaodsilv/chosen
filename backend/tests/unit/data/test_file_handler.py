"""Unit tests for FileHandler class.

This module contains comprehensive tests for:
    - File read/write operations with UTF-8 encoding
    - Directory operations (create, list, delete)
    - File locking for concurrency safety
    - File information retrieval
    - Error handling
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from app.core.exceptions import (
    AppFileNotFoundError,
    DirectoryNotEmptyError,
    DirectoryNotFoundError,
    FileAccessError,
    FileLockError,
    FileOperationError,
)
from app.data.file_handler import FileHandler, FileInfo, FileLock

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def file_handler() -> FileHandler:
    """Create a FileHandler instance for testing."""
    return FileHandler()


@pytest.fixture
def sample_text_content() -> str:
    """Provide sample text content for file operations."""
    return "Hello, World!\nThis is a test file.\nWith multiple lines."


@pytest.fixture
def sample_unicode_content() -> str:
    """Provide sample Unicode content for encoding tests."""
    return "Hello, 世界! 🌍\nCafé résumé naïve\nДобрый день"


@pytest.fixture
def sample_bytes_content() -> bytes:
    """Provide sample bytes content for binary file operations."""
    return b"\x00\x01\x02\x03\x04\x05\xff\xfe\xfd"


# =============================================================================
# File Read Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerRead:
    """Test suite for FileHandler read operations."""

    async def test_read_file_success(self, tmp_path: Path, file_handler: FileHandler, sample_text_content: str) -> None:
        """Test reading an existing file returns correct content."""
        # Arrange
        test_file = tmp_path / "test.txt"
        test_file.write_text(sample_text_content, encoding="utf-8")

        # Act
        content = await file_handler.read_file(test_file)

        # Assert
        assert content == sample_text_content

    async def test_read_file_with_unicode(
        self, tmp_path: Path, file_handler: FileHandler, sample_unicode_content: str
    ) -> None:
        """Test reading a file with Unicode content."""
        # Arrange
        test_file = tmp_path / "unicode.txt"
        test_file.write_text(sample_unicode_content, encoding="utf-8")

        # Act
        content = await file_handler.read_file(test_file)

        # Assert
        assert content == sample_unicode_content

    async def test_read_file_not_found_raises_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test reading a non-existent file raises AppFileNotFoundError."""
        # Arrange
        non_existent = tmp_path / "does_not_exist.txt"

        # Act & Assert
        with pytest.raises(AppFileNotFoundError) as exc_info:
            await file_handler.read_file(non_existent)

        assert exc_info.value.status_code == 404
        assert "not found" in exc_info.value.message.lower()

    async def test_read_empty_file(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test reading an empty file returns empty string."""
        # Arrange
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")

        # Act
        content = await file_handler.read_file(empty_file)

        # Assert
        assert content == ""

    async def test_read_bytes_success(
        self, tmp_path: Path, file_handler: FileHandler, sample_bytes_content: bytes
    ) -> None:
        """Test reading a binary file returns correct bytes."""
        # Arrange
        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(sample_bytes_content)

        # Act
        content = await file_handler.read_bytes(binary_file)

        # Assert
        assert content == sample_bytes_content

    async def test_read_bytes_not_found_raises_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test reading non-existent binary file raises AppFileNotFoundError."""
        # Arrange
        non_existent = tmp_path / "does_not_exist.bin"

        # Act & Assert
        with pytest.raises(AppFileNotFoundError):
            await file_handler.read_bytes(non_existent)


# =============================================================================
# File Write Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerWrite:
    """Test suite for FileHandler write operations."""

    async def test_write_file_success(
        self, tmp_path: Path, file_handler: FileHandler, sample_text_content: str
    ) -> None:
        """Test writing content to a new file."""
        # Arrange
        test_file = tmp_path / "output.txt"

        # Act
        await file_handler.write_file(test_file, sample_text_content)

        # Assert
        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == sample_text_content

    async def test_write_file_with_unicode(
        self, tmp_path: Path, file_handler: FileHandler, sample_unicode_content: str
    ) -> None:
        """Test writing Unicode content to a file."""
        # Arrange
        test_file = tmp_path / "unicode_output.txt"

        # Act
        await file_handler.write_file(test_file, sample_unicode_content)

        # Assert
        assert test_file.read_text(encoding="utf-8") == sample_unicode_content

    async def test_write_file_creates_parent_directories(
        self, tmp_path: Path, file_handler: FileHandler, sample_text_content: str
    ) -> None:
        """Test writing to a file creates parent directories if needed."""
        # Arrange
        nested_file = tmp_path / "deep" / "nested" / "dir" / "file.txt"

        # Act
        await file_handler.write_file(nested_file, sample_text_content)

        # Assert
        assert nested_file.exists()
        assert nested_file.read_text(encoding="utf-8") == sample_text_content

    async def test_write_file_overwrites_existing(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test writing to an existing file overwrites content."""
        # Arrange
        test_file = tmp_path / "existing.txt"
        test_file.write_text("original content", encoding="utf-8")
        new_content = "new content"

        # Act
        await file_handler.write_file(test_file, new_content)

        # Assert
        assert test_file.read_text(encoding="utf-8") == new_content

    async def test_write_empty_content(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test writing empty content creates empty file."""
        # Arrange
        test_file = tmp_path / "empty_output.txt"

        # Act
        await file_handler.write_file(test_file, "")

        # Assert
        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == ""

    async def test_write_bytes_success(
        self, tmp_path: Path, file_handler: FileHandler, sample_bytes_content: bytes
    ) -> None:
        """Test writing binary content to a file."""
        # Arrange
        binary_file = tmp_path / "binary_output.bin"

        # Act
        await file_handler.write_bytes(binary_file, sample_bytes_content)

        # Assert
        assert binary_file.exists()
        assert binary_file.read_bytes() == sample_bytes_content

    async def test_write_bytes_creates_parent_directories(
        self, tmp_path: Path, file_handler: FileHandler, sample_bytes_content: bytes
    ) -> None:
        """Test writing binary file creates parent directories."""
        # Arrange
        nested_file = tmp_path / "nested" / "binary.bin"

        # Act
        await file_handler.write_bytes(nested_file, sample_bytes_content)

        # Assert
        assert nested_file.exists()


# =============================================================================
# File Delete Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerDelete:
    """Test suite for FileHandler delete operations."""

    async def test_delete_file_success(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting an existing file returns True."""
        # Arrange
        test_file = tmp_path / "to_delete.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act
        result = await file_handler.delete_file(test_file)

        # Assert
        assert result is True
        assert not test_file.exists()

    async def test_delete_file_not_found_returns_false(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting a non-existent file returns False."""
        # Arrange
        non_existent = tmp_path / "does_not_exist.txt"

        # Act
        result = await file_handler.delete_file(non_existent)

        # Assert
        assert result is False


# =============================================================================
# File Existence Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerExists:
    """Test suite for FileHandler existence checks."""

    async def test_file_exists_returns_true(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test file_exists returns True for existing file."""
        # Arrange
        test_file = tmp_path / "exists.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act
        result = await file_handler.file_exists(test_file)

        # Assert
        assert result is True

    async def test_file_exists_returns_false(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test file_exists returns False for non-existent file."""
        # Arrange
        non_existent = tmp_path / "does_not_exist.txt"

        # Act
        result = await file_handler.file_exists(non_existent)

        # Assert
        assert result is False

    async def test_file_exists_returns_false_for_directory(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test file_exists returns False for a directory."""
        # Arrange
        test_dir = tmp_path / "a_directory"
        test_dir.mkdir()

        # Act
        result = await file_handler.file_exists(test_dir)

        # Assert
        assert result is False


# =============================================================================
# Directory Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerDirectory:
    """Test suite for FileHandler directory operations."""

    async def test_create_directory(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test creating a new directory."""
        # Arrange
        new_dir = tmp_path / "new_directory"

        # Act
        await file_handler.create_directory(new_dir)

        # Assert
        assert new_dir.exists()
        assert new_dir.is_dir()

    async def test_create_nested_directories(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test creating nested directories with parents=True."""
        # Arrange
        nested_dir = tmp_path / "level1" / "level2" / "level3"

        # Act
        await file_handler.create_directory(nested_dir, parents=True)

        # Assert
        assert nested_dir.exists()
        assert nested_dir.is_dir()

    async def test_create_directory_already_exists(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test creating a directory that already exists does not raise error."""
        # Arrange
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        # Act & Assert (should not raise)
        await file_handler.create_directory(existing_dir)
        assert existing_dir.exists()

    async def test_create_directory_without_parents_fails(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test creating directory without parents when parent doesn't exist raises error."""
        # Arrange
        nested_dir = tmp_path / "nonexistent_parent" / "child"

        # Act & Assert
        with pytest.raises(FileOperationError):
            await file_handler.create_directory(nested_dir, parents=False)

    async def test_list_directory(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test listing directory contents."""
        # Arrange
        (tmp_path / "file1.txt").write_text("content1", encoding="utf-8")
        (tmp_path / "file2.txt").write_text("content2", encoding="utf-8")
        (tmp_path / "subdir").mkdir()

        # Act
        contents = await file_handler.list_directory(tmp_path)

        # Assert
        names = [p.name for p in contents]
        assert "file1.txt" in names
        assert "file2.txt" in names
        assert "subdir" in names
        assert len(contents) == 3

    async def test_list_directory_with_pattern(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test listing directory with glob pattern."""
        # Arrange
        (tmp_path / "file1.txt").write_text("content1", encoding="utf-8")
        (tmp_path / "file2.yaml").write_text("content2", encoding="utf-8")
        (tmp_path / "file3.txt").write_text("content3", encoding="utf-8")

        # Act
        contents = await file_handler.list_directory(tmp_path, pattern="*.txt")

        # Assert
        names = [p.name for p in contents]
        assert "file1.txt" in names
        assert "file3.txt" in names
        assert "file2.yaml" not in names
        assert len(contents) == 2

    async def test_list_directory_empty(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test listing an empty directory returns empty list."""
        # Arrange
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        # Act
        contents = await file_handler.list_directory(empty_dir)

        # Assert
        assert contents == []

    async def test_list_directory_not_found_raises_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test listing non-existent directory raises DirectoryNotFoundError."""
        # Arrange
        non_existent = tmp_path / "does_not_exist"

        # Act & Assert
        with pytest.raises(DirectoryNotFoundError) as exc_info:
            await file_handler.list_directory(non_existent)

        assert exc_info.value.status_code == 404

    async def test_delete_empty_directory(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting an empty directory."""
        # Arrange
        empty_dir = tmp_path / "empty_dir"
        empty_dir.mkdir()

        # Act
        result = await file_handler.delete_directory(empty_dir)

        # Assert
        assert result is True
        assert not empty_dir.exists()

    async def test_delete_directory_recursive(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting a non-empty directory with recursive=True."""
        # Arrange
        parent_dir = tmp_path / "parent"
        parent_dir.mkdir()
        (parent_dir / "file.txt").write_text("content", encoding="utf-8")
        (parent_dir / "subdir").mkdir()
        (parent_dir / "subdir" / "nested.txt").write_text("nested", encoding="utf-8")

        # Act
        result = await file_handler.delete_directory(parent_dir, recursive=True)

        # Assert
        assert result is True
        assert not parent_dir.exists()

    async def test_delete_non_empty_directory_fails(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting non-empty directory without recursive raises error."""
        # Arrange
        non_empty_dir = tmp_path / "non_empty"
        non_empty_dir.mkdir()
        (non_empty_dir / "file.txt").write_text("content", encoding="utf-8")

        # Act & Assert
        with pytest.raises(DirectoryNotEmptyError) as exc_info:
            await file_handler.delete_directory(non_empty_dir, recursive=False)

        assert exc_info.value.status_code == 409

    async def test_delete_directory_not_found_returns_false(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test deleting non-existent directory returns False."""
        # Arrange
        non_existent = tmp_path / "does_not_exist"

        # Act
        result = await file_handler.delete_directory(non_existent)

        # Assert
        assert result is False

    async def test_directory_exists_returns_true(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test directory_exists returns True for existing directory."""
        # Arrange
        test_dir = tmp_path / "existing_dir"
        test_dir.mkdir()

        # Act
        result = await file_handler.directory_exists(test_dir)

        # Assert
        assert result is True

    async def test_directory_exists_returns_false(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test directory_exists returns False for non-existent directory."""
        # Arrange
        non_existent = tmp_path / "does_not_exist"

        # Act
        result = await file_handler.directory_exists(non_existent)

        # Assert
        assert result is False

    async def test_directory_exists_returns_false_for_file(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test directory_exists returns False for a file."""
        # Arrange
        test_file = tmp_path / "a_file.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act
        result = await file_handler.directory_exists(test_file)

        # Assert
        assert result is False


# =============================================================================
# File Info Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerInfo:
    """Test suite for FileHandler file info operations."""

    async def test_get_file_info(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test getting file information."""
        # Arrange
        test_file = tmp_path / "info_test.txt"
        content = "Test content for info"
        test_file.write_text(content, encoding="utf-8")

        # Act
        info = await file_handler.get_file_info(test_file)

        # Assert
        assert isinstance(info, FileInfo)
        assert info.path == test_file
        assert info.size == len(content.encode("utf-8"))
        assert info.is_file is True
        assert info.is_directory is False
        assert isinstance(info.created_at, datetime)
        assert isinstance(info.modified_at, datetime)

    async def test_get_directory_info(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test getting directory information."""
        # Arrange
        test_dir = tmp_path / "info_dir"
        test_dir.mkdir()

        # Act
        info = await file_handler.get_file_info(test_dir)

        # Assert
        assert isinstance(info, FileInfo)
        assert info.path == test_dir
        assert info.is_file is False
        assert info.is_directory is True

    async def test_get_file_info_not_found_raises_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test getting info for non-existent path raises AppFileNotFoundError."""
        # Arrange
        non_existent = tmp_path / "does_not_exist.txt"

        # Act & Assert
        with pytest.raises(AppFileNotFoundError) as exc_info:
            await file_handler.get_file_info(non_existent)

        assert exc_info.value.status_code == 404


# =============================================================================
# File Locking Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerLocking:
    """Test suite for FileHandler file locking operations."""

    async def test_acquire_and_release_lock(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test acquiring and releasing a file lock."""
        # Arrange
        test_file = tmp_path / "lockable.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act
        lock = await file_handler.acquire_lock(test_file)

        # Assert
        assert isinstance(lock, FileLock)
        assert lock.path == test_file
        assert isinstance(lock.acquired_at, datetime)

        # Cleanup
        await file_handler.release_lock(lock)

    async def test_lock_context_manager(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test using file lock as context manager."""
        # Arrange
        test_file = tmp_path / "context_lock.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act & Assert
        async with file_handler.locked(test_file) as lock:
            assert isinstance(lock, FileLock)
            assert lock.path == test_file

        # Lock should be released after context

    async def test_lock_timeout(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test lock acquisition timeout."""
        # Arrange
        test_file = tmp_path / "timeout_lock.txt"
        test_file.write_text("content", encoding="utf-8")

        # Acquire first lock
        lock1 = await file_handler.acquire_lock(test_file)

        # Act & Assert - try to acquire second lock with short timeout
        with pytest.raises(FileLockError) as exc_info:
            await file_handler.acquire_lock(test_file, timeout=0.1)

        assert exc_info.value.status_code == 409
        assert "lock" in exc_info.value.message.lower()

        # Cleanup
        await file_handler.release_lock(lock1)

    async def test_lock_for_non_existent_file_creates_lock(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test acquiring lock for non-existent file creates lock file."""
        # Arrange
        test_file = tmp_path / "non_existent_for_lock.txt"

        # Act
        lock = await file_handler.acquire_lock(test_file)

        # Assert
        assert isinstance(lock, FileLock)
        assert lock.path == test_file

        # Cleanup
        await file_handler.release_lock(lock)

    async def test_release_lock_idempotent(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test releasing an already released lock does not raise error."""
        # Arrange
        test_file = tmp_path / "idempotent_lock.txt"
        test_file.write_text("content", encoding="utf-8")
        lock = await file_handler.acquire_lock(test_file)
        await file_handler.release_lock(lock)

        # Act & Assert (should not raise)
        await file_handler.release_lock(lock)

    async def test_lock_released_on_exception(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that lock is released when exception occurs in context manager."""
        # Arrange
        test_file = tmp_path / "exception_lock.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act - Exception should not prevent lock release
        with pytest.raises(ValueError):
            async with file_handler.locked(test_file) as lock:
                assert isinstance(lock, FileLock)
                raise ValueError("Test exception")

        # Assert - Lock should be released, allowing new acquisition
        new_lock = await file_handler.acquire_lock(test_file, timeout=0.1)
        assert isinstance(new_lock, FileLock)
        await file_handler.release_lock(new_lock)

    async def test_lock_zero_timeout(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test lock acquisition with zero timeout fails immediately if locked."""
        # Arrange
        test_file = tmp_path / "zero_timeout.txt"
        test_file.write_text("content", encoding="utf-8")

        # Acquire first lock
        lock1 = await file_handler.acquire_lock(test_file)

        # Act & Assert - Try with zero timeout, should fail immediately
        with pytest.raises(FileLockError) as exc_info:
            await file_handler.acquire_lock(test_file, timeout=0.0)

        assert "timeout" in exc_info.value.message.lower()
        assert exc_info.value.details["timeout"] == 0.0

        # Cleanup
        await file_handler.release_lock(lock1)


# =============================================================================
# Error Handling Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerErrors:
    """Test suite for FileHandler error handling."""

    async def test_file_operation_error_has_correct_attributes(self) -> None:
        """Test FileOperationError has correct attributes."""
        # Act
        error = FileOperationError("Test error", details={"path": "/test"})

        # Assert
        assert error.message == "Test error"
        assert error.status_code == 500
        assert error.error_type == "FILE_OPERATION_ERROR"
        assert error.details == {"path": "/test"}

    async def test_file_not_found_error_has_correct_attributes(self) -> None:
        """Test AppFileNotFoundError has correct attributes."""
        # Act
        error = AppFileNotFoundError("File not found: /test/path")

        # Assert
        assert error.status_code == 404
        assert error.error_type == "FILE_NOT_FOUND"

    async def test_file_access_error_has_correct_attributes(self) -> None:
        """Test FileAccessError has correct attributes."""
        # Act
        error = FileAccessError("Access denied: /test/path")

        # Assert
        assert error.status_code == 403
        assert error.error_type == "FILE_ACCESS_DENIED"

    async def test_file_lock_error_has_correct_attributes(self) -> None:
        """Test FileLockError has correct attributes."""
        # Act
        error = FileLockError("Lock failed: /test/path")

        # Assert
        assert error.status_code == 409
        assert error.error_type == "FILE_LOCK_ERROR"

    async def test_directory_not_found_error_has_correct_attributes(self) -> None:
        """Test DirectoryNotFoundError has correct attributes."""
        # Act
        error = DirectoryNotFoundError("Directory not found: /test/dir")

        # Assert
        assert error.status_code == 404
        assert error.error_type == "DIRECTORY_NOT_FOUND"

    async def test_directory_not_empty_error_has_correct_attributes(self) -> None:
        """Test DirectoryNotEmptyError has correct attributes."""
        # Act
        error = DirectoryNotEmptyError("Directory not empty: /test/dir")

        # Assert
        assert error.status_code == 409
        assert error.error_type == "DIRECTORY_NOT_EMPTY"


# =============================================================================
# Exception Path Tests (using mocking)
# =============================================================================


@pytest.mark.unit
class TestFileHandlerExceptionPaths:
    """Test suite for FileHandler exception handling paths."""

    async def test_read_file_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test read_file raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_test.txt"
        test_file.write_text("content", encoding="utf-8")

        # Mock aiofiles.open to raise PermissionError
        with patch("aiofiles.open", side_effect=PermissionError("Access denied")):
            # Act & Assert
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.read_file(test_file)

            assert "Permission denied" in exc_info.value.message

    async def test_read_file_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test read_file raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_test.txt"
        test_file.write_text("content", encoding="utf-8")

        # Mock aiofiles.open to raise OSError
        with patch("aiofiles.open", side_effect=OSError("I/O error")):
            # Act & Assert
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.read_file(test_file)

            assert "Error reading file" in exc_info.value.message

    async def test_read_bytes_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test read_bytes raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_bytes.bin"
        test_file.write_bytes(b"content")

        with patch("aiofiles.open", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.read_bytes(test_file)

    async def test_read_bytes_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test read_bytes raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_bytes.bin"
        test_file.write_bytes(b"content")

        with patch("aiofiles.open", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.read_bytes(test_file)

    async def test_write_file_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test write_file raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_write.txt"

        with patch("aiofiles.open", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.write_file(test_file, "content")

    async def test_write_file_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test write_file raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_write.txt"

        with patch("aiofiles.open", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.write_file(test_file, "content")

    async def test_write_bytes_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test write_bytes raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_write_bytes.bin"

        with patch("aiofiles.open", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.write_bytes(test_file, b"content")

    async def test_write_bytes_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test write_bytes raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_write_bytes.bin"

        with patch("aiofiles.open", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.write_bytes(test_file, b"content")

    async def test_delete_file_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_file raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_delete.txt"
        test_file.write_text("content", encoding="utf-8")

        with patch.object(Path, "unlink", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.delete_file(test_file)

    async def test_delete_file_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_file raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_delete.txt"
        test_file.write_text("content", encoding="utf-8")

        with patch.object(Path, "unlink", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.delete_file(test_file)

    async def test_create_directory_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test create_directory raises FileAccessError on permission error."""
        # Arrange
        test_dir = tmp_path / "permission_mkdir"

        with patch.object(Path, "mkdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.create_directory(test_dir)

    async def test_create_directory_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test create_directory raises FileOperationError on OS error."""
        # Arrange
        test_dir = tmp_path / "os_error_mkdir"

        with patch.object(Path, "mkdir", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.create_directory(test_dir)

    async def test_list_directory_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test list_directory raises FileAccessError on permission error."""
        # Arrange
        test_dir = tmp_path / "permission_list"
        test_dir.mkdir()

        with patch.object(Path, "glob", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.list_directory(test_dir)

    async def test_list_directory_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test list_directory raises FileOperationError on OS error."""
        # Arrange
        test_dir = tmp_path / "os_error_list"
        test_dir.mkdir()

        with patch.object(Path, "glob", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.list_directory(test_dir)

    async def test_list_directory_file_not_directory(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test list_directory raises DirectoryNotFoundError for a file."""
        # Arrange
        test_file = tmp_path / "not_a_directory.txt"
        test_file.write_text("content", encoding="utf-8")

        with pytest.raises(DirectoryNotFoundError) as exc_info:
            await file_handler.list_directory(test_file)

        assert "not a directory" in exc_info.value.message.lower()

    async def test_delete_directory_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_directory raises FileAccessError on permission error."""
        # Arrange
        test_dir = tmp_path / "permission_rmdir"
        test_dir.mkdir()

        with patch.object(Path, "rmdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.delete_directory(test_dir)

    async def test_delete_directory_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_directory raises FileOperationError on OS error."""
        # Arrange
        test_dir = tmp_path / "os_error_rmdir"
        test_dir.mkdir()

        with patch.object(Path, "rmdir", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.delete_directory(test_dir)

    async def test_get_file_info_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test get_file_info raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "permission_info.txt"
        test_file.write_text("content", encoding="utf-8")

        with patch.object(Path, "stat", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError):
                await file_handler.get_file_info(test_file)

    async def test_get_file_info_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test get_file_info raises FileOperationError on OS error."""
        # Arrange
        test_file = tmp_path / "os_error_info.txt"
        test_file.write_text("content", encoding="utf-8")

        with patch.object(Path, "stat", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError):
                await file_handler.get_file_info(test_file)


# =============================================================================
# FileInfo Validation Tests
# =============================================================================


@pytest.mark.unit
class TestFileInfoValidation:
    """Test suite for FileInfo dataclass validation."""

    def test_fileinfo_cannot_be_both_file_and_directory(self) -> None:
        """Test that FileInfo raises ValueError when both is_file and is_directory are True."""
        from datetime import datetime, timezone

        with pytest.raises(ValueError) as exc_info:
            FileInfo(
                path=Path("/test"),
                size=100,
                created_at=datetime.now(timezone.utc),
                modified_at=datetime.now(timezone.utc),
                is_file=True,
                is_directory=True,
            )

        assert "cannot be both a file and a directory" in str(exc_info.value)

    def test_fileinfo_can_be_file_only(self) -> None:
        """Test that FileInfo accepts is_file=True, is_directory=False."""
        from datetime import datetime, timezone

        info = FileInfo(
            path=Path("/test.txt"),
            size=100,
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
            is_file=True,
            is_directory=False,
        )
        assert info.is_file is True
        assert info.is_directory is False

    def test_fileinfo_can_be_directory_only(self) -> None:
        """Test that FileInfo accepts is_file=False, is_directory=True."""
        from datetime import datetime, timezone

        info = FileInfo(
            path=Path("/test_dir"),
            size=0,
            created_at=datetime.now(timezone.utc),
            modified_at=datetime.now(timezone.utc),
            is_file=False,
            is_directory=True,
        )
        assert info.is_file is False
        assert info.is_directory is True


# =============================================================================
# Copy and Move File Tests
# =============================================================================


@pytest.mark.unit
class TestFileHandlerCopyMoveOperations:
    """Test suite for FileHandler copy and move operations."""

    async def test_copy_file_success(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test successful file copy."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        content = "Content to copy"
        source.write_text(content, encoding="utf-8")

        # Act
        await file_handler.copy_file(source, destination)

        # Assert
        assert destination.exists()
        assert destination.read_text(encoding="utf-8") == content
        assert source.exists()  # Source should still exist

    async def test_copy_file_creates_parent_directories(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that copy_file creates parent directories."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "dir" / "destination.txt"
        content = "Content to copy"
        source.write_text(content, encoding="utf-8")

        # Act
        await file_handler.copy_file(source, destination)

        # Assert
        assert destination.exists()
        assert destination.read_text(encoding="utf-8") == content

    async def test_copy_file_source_not_found(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test copy_file raises error when source doesn't exist."""
        # Arrange
        source = tmp_path / "nonexistent.txt"
        destination = tmp_path / "destination.txt"

        # Act & Assert
        with pytest.raises(AppFileNotFoundError) as exc_info:
            await file_handler.copy_file(source, destination)

        assert "Source file not found" in exc_info.value.message

    async def test_move_file_success(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test successful file move."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        content = "Content to move"
        source.write_text(content, encoding="utf-8")

        # Act
        await file_handler.move_file(source, destination)

        # Assert
        assert destination.exists()
        assert destination.read_text(encoding="utf-8") == content
        assert not source.exists()  # Source should be gone

    async def test_move_file_creates_parent_directories(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that move_file creates parent directories."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "dir" / "destination.txt"
        content = "Content to move"
        source.write_text(content, encoding="utf-8")

        # Act
        await file_handler.move_file(source, destination)

        # Assert
        assert destination.exists()
        assert destination.read_text(encoding="utf-8") == content
        assert not source.exists()

    async def test_move_file_source_not_found(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test move_file raises error when source doesn't exist."""
        # Arrange
        source = tmp_path / "nonexistent.txt"
        destination = tmp_path / "destination.txt"

        # Act & Assert
        with pytest.raises(AppFileNotFoundError) as exc_info:
            await file_handler.move_file(source, destination)

        assert "Source file not found" in exc_info.value.message


# =============================================================================
# Glob Pattern Validation Tests
# =============================================================================


@pytest.mark.unit
class TestGlobPatternValidation:
    """Test suite for glob pattern validation."""

    async def test_glob_pattern_with_parent_traversal_rejected(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that glob patterns with '..' are rejected."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await file_handler.list_directory(test_dir, pattern="../*")

        assert "cannot contain '..'" in str(exc_info.value)

    async def test_glob_pattern_with_embedded_parent_traversal_rejected(
        self, tmp_path: Path, file_handler: FileHandler
    ) -> None:
        """Test that glob patterns with embedded '..' are rejected."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await file_handler.list_directory(test_dir, pattern="subdir/../*.txt")

        assert "cannot contain '..'" in str(exc_info.value)

    async def test_valid_glob_patterns_accepted(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that valid glob patterns work correctly."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content", encoding="utf-8")
        (test_dir / "file2.txt").write_text("content", encoding="utf-8")
        (test_dir / "data.json").write_text("{}", encoding="utf-8")

        # Act & Assert - Various valid patterns
        txt_files = await file_handler.list_directory(test_dir, pattern="*.txt")
        assert len(txt_files) == 2

        all_files = await file_handler.list_directory(test_dir, pattern="*")
        assert len(all_files) == 3

        file1_only = await file_handler.list_directory(test_dir, pattern="file1.*")
        assert len(file1_only) == 1

    async def test_glob_pattern_with_absolute_path_rejected(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that glob patterns starting with '/' are rejected."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await file_handler.list_directory(test_dir, pattern="/etc/passwd")

        assert "absolute path" in str(exc_info.value)

    async def test_glob_pattern_with_drive_letter_rejected(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that glob patterns with Windows drive letters are rejected."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await file_handler.list_directory(test_dir, pattern="C:\\Windows\\*")

        assert "drive letters" in str(exc_info.value)

    async def test_empty_glob_pattern_raises_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that empty glob pattern raises an error from pathlib.glob."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content", encoding="utf-8")

        # Act & Assert - Empty pattern is invalid for pathlib.glob in Python 3.14+
        # Earlier versions might behave differently, but current Python raises ValueError
        with pytest.raises((ValueError, FileOperationError)):
            await file_handler.list_directory(test_dir, pattern="")


# =============================================================================
# Copy and Move Permission Error Tests
# =============================================================================


@pytest.mark.unit
class TestCopyMovePermissionErrors:
    """Test suite for copy and move permission error handling."""

    async def test_copy_file_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test copy_file raises FileAccessError on permission error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch("shutil.copy2", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.copy_file(source, destination)

            assert "Permission denied" in exc_info.value.message

    async def test_copy_file_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test copy_file raises FileOperationError on OS error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch("shutil.copy2", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.copy_file(source, destination)

            assert "Error copying file" in exc_info.value.message

    async def test_move_file_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test move_file raises FileAccessError on permission error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch("shutil.move", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.move_file(source, destination)

            assert "Permission denied" in exc_info.value.message

    async def test_move_file_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test move_file raises FileOperationError on OS error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch("shutil.move", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.move_file(source, destination)

            assert "Error moving file" in exc_info.value.message

    async def test_copy_file_mkdir_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test copy_file raises FileAccessError when mkdir fails with permission error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch.object(Path, "mkdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.copy_file(source, destination)

            assert "Permission denied creating destination directory" in exc_info.value.message

    async def test_copy_file_mkdir_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test copy_file raises FileOperationError when mkdir fails with OS error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch.object(Path, "mkdir", side_effect=OSError("Disk full")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.copy_file(source, destination)

            assert "Error creating destination directory" in exc_info.value.message

    async def test_move_file_mkdir_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test move_file raises FileAccessError when mkdir fails with permission error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch.object(Path, "mkdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.move_file(source, destination)

            assert "Permission denied creating destination directory" in exc_info.value.message

    async def test_move_file_mkdir_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test move_file raises FileOperationError when mkdir fails with OS error."""
        # Arrange
        source = tmp_path / "source.txt"
        destination = tmp_path / "nested" / "destination.txt"
        source.write_text("content", encoding="utf-8")

        with patch.object(Path, "mkdir", side_effect=OSError("Disk full")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.move_file(source, destination)

            assert "Error creating destination directory" in exc_info.value.message


# =============================================================================
# Recursive Delete Permission Error Tests
# =============================================================================


@pytest.mark.unit
class TestRecursiveDeletePermissionErrors:
    """Test suite for recursive delete permission error handling."""

    async def test_delete_directory_recursive_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_directory with recursive=True raises FileAccessError on permission error."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content", encoding="utf-8")

        with patch("shutil.rmtree", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.delete_directory(test_dir, recursive=True)

            assert "Permission denied" in exc_info.value.message

    async def test_delete_directory_recursive_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test delete_directory with recursive=True raises FileOperationError on OS error."""
        # Arrange
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "file.txt").write_text("content", encoding="utf-8")

        with patch("shutil.rmtree", side_effect=OSError("I/O error")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.delete_directory(test_dir, recursive=True)

            assert "Error deleting directory" in exc_info.value.message


# =============================================================================
# UnicodeDecodeError Tests
# =============================================================================


@pytest.mark.unit
class TestUnicodeDecodeError:
    """Test suite for UnicodeDecodeError handling."""

    async def test_read_file_unicode_decode_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test read_file raises FileOperationError for non-UTF-8 files."""
        # Arrange - Create a file with invalid UTF-8 bytes
        test_file = tmp_path / "invalid_utf8.txt"
        # Write bytes that are invalid UTF-8 (0xFF 0xFE is not valid UTF-8)
        test_file.write_bytes(b"\xff\xfe\x00\x01")

        # Act & Assert
        with pytest.raises(FileOperationError) as exc_info:
            await file_handler.read_file(test_file)

        assert "not valid UTF-8" in exc_info.value.message
        assert "encoding" in exc_info.value.details


# =============================================================================
# FileInfo Invalid State Tests
# =============================================================================


@pytest.mark.unit
class TestFileInfoInvalidState:
    """Test suite for FileInfo invalid state validation."""

    def test_fileinfo_cannot_be_neither_file_nor_directory(self) -> None:
        """Test that FileInfo raises ValueError when both is_file and is_directory are False."""
        from datetime import datetime, timezone

        with pytest.raises(ValueError) as exc_info:
            FileInfo(
                path=Path("/test"),
                size=100,
                created_at=datetime.now(timezone.utc),
                modified_at=datetime.now(timezone.utc),
                is_file=False,
                is_directory=False,
            )

        assert "must be either a file or a directory" in str(exc_info.value)


# =============================================================================
# FileLock Computed Property Tests
# =============================================================================


@pytest.mark.unit
class TestFileLockComputedProperty:
    """Test suite for FileLock computed lock_file property."""

    def test_lock_file_is_computed_from_path(self) -> None:
        """Test that lock_file is correctly computed from path."""
        from datetime import datetime, timezone

        lock = FileLock(
            path=Path("/some/dir/myfile.txt"),
            acquired_at=datetime.now(timezone.utc),
        )

        assert lock.lock_file == Path("/some/dir/.myfile.txt.lock")

    def test_lock_file_computation_consistent(self) -> None:
        """Test that lock_file computation is consistent across calls."""
        from datetime import datetime, timezone

        lock = FileLock(
            path=Path("/test/file.yaml"),
            acquired_at=datetime.now(timezone.utc),
        )

        # Multiple calls should return the same value
        assert lock.lock_file == lock.lock_file
        assert str(lock.lock_file).endswith(".file.yaml.lock")


# =============================================================================
# Lock Acquisition Error Tests
# =============================================================================


@pytest.mark.unit
class TestLockAcquisitionErrors:
    """Test suite for lock acquisition error handling."""

    async def test_acquire_lock_permission_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test acquire_lock raises FileAccessError on permission error."""
        # Arrange
        test_file = tmp_path / "lockable.txt"
        test_file.write_text("content", encoding="utf-8")

        import os

        with patch.object(os, "open", side_effect=PermissionError("Access denied")):
            with pytest.raises(FileAccessError) as exc_info:
                await file_handler.acquire_lock(test_file)

            assert "Permission denied" in exc_info.value.message

    async def test_acquire_lock_os_error(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test acquire_lock raises FileOperationError on unexpected OS error."""
        # Arrange
        test_file = tmp_path / "lockable.txt"
        test_file.write_text("content", encoding="utf-8")

        import os

        with patch.object(os, "open", side_effect=OSError("Disk full")):
            with pytest.raises(FileOperationError) as exc_info:
                await file_handler.acquire_lock(test_file)

            assert "Error creating lock file" in exc_info.value.message


# =============================================================================
# Negative Timeout Tests
# =============================================================================


@pytest.mark.unit
class TestNegativeTimeout:
    """Test suite for negative timeout handling."""

    async def test_lock_with_negative_timeout(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test lock acquisition with negative timeout fails immediately if locked."""
        # Arrange
        test_file = tmp_path / "negative_timeout.txt"
        test_file.write_text("content", encoding="utf-8")

        # Acquire first lock
        lock1 = await file_handler.acquire_lock(test_file)

        # Act & Assert - Negative timeout should fail immediately
        with pytest.raises(FileLockError) as exc_info:
            await file_handler.acquire_lock(test_file, timeout=-1.0)

        assert "Timeout" in exc_info.value.message
        assert exc_info.value.details["timeout"] == -1.0

        # Cleanup
        await file_handler.release_lock(lock1)
