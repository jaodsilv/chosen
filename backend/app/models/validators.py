"""Shared validators for Pydantic models.

This module provides reusable validation functions for model fields,
including security-focused path validation.
"""

import os
from pathlib import Path
from typing import List, Optional

from app.config import get_settings


def validate_path_in_data_dir(path: Optional[str]) -> Optional[str]:
    """Validate that a path resolves to within the data directory.

    This function ensures that file paths cannot escape the configured
    data directory, preventing path traversal attacks.

    Args:
        path: The path to validate (relative to data_dir or absolute).
            Can be None.

    Returns:
        The validated path (as provided, not resolved).

    Raises:
        ValueError: If path resolves outside the allowed data directory.
    """
    if path is None:
        return path

    settings = get_settings()
    data_dir = Path(settings.data_dir).resolve()

    # Resolve the path relative to data_dir
    if os.path.isabs(path):
        resolved = Path(path).resolve()
    else:
        resolved = (data_dir / path).resolve()

    # Check if resolved path is within data_dir
    try:
        resolved.relative_to(data_dir)
    except ValueError:
        raise ValueError(
            f"Path must be within the data directory. "
            f"'{path}' resolves outside allowed directory."
        )

    return path


def validate_attachment_paths(paths: List[str]) -> List[str]:
    """Validate all paths in an attachments list.

    Ensures that all file paths in the list resolve to within
    the configured data directory.

    Args:
        paths: List of file paths to validate.

    Returns:
        The validated list of paths (unchanged if valid).

    Raises:
        ValueError: If any path resolves outside the allowed data directory.
    """
    for path in paths:
        validate_path_in_data_dir(path)
    return paths
