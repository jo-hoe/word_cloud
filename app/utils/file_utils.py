import os
from typing import Optional


def get_absolute_path(base_dir: str, path: str) -> str:
    """
    Join a path with a base directory.
    Useful for constructing absolute paths relative to a known directory.
    """
    return os.path.join(base_dir, path)


def get_file_content(
    path: str,
    *,
    base_dir: Optional[str] = None,
    project_root: Optional[str] = None,
    encoding: str = "utf8",
) -> str:
    """
    Read text content from a file. Tries multiple locations for relative paths:
    - As provided (current working directory)
    - Relative to base_dir (typically the caller's module directory)
    - Under project_root (defaults to two levels above base_dir if not provided)
    """
    candidates = [path]

    if not os.path.isabs(path):
        if base_dir:
            candidates.append(os.path.join(base_dir, path))
            # Mirror the original behavior: if not provided, project_root defaults to two levels above base_dir
            if project_root is None:
                project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
        if project_root:
            candidates.append(os.path.join(project_root, path))

    last_error: Optional[Exception] = None
    for p in candidates:
        try:
            with open(p, "r", encoding=encoding, errors="ignore") as file:
                return file.read()
        except FileNotFoundError as e:
            last_error = e
            continue

    if last_error:
        raise last_error
    raise FileNotFoundError(f"File not found: {path}")