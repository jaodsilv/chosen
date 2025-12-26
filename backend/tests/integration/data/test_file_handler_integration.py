"""Integration tests for FileHandler class.

This module contains integration tests that verify FileHandler operations
with real filesystem interactions, including:
    - Full file lifecycle (create, read, update, delete)
    - Concurrent access with file locking
    - Large file handling
    - Directory operations with real filesystem
"""

import asyncio
from pathlib import Path
from typing import List

import pytest

from app.core.exceptions import FileLockError
from app.data.file_handler import FileHandler, FileLock

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def file_handler() -> FileHandler:
    """Create a FileHandler instance for testing."""
    return FileHandler()


@pytest.fixture
def large_content() -> str:
    """Provide large content for testing large file operations."""
    # Generate ~1MB of content
    line = "This is a test line with some content for large file testing.\n"
    return line * 20000  # Approximately 1.2MB


# =============================================================================
# Full Lifecycle Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerFullLifecycle:
    """Integration tests for complete file lifecycle operations."""

    async def test_full_file_lifecycle(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test complete file lifecycle: create, read, update, delete."""
        # Arrange
        test_file = tmp_path / "lifecycle.txt"
        initial_content = "Initial content"
        updated_content = "Updated content"

        # Act & Assert - Create
        await file_handler.write_file(test_file, initial_content)
        assert await file_handler.file_exists(test_file)

        # Act & Assert - Read
        content = await file_handler.read_file(test_file)
        assert content == initial_content

        # Act & Assert - Get info
        info = await file_handler.get_file_info(test_file)
        assert info.is_file is True
        assert info.size == len(initial_content.encode("utf-8"))

        # Act & Assert - Update
        await file_handler.write_file(test_file, updated_content)
        content = await file_handler.read_file(test_file)
        assert content == updated_content

        # Act & Assert - Delete
        result = await file_handler.delete_file(test_file)
        assert result is True
        assert not await file_handler.file_exists(test_file)

    async def test_full_directory_lifecycle(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test complete directory lifecycle: create, list, delete."""
        # Arrange
        test_dir = tmp_path / "lifecycle_dir"

        # Act & Assert - Create directory
        await file_handler.create_directory(test_dir)
        assert await file_handler.directory_exists(test_dir)

        # Act & Assert - Create files in directory
        for i in range(5):
            file_path = test_dir / f"file_{i}.txt"
            await file_handler.write_file(file_path, f"Content {i}")

        # Act & Assert - List directory
        contents = await file_handler.list_directory(test_dir)
        assert len(contents) == 5

        # Act & Assert - Get directory info
        info = await file_handler.get_file_info(test_dir)
        assert info.is_directory is True

        # Act & Assert - Delete directory
        result = await file_handler.delete_directory(test_dir, recursive=True)
        assert result is True
        assert not await file_handler.directory_exists(test_dir)

    async def test_nested_directory_operations(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test operations with deeply nested directories."""
        # Arrange
        nested_path = tmp_path / "level1" / "level2" / "level3" / "level4"
        file_path = nested_path / "deep_file.txt"
        content = "Content in deeply nested file"

        # Act - Create nested structure
        await file_handler.write_file(file_path, content)

        # Assert - Verify structure
        assert await file_handler.directory_exists(nested_path)
        assert await file_handler.file_exists(file_path)
        assert await file_handler.read_file(file_path) == content

        # Cleanup
        await file_handler.delete_directory(tmp_path / "level1", recursive=True)


# =============================================================================
# Concurrent Access Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerConcurrentAccess:
    """Integration tests for concurrent file access with locking."""

    async def test_concurrent_writes_with_locking(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that file locking prevents concurrent write conflicts."""
        # Arrange
        test_file = tmp_path / "concurrent.txt"
        await file_handler.write_file(test_file, "initial")
        results: List[str] = []

        async def write_with_lock(value: str) -> None:
            async with file_handler.locked(test_file):
                # Read current content
                current = await file_handler.read_file(test_file)
                # Simulate some processing
                await asyncio.sleep(0.05)
                # Write new content
                await file_handler.write_file(test_file, f"{current},{value}")
                results.append(value)

        # Act - Run concurrent writes
        await asyncio.gather(
            write_with_lock("A"),
            write_with_lock("B"),
            write_with_lock("C"),
        )

        # Assert - All writes completed successfully
        final_content = await file_handler.read_file(test_file)
        assert len(results) == 3
        # Content should contain all values (order may vary due to locking)
        for value in ["A", "B", "C"]:
            assert value in final_content

    async def test_lock_prevents_concurrent_access(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that second lock acquisition fails while first is held."""
        # Arrange
        test_file = tmp_path / "lock_test.txt"
        await file_handler.write_file(test_file, "content")

        lock_acquired = asyncio.Event()
        lock_released = asyncio.Event()
        second_lock_attempted = asyncio.Event()
        second_lock_failed = asyncio.Event()

        async def hold_lock() -> None:
            async with file_handler.locked(test_file):
                lock_acquired.set()
                # Wait for second lock attempt to be made
                await second_lock_attempted.wait()
                # Give some time for the second lock to timeout
                await asyncio.sleep(0.2)
            lock_released.set()

        async def attempt_second_lock() -> None:
            # Wait for first lock to be acquired
            await lock_acquired.wait()
            second_lock_attempted.set()
            try:
                # Try to acquire with short timeout
                await file_handler.acquire_lock(test_file, timeout=0.1)
            except Exception:
                second_lock_failed.set()

        # Act
        await asyncio.gather(
            hold_lock(),
            attempt_second_lock(),
        )

        # Assert
        assert second_lock_failed.is_set()

    async def test_lock_released_allows_new_lock(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that releasing a lock allows another lock to be acquired."""
        # Arrange
        test_file = tmp_path / "release_test.txt"
        await file_handler.write_file(test_file, "content")

        # Act - Acquire and release first lock
        lock1 = await file_handler.acquire_lock(test_file)
        await file_handler.release_lock(lock1)

        # Assert - Second lock should succeed
        lock2 = await file_handler.acquire_lock(test_file)
        assert isinstance(lock2, FileLock)
        await file_handler.release_lock(lock2)


# =============================================================================
# Large File Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerLargeFiles:
    """Integration tests for large file operations."""

    async def test_large_file_write_and_read(
        self, tmp_path: Path, file_handler: FileHandler, large_content: str
    ) -> None:
        """Test writing and reading large files."""
        # Arrange
        large_file = tmp_path / "large_file.txt"

        # Act - Write large file
        await file_handler.write_file(large_file, large_content)

        # Assert - Read back and verify
        read_content = await file_handler.read_file(large_file)
        assert read_content == large_content

        # Verify file info - Note: file size may differ from in-memory size
        # due to platform-specific line endings (CRLF on Windows)
        info = await file_handler.get_file_info(large_file)
        assert info.size > 0
        assert info.is_file is True

    async def test_large_binary_file(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test writing and reading large binary files."""
        # Arrange
        large_binary = tmp_path / "large_binary.bin"
        # Generate ~500KB of binary data
        binary_content = bytes(range(256)) * 2000

        # Act
        await file_handler.write_bytes(large_binary, binary_content)
        read_content = await file_handler.read_bytes(large_binary)

        # Assert
        assert read_content == binary_content


# =============================================================================
# Directory Pattern Matching Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerPatternMatching:
    """Integration tests for directory listing with patterns."""

    async def test_list_with_various_patterns(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test listing directory with various glob patterns."""
        # Arrange - Create files with different extensions
        extensions = ["txt", "yaml", "json", "md", "py"]
        for ext in extensions:
            for i in range(3):
                file_path = tmp_path / f"file_{i}.{ext}"
                await file_handler.write_file(file_path, f"content for {ext}")

        # Act & Assert - Test different patterns
        txt_files = await file_handler.list_directory(tmp_path, pattern="*.txt")
        assert len(txt_files) == 3

        yaml_files = await file_handler.list_directory(tmp_path, pattern="*.yaml")
        assert len(yaml_files) == 3

        all_files = await file_handler.list_directory(tmp_path, pattern="*")
        assert len(all_files) == 15

        file_0_files = await file_handler.list_directory(tmp_path, pattern="file_0.*")
        assert len(file_0_files) == 5

    async def test_recursive_directory_listing(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test that list_directory only lists immediate children."""
        # Arrange
        (tmp_path / "file1.txt").write_text("content", encoding="utf-8")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").write_text("content", encoding="utf-8")

        # Act
        contents = await file_handler.list_directory(tmp_path)

        # Assert - Should only show immediate children
        names = [p.name for p in contents]
        assert "file1.txt" in names
        assert "subdir" in names
        assert "file2.txt" not in names  # Should not include nested files
        assert len(contents) == 2


# =============================================================================
# Edge Cases Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerEdgeCases:
    """Integration tests for edge cases and boundary conditions."""

    async def test_special_characters_in_filename(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test handling files with special characters in name."""
        # Arrange - Use characters that are valid on most filesystems
        special_name = tmp_path / "file-with_special.chars (1).txt"
        content = "Content with special filename"

        # Act
        await file_handler.write_file(special_name, content)
        read_content = await file_handler.read_file(special_name)

        # Assert
        assert read_content == content

    async def test_unicode_in_filename(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test handling files with Unicode characters in name."""
        # Arrange
        unicode_name = tmp_path / "файл_测试_αβγ.txt"
        content = "Content with unicode filename"

        # Act
        await file_handler.write_file(unicode_name, content)
        read_content = await file_handler.read_file(unicode_name)

        # Assert
        assert read_content == content

    async def test_very_long_content_single_line(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test handling very long single-line content."""
        # Arrange
        long_line = "x" * 100000  # 100KB single line
        test_file = tmp_path / "long_line.txt"

        # Act
        await file_handler.write_file(test_file, long_line)
        read_content = await file_handler.read_file(test_file)

        # Assert
        assert read_content == long_line
        assert len(read_content) == 100000

    async def test_file_with_only_whitespace(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test handling file with only whitespace content."""
        # Arrange
        whitespace_content = "   \n\t\n   \n"
        test_file = tmp_path / "whitespace.txt"

        # Act
        await file_handler.write_file(test_file, whitespace_content)
        read_content = await file_handler.read_file(test_file)

        # Assert
        assert read_content == whitespace_content

    async def test_multiple_sequential_operations(self, tmp_path: Path, file_handler: FileHandler) -> None:
        """Test many sequential file operations."""
        # Arrange
        test_dir = tmp_path / "sequential"
        await file_handler.create_directory(test_dir)

        # Act - Perform many operations
        for i in range(50):
            file_path = test_dir / f"file_{i}.txt"
            content = f"Content for file {i}"
            await file_handler.write_file(file_path, content)
            read_content = await file_handler.read_file(file_path)
            assert read_content == content

        # Assert - All files exist
        contents = await file_handler.list_directory(test_dir)
        assert len(contents) == 50

        # Cleanup
        await file_handler.delete_directory(test_dir, recursive=True)


# =============================================================================
# Cross-Instance Locking Tests
# =============================================================================


@pytest.mark.integration
class TestFileHandlerCrossInstanceLocking:
    """Integration tests for locking behavior across FileHandler instances."""

    async def test_concurrent_locking_across_instances(self, tmp_path: Path) -> None:
        """Test that locks work across separate FileHandler instances."""
        # Arrange - Create two independent FileHandler instances
        handler1 = FileHandler()
        handler2 = FileHandler()
        test_file = tmp_path / "shared.txt"
        test_file.write_text("content", encoding="utf-8")

        # Act - Acquire lock with first handler
        lock1 = await handler1.acquire_lock(test_file)

        # Assert - Second handler cannot acquire lock
        with pytest.raises(FileLockError) as exc_info:
            await handler2.acquire_lock(test_file, timeout=0.1)

        assert "Timeout acquiring lock" in str(exc_info.value.message)
        assert exc_info.value.details["lock_file_exists"] is True

        # Cleanup - Release lock
        await handler1.release_lock(lock1)

        # After release, second handler should be able to acquire
        lock2 = await handler2.acquire_lock(test_file, timeout=0.1)
        assert isinstance(lock2, FileLock)
        await handler2.release_lock(lock2)

    async def test_orphaned_lock_file_handling(self, tmp_path: Path) -> None:
        """Test behavior when encountering orphaned lock files.

        This test verifies that the current implementation correctly times out
        when an orphaned lock file exists. Stale lock detection (via PID tracking
        or timestamps) is not yet implemented.
        """
        # Arrange
        file_handler = FileHandler()
        test_file = tmp_path / "orphaned.txt"
        test_file.write_text("content", encoding="utf-8")

        # Manually create orphaned lock file (simulates crashed process)
        lock_file = tmp_path / ".orphaned.txt.lock"
        lock_file.write_text("orphaned", encoding="utf-8")

        # Act & Assert - Should timeout since lock file exists
        # (until stale detection is implemented)
        with pytest.raises(FileLockError) as exc_info:
            await file_handler.acquire_lock(test_file, timeout=0.1)

        assert "Timeout acquiring lock" in str(exc_info.value.message)
        assert exc_info.value.details["lock_file_exists"] is True

        # Cleanup - Remove orphaned lock file
        lock_file.unlink()
