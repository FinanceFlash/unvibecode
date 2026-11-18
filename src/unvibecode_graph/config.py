"""Every setting of a fast-lane run (Config) and the language tables."""
from __future__ import annotations

import os
from dataclasses import dataclass

VERSION = "v11-api-context-bundle"


@dataclass(frozen=True)
class Config:
    """One run's settings. The defaults are exactly what the hosted service uses."""

    # what to produce
    context_downloads: bool = True  # per-file connected-code downloads + complete-context ZIP
    open_browser: bool = False  # open the graph HTML when the run finishes

    # stage two: linker
    allow_global_symbol_fallback: bool = False
    strict_hard_path: bool = False
    deep_relative_parent_hops: int = 3
    enrich_python: bool = True

    # code chunking (tokens)
    whole_file_limit: int = 2500  # files up to this size stay one chunk
    max_entity_tokens: int = 3000  # larger functions/classes are split
    segment_tokens: int = 1800  # size of the pieces they are split into
    overlap_tokens: int = 150
    tiny_context_tokens: int = 100  # file-context pieces smaller than this are merged
    encoding_name: str = "cl100k_base"
    # "fast" estimates tokens conservatively without calling the tokenizer for
    # every file's three download choices; "exact" uses tiktoken.
    token_mode: str = "fast"

    # connected-code downloads (tokens): radius 0 = focused, 1 = direct, 2 = extended
    focused_max_tokens: int = 30000
    direct_target_tokens: int = 35000
    direct_max_tokens: int = 45000
    extended_target_tokens: int = 60000
    extended_max_tokens: int = 75000
    package_safety_tokens: int = 2500  # reserved for the download's own wrapper


# -----------------------------------------------------------------------------
# Language tables
# -----------------------------------------------------------------------------
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".next",
    ".nuxt",
    "dist",
    "build",
    "out",
    "target",
    "coverage",
    ".turbo",
    ".cache",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".rs": "rust",
    ".go": "go",
    ".php": "php",
    ".rb": "ruby",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
}

# These are scanned and reported as unsupported instead of silently ignored.
UNSUPPORTED_LANGUAGE_BY_EXTENSION = {
    ".java": "java",
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".h": "c_header",
    ".hpp": "cpp_header",
    ".cs": "csharp",
    ".kt": "kotlin",
    ".swift": "swift",
}

# Tree-sitter parser names can differ slightly by package. We try these in order.
TREE_SITTER_LANGUAGE_CANDIDATES = {
    "javascript": ["javascript"],
    "jsx": ["javascript", "tsx"],
    "typescript": ["typescript"],
    "tsx": ["tsx", "typescript"],
    "rust": ["rust"],
    "go": ["go"],
    "php": ["php"],
    "ruby": ["ruby"],
}

NODE_TS_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json"]
PY_EXTENSIONS = [".py", os.path.join("", "__init__.py")]
RUST_EXTENSIONS = [".rs"]
PHP_EXTENSIONS = [".php"]
RUBY_EXTENSIONS = [".rb"]
WEB_ASSET_EXTENSIONS = [".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".json"]
