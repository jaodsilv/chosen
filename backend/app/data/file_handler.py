"""FileHandler for file system operations.

This module provides a comprehensive file handler class that supports:
    - File read/write operations with UTF-8 encoding
    - Directory operations (create, list, delete)
    - File locking for concurrency safety
    - Async operations for non-blocking I/O
    - Comprehensive error handling

Example usage::

    import asyncio
    from pathlib import Path
    from app.data.file_handler import FileHandler

    async def main():
        handler = FileHandler()
        await handler.write_file(Path("test.txt"), "Hello, World!")
        content = await handler.read_file(Path("test.txt"))
        print(content)  # Output: Hello, World!

    asyncio.run(main())
"""

import asyncio
import logging
import os
import shutil
import threading
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator, List

import aiofiles
import aiofiles.os

from app.core.exceptions import (
    AppFileNotFoundError,
    DirectoryNotEmptyError,
    DirectoryNotFoundError,
    FileAccessError,
    FileLockError,
    FileOperationError,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FileInfo:
    """Information about a file or directory.

    Attributes:
        path: The path to the file or directory.
        size: The size in bytes (0 for directories).
        created_at: When the file was created. Note: Uses st_ctime which is
            file creation time on Windows, but metadata change time on Unix/Linux.
        modified_at: When the file was last modified.
        is_file: Whether this is a regular file.
        is_directory: Whether this is a directory.

    Raises:
        ValueError: If both is_file and is_directory are True, or if both are False
            (which would indicate an invalid filesystem entry like a broken symlink).
    """

    path: Path
    size: int
    created_at: datetime
    modified_at: datetime
    is_file: bool
    is_directory: bool

    def __post_init__(self) -> None:
        """Validate that is_file and is_directory represent a valid filesystem state."""
        if self.is_file and self.is_directory:
            raise ValueError("FileInfo cannot be both a file and a directory")
        if not self.is_file and not self.is_directory:
            raise ValueError(
                "FileInfo must be either a file or a directory "
                "(neither is set - this may indicate a broken symlink or special file)"
            )


@dataclass(frozen=True)
class FileLock:
    """Represents an acquired file lock.

    Attributes:
        path: The path to the locked file.
        acquired_at: When the lock was acquired.
        lock_file: Path to the lock file (computed from path).
    """

    path: Path
    acquired_at: datetime

    @property
    def lock_file(self) -> Path:
        """Return the path to the lock file.

        The lock file is stored in the same directory as the target file,
        with a '.' prefix and '.lock' suffix.
        """
        return self.path.parent / f".{self.path.name}.lock"


class FileHandler:
    """Handles file system operations with async support and file locking.

    This class provides methods for:
        - Reading and writing text and binary files
        - Creating, listing, and deleting directories
        - File locking for safe concurrent access
        - Getting file information and metadata

    All file operations are performed with UTF-8 encoding by default.
    Async operations use aiofiles for true async I/O on file read/write,
    and asyncio.to_thread for other filesystem operations (stat, mkdir, etc.).

    Example usage::

        handler = FileHandler()
        # In an async context:
        content = await handler.read_file(Path("data.txt"))
        await handler.write_file(Path("output.txt"), content)
    """

    def __init__(self) -> None:
        """Initialize the FileHandler."""
        self._encoding = "utf-8"
        self._active_locks: dict[Path, FileLock] = {}
        self._locks_mutex = threading.Lock()

    # =========================================================================
    # File Read Operations
    # =========================================================================

    async def read_file(self, path: Path) -> str:
        """Read text content from a file.

        Uses aiofiles for true async I/O. Uses try/except pattern instead of
        exists() check to avoid TOCTOU race condition.

        Args:
            path: Path to the file to read.

        Returns:
            The file content as a string.

        Raises:
            AppFileNotFoundError: If the file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors (including
                encoding errors for non-UTF-8 files).
        """
        try:
            async with aiofiles.open(path, "r", encoding=self._encoding) as f:
                content: str = await f.read()
                return content
        except FileNotFoundError:
            raise AppFileNotFoundError(
                message=f"File not found: {path}",
                details={"path": str(path)},
            )
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e
        except UnicodeDecodeError as e:
            raise FileOperationError(
                message=f"Error reading file: {path} - file is not valid UTF-8 encoded",
                details={"path": str(path), "error": str(e), "encoding": self._encoding},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error reading file: {path}",
                details={"path": str(path), "error": str(e)},
            ) from e

    async def read_bytes(self, path: Path) -> bytes:
        """Read binary content from a file.

        Uses aiofiles for true async I/O. Uses try/except pattern instead of
        exists() check to avoid TOCTOU race condition.

        Args:
            path: Path to the file to read.

        Returns:
            The file content as bytes.

        Raises:
            AppFileNotFoundError: If the file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        try:
            async with aiofiles.open(path, "rb") as f:
                content: bytes = await f.read()
                return content
        except FileNotFoundError:
            raise AppFileNotFoundError(
                message=f"File not found: {path}",
                details={"path": str(path)},
            )
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
        Uses aiofiles for true async I/O.

        Note:
            If the file already exists, it will be completely overwritten.
            Use file locking (via `locked()` context manager) if you need
            to prevent concurrent access during read-modify-write operations.

        Args:
            path: Path to the file to write.
            content: The content to write.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        try:
            # Create parent directories if needed (sync, but quick)
            path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(path, "w", encoding=self._encoding) as f:
                await f.write(content)
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
        Uses aiofiles for true async I/O.

        Note:
            If the file already exists, it will be completely overwritten.
            Use file locking (via `locked()` context manager) if you need
            to prevent concurrent access during read-modify-write operations.

        Args:
            path: Path to the file to write.
            content: The binary content to write.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        try:
            # Create parent directories if needed (sync, but quick)
            path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(path, "wb") as f:
                await f.write(content)
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
        """Synchronous implementation of delete_file.

        Uses try/except pattern instead of exists() check to avoid TOCTOU
        race condition where file could be deleted between check and unlink.
        """
        try:
            path.unlink()
            return True
        except FileNotFoundError:
            # Python's built-in FileNotFoundError - file doesn't exist
            return False
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
    # File Copy and Move Operations
    # =========================================================================

    async def copy_file(self, source: Path, destination: Path) -> None:
        """Copy a file from source to destination.

        Creates parent directories of destination if they don't exist.
        Uses try/except pattern to avoid TOCTOU race condition.

        Note:
            If the destination file already exists, it will be completely overwritten.
            Use file locking if you need to prevent concurrent access.

        Args:
            source: Path to the source file.
            destination: Path to the destination file.

        Raises:
            AppFileNotFoundError: If the source file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors, including
                errors creating parent directories.
        """
        try:
            # Create parent directories if needed
            destination.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied creating destination directory: {destination.parent}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error creating destination directory: {destination.parent}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e

        try:
            # Use shutil.copy2 to preserve metadata
            await asyncio.to_thread(shutil.copy2, source, destination)
        except FileNotFoundError:
            raise AppFileNotFoundError(
                message=f"Source file not found: {source}",
                details={"source": str(source), "destination": str(destination)},
            )
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied copying file: {source} -> {destination}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error copying file: {source} -> {destination}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e

    async def move_file(self, source: Path, destination: Path) -> None:
        """Move a file from source to destination.

        Creates parent directories of destination if they don't exist.
        Uses try/except pattern to avoid TOCTOU race condition.

        Note:
            If the destination file already exists, it will be completely overwritten.
            Use file locking if you need to prevent concurrent access.

        Args:
            source: Path to the source file.
            destination: Path to the destination file.

        Raises:
            AppFileNotFoundError: If the source file does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors, including
                errors creating parent directories.
        """
        try:
            # Create parent directories if needed
            destination.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied creating destination directory: {destination.parent}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error creating destination directory: {destination.parent}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e

        try:
            # Use shutil.move for cross-filesystem moves
            await asyncio.to_thread(shutil.move, str(source), str(destination))
        except FileNotFoundError:
            raise AppFileNotFoundError(
                message=f"Source file not found: {source}",
                details={"source": str(source), "destination": str(destination)},
            )
        except PermissionError as e:
            raise FileAccessError(
                message=f"Permission denied moving file: {source} -> {destination}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
            ) from e
        except OSError as e:
            raise FileOperationError(
                message=f"Error moving file: {source} -> {destination}",
                details={"source": str(source), "destination": str(destination), "error": str(e)},
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

        Creates the directory if it does not exist. If the directory already
        exists, no error is raised (equivalent to mkdir's exist_ok=True behavior).

        Args:
            path: Path to the directory to create.
            parents: If True (default), create parent directories as needed.
                If False and parent directories don't exist, raises FileOperationError.

        Raises:
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors, including
                missing parent directories when parents=False.
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
            ValueError: If the pattern contains unsafe path traversal sequences.
        """
        self._validate_glob_pattern(pattern)
        return await asyncio.to_thread(self._list_directory_sync, path, pattern)

    def _validate_glob_pattern(self, pattern: str) -> None:
        """Validate glob pattern is safe and well-formed.

        Args:
            pattern: The glob pattern to validate.

        Raises:
            ValueError: If the pattern contains unsafe sequences like '..',
                absolute paths (starting with '/'), or Windows drive letters.
        """
        if not pattern:
            return
        # Check for directory traversal attempts
        if ".." in pattern:
            raise ValueError("Glob pattern cannot contain '..' for security reasons")
        # Check for absolute paths (Unix-style)
        if pattern.startswith("/"):
            raise ValueError("Glob pattern cannot be an absolute path for security reasons")
        # Check for Windows drive letters (e.g., "C:", "D:")
        if len(pattern) >= 2 and pattern[1] == ":" and pattern[0].isalpha():
            raise ValueError("Glob pattern cannot contain drive letters for security reasons")

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
            AppFileNotFoundError: If the path does not exist.
            FileAccessError: If there's a permission error.
            FileOperationError: For other file operation errors.
        """
        return await asyncio.to_thread(self._get_file_info_sync, path)

    def _get_file_info_sync(self, path: Path) -> FileInfo:
        """Synchronous implementation of get_file_info.

        Note:
            The created_at field uses st_ctime which represents:
            - On Windows: The actual file creation time
            - On Unix/Linux: The last metadata change time (inode change)
        """
        if not path.exists():
            raise AppFileNotFoundError(
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
            FileAccessError: If there's a permission error creating the lock file.
            FileOperationError: For other unexpected errors (disk full, etc.).
        """
        # Compute lock_file path (same logic as FileLock.lock_file property)
        lock_file = path.parent / f".{path.name}.lock"
        start_time = time.monotonic()

        while True:
            # Try to acquire lock
            acquired = await asyncio.to_thread(self._try_acquire_lock_sync, path, lock_file)

            if acquired:
                lock = FileLock(
                    path=path,
                    acquired_at=datetime.now(timezone.utc),
                )
                with self._locks_mutex:
                    self._active_locks[path] = lock
                return lock

            # Check timeout
            elapsed = time.monotonic() - start_time
            if elapsed >= timeout:
                raise FileLockError(
                    message=f"Timeout acquiring lock for: {path}",
                    details={
                        "path": str(path),
                        "timeout": timeout,
                        "lock_file": str(lock_file),
                        "lock_file_exists": lock_file.exists(),
                    },
                )

            # Wait a bit before retrying
            await asyncio.sleep(0.01)

    def _try_acquire_lock_sync(self, path: Path, lock_file: Path) -> bool:
        """Try to acquire lock synchronously.

        Returns:
            True if lock was acquired, False if lock is held by another process.

        Raises:
            FileAccessError: If there's a permission error creating the lock file.
            FileOperationError: For other unexpected OS errors (disk full, etc.).
        """
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
            # Lock already held by another process - expected behavior
            return False
        except PermissionError as e:
            # Permission denied - raise immediately instead of waiting for timeout
            raise FileAccessError(
                message=f"Permission denied creating lock file for: {path}",
                details={"path": str(path), "lock_file": str(lock_file), "error": str(e)},
            ) from e
        except OSError as e:
            # Unexpected error (disk full, etc.) - raise immediately
            logger.warning(f"Failed to acquire lock for {path}: {e}")
            raise FileOperationError(
                message=f"Error creating lock file for: {path}",
                details={"path": str(path), "lock_file": str(lock_file), "error": str(e)},
            ) from e

    async def release_lock(self, lock: FileLock) -> None:
        """Release a previously acquired lock.

        Args:
            lock: The FileLock object to release.
        """
        await asyncio.to_thread(self._release_lock_sync, lock)

        # Remove from active locks with thread safety
        with self._locks_mutex:
            if lock.path in self._active_locks:
                del self._active_locks[lock.path]

    def _release_lock_sync(self, lock: FileLock) -> None:
        """Synchronous implementation of release_lock."""
        try:
            if lock.lock_file.exists():
                lock.lock_file.unlink()
        except OSError as e:
            # Log at ERROR level with actionable guidance - orphan lock files can
            # block future operations indefinitely
            logger.error(
                f"Failed to release lock file {lock.lock_file}: {e}. "
                f"This may leave an orphan lock file that blocks future operations. "
                f"Manual cleanup may be required: delete {lock.lock_file}"
            )

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

        Example usage::

            async with handler.locked(Path("file.txt")) as lock:
                await handler.write_file(Path("file.txt"), "content")
        """
        lock = await self.acquire_lock(path, timeout)
        try:
            yield lock
        finally:
            await self.release_lock(lock)
