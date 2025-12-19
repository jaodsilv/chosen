"""FileHandler for file system operations.

This module provides a comprehensive file handler class that supports:
    - File read/write operations with UTF-8 encoding
    - Directory operations (create, list, delete)
    - File locking for concurrency safety
    - Async operations for non-blocking I/O
    - Comprehensive error handling

Example:
    >>> handler = FileHandler()
    >>> await handler.write_file(Path("test.txt"), "Hello, World!")
    >>> content = await handler.read_file(Path("test.txt"))
    >>> print(content)
    Hello, World!
"""

import asyncio
import os
import shutil
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator, List

from app.core.exceptions import (
    DirectoryNotEmptyError,
    DirectoryNotFoundError,
    FileAccessError,
    FileLockError,
    FileNotFoundError,
    FileOperationError,
)


@dataclass
class FileInfo:
    """Information about a file or directory.

    Attributes:
        path: The path to the file or directory.
        size: The size in bytes (0 for directories).
        created_at: When the file was created.
        modified_at: When the file was last modified.
        is_file: Whether this is a regular file.
        is_directory: Whether this is a directory.
    """

    path: Path
    size: int
    created_at: datetime
    modified_at: datetime
    is_file: bool
    is_directory: bool


@dataclass
class FileLock:
    """Represents an acquired file lock.

    Attributes:
        path: The path to the locked file.
        acquired_at: When the lock was acquired.
        lock_file: Path to the lock file.
    """

    path: Path
    acquired_at: datetime
    lock_file: Path


class FileHandler:
    """Handles file system operations with async support and file locking.

    This class provides methods for:
        - Reading and writing text and binary files
        - Creating, listing, and deleting directories
        - File locking for safe concurrent access
        - Getting file information and metadata

    All file operations are performed with UTF-8 encoding by default.
    Async operations use asyncio.to_thread for non-blocking I/O.

    Example:
        >>> handler = FileHandler()
        >>> await handler.write_file(Path("data.txt"), "content")
        >>> content = await handler.read_file(Path("data.txt"))
    """

    def __init__(self) -> None:
        """Initialize the FileHandler."""
        self._encoding = "utf-8"
        self._active_locks: dict[Path, FileLock] = {}

    # =========================================================================
    # File Read Operations
    # =========================================================================

    async def read_file(self, path: Path) -> str:
        """Read text content from a file.

        Args:
            path: Path to the file to read.

        Returns:
            The file content as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._read_file_sync, path)

    def _read_file_sync(self, path: Path) -> str:
        """Synchronous implementation of read_file."""
        if not path.exists():
            raise FileNotFoundError(
                message=f"File not found: {path}",
                details={"path": str(path)},
            )

        try:
            return path.read_text(encoding=self._encoding)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def read_bytes(self, path: Path) -> bytes:
        """Read binary content from a file.

        Args:
            path: Path to the file to read.

        Returns:
            The file content as bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._read_bytes_sync, path)

    def _read_bytes_sync(self, path: Path) -> bytes:
        """Synchronous implementation of read_bytes."""
        if not path.exists():
            raise FileNotFoundError(
                message=f"File not found: {path}",
                details={"path": str(path)},
            )

        try:
            return path.read_bytes()
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    # =========================================================================
    # File Write Operations
    # =========================================================================

    async def write_file(self, path: Path, content: str) -> None:
        """Write text content to a file.

        Creates parent directories if they don't exist.

        Args:
            path: Path to the file to write.
            content: The content to write.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        await asyncio.to_thread(self._write_file_sync, path, content)

    def _write_file_sync(self, path: Path, content: str) -> None:
        """Synchronous implementation of write_file."""
        try:
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding=self._encoding)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied writing file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error writing file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def write_bytes(self, path: Path, content: bytes) -> None:
        """Write binary content to a file.

        Creates parent directories if they don't exist.

        Args:
            path: Path to the file to write.
            content: The binary content to write.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        await asyncio.to_thread(self._write_bytes_sync, path, content)

    def _write_bytes_sync(self, path: Path, content: bytes) -> None:
        """Synchronous implementation of write_bytes."""
        try:
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied writing file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error writing file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    # =========================================================================
    # File Delete Operations
    # =========================================================================

    async def delete_file(self, path: Path) -> bool:
        """Delete a file.

        Args:
            path: Path to the file to delete.

        Returns:
            True if the file was deleted, False if it didn't exist.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._delete_file_sync, path)

    def _delete_file_sync(self, path: Path) -> bool:
        """Synchronous implementation of delete_file."""
        if not path.exists():
            return False

        try:
            path.unlink()
            return True
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied deleting file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error deleting file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    # =========================================================================
    # File Existence Operations
    # =========================================================================

    async def file_exists(self, path: Path) -> bool:
        """Check if a file exists.

        Args:
            path: Path to check.

        Returns:
            True if the path exists and is a file, False otherwise.
        """
        return await asyncio.to_thread(self._file_exists_sync, path)

    def _file_exists_sync(self, path: Path) -> bool:
        """Synchronous implementation of file_exists."""
        return path.exists() and path.is_file()

    # =========================================================================
    # Directory Operations
    # =========================================================================

    async def create_directory(self, path: Path, parents: bool = True) -> None:
        """Create a directory.

        Args:
            path: Path to the directory to create.
            parents: If True, create parent directories as needed.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        await asyncio.to_thread(self._create_directory_sync, path, parents)

    def _create_directory_sync(self, path: Path, parents: bool) -> None:
        """Synchronous implementation of create_directory."""
        try:
            path.mkdir(parents=parents, exist_ok=True)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied creating directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error creating directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def list_directory(self, path: Path, pattern: str = "*") -> List[Path]:
        """List contents of a directory.

        Args:
            path: Path to the directory to list.
            pattern: Glob pattern to filter results. Default is "*" (all).

        Returns:
            List of paths in the directory matching the pattern.

        Raises:
            DirectoryNotFoundError: If the directory does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._list_directory_sync, path, pattern)

    def _list_directory_sync(self, path: Path, pattern: str) -> List[Path]:
        """Synchronous implementation of list_directory."""
        if not path.exists():
            raise DirectoryNotFoundError(
                message=f"Directory not found: {path}",
                details={"path": str(path)},
            )

        if not path.is_dir():
            raise DirectoryNotFoundError(
                message=f"Path is not a directory: {path}",
                details={"path": str(path)},
            )

        try:
            return list(path.glob(pattern))
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied listing directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error listing directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def delete_directory(self, path: Path, recursive: bool = False) -> bool:
        """Delete a directory.

        Args:
            path: Path to the directory to delete.
            recursive: If True, delete directory and all contents.
                      If False, only delete if directory is empty.

        Returns:
            True if the directory was deleted, False if it didn't exist.

        Raises:
            DirectoryNotEmptyError: If directory is not empty and recursive=False.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._delete_directory_sync, path, recursive)

    def _delete_directory_sync(self, path: Path, recursive: bool) -> bool:
        """Synchronous implementation of delete_directory."""
        if not path.exists():
            return False

        try:
            if recursive:
                shutil.rmtree(path)
            else:
                # Check if directory is empty
                if any(path.iterdir()):
                    raise DirectoryNotEmptyError(
                        message=f"Directory is not empty: {path}",
                        details={"path": str(path)},
                    )
                path.rmdir()
            return True
        except DirectoryNotEmptyError:
            raise
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied deleting directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error deleting directory: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def directory_exists(self, path: Path) -> bool:
        """Check if a directory exists.

        Args:
            path: Path to check.

        Returns:
            True if the path exists and is a directory, False otherwise.
        """
        return await asyncio.to_thread(self._directory_exists_sync, path)

    def _directory_exists_sync(self, path: Path) -> bool:
        """Synchronous implementation of directory_exists."""
        return path.exists() and path.is_dir()

    # =========================================================================
    # File Info Operations
    # =========================================================================

    async def get_file_info(self, path: Path) -> FileInfo:
        """Get information about a file or directory.

        Args:
            path: Path to get info for.

        Returns:
            FileInfo object with file metadata.

        Raises:
            FileNotFoundError: If the path does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._get_file_info_sync, path)

    def _get_file_info_sync(self, path: Path) -> FileInfo:
        """Synchronous implementation of get_file_info."""
        if not path.exists():
            raise FileNotFoundError(
                message=f"Path not found: {path}",
                details={"path": str(path)},
            )

        try:
            stat = path.stat()

            # Convert timestamps to datetime
            created_at = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc)
            modified_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

            return FileInfo(
                path=path,
                size=stat.st_size if path.is_file() else 0,
                created_at=created_at,
                modified_at=modified_at,
                is_file=path.is_file(),
                is_directory=path.is_dir(),
            )
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied getting file info: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error getting file info: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    # =========================================================================
    # File Locking Operations
    # =========================================================================

    async def acquire_lock(self, path: Path, timeout: float = 10.0) -> FileLock:
        """Acquire a lock on a file.

        Uses a .lock file to indicate the lock is held.

        Args:
            path: Path to the file to lock.
            timeout: Maximum time to wait for lock in seconds.

        Returns:
            FileLock object representing the acquired lock.

        Raises:
            FileLockError: If the lock cannot be acquired within timeout.
        """
        lock_file = path.parent / f".{path.name}.lock"
        start_time = asyncio.get_event_loop().time()

        while True:
            # Try to acquire lock
            acquired = await asyncio.to_thread(self._try_acquire_lock_sync, path, lock_file)

            if acquired:
                lock = FileLock(
                    path=path,
                    acquired_at=datetime.now(timezone.utc),
                    lock_file=lock_file,
                )
                self._active_locks[path] = lock
                return lock

            # Check timeout
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed >= timeout:
                raise FileLockError(
                    message=f"Timeout acquiring lock for: {path}",
                    details={"path": str(path), "timeout": timeout},
                )

            # Wait a bit before retrying
            await asyncio.sleep(0.01)

    def _try_acquire_lock_sync(self, path: Path, lock_file: Path) -> bool:
        """Try to acquire lock synchronously."""
        try:
            # Ensure parent directory exists
            lock_file.parent.mkdir(parents=True, exist_ok=True)

            # Try to create lock file exclusively
            fd = os.open(
                str(lock_file),
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            )
            os.close(fd)
            return True
        except FileExistsError:
            return False
        except OSError:
            return False

    async def release_lock(self, lock: FileLock) -> None:
        """Release a previously acquired lock.

        Args:
            lock: The FileLock object to release.
        """
        await asyncio.to_thread(self._release_lock_sync, lock)

        # Remove from active locks
        if lock.path in self._active_locks:
            del self._active_locks[lock.path]

    def _release_lock_sync(self, lock: FileLock) -> None:
        """Synchronous implementation of release_lock."""
        try:
            if lock.lock_file.exists():
                lock.lock_file.unlink()
        except OSError:
            # Ignore errors when releasing lock
            pass

    @asynccontextmanager
    async def locked(self, path: Path, timeout: float = 10.0) -> AsyncIterator[FileLock]:
        """Context manager for file locking.

        Args:
            path: Path to the file to lock.
            timeout: Maximum time to wait for lock in seconds.

        Yields:
            FileLock object representing the acquired lock.

        Raises:
            FileLockError: If the lock cannot be acquired within timeout.

        Example:
            >>> async with handler.locked(Path("file.txt")) as lock:
            ...     await handler.write_file(Path("file.txt"), "content")
        """
        lock = await self.acquire_lock(path, timeout)
        try:
            yield lock
        finally:
            await self.release_lock(lock)
