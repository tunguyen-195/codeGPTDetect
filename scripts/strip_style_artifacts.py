"""
Strip Style Artifacts from AI-Generated Python Code  (v2 - aggressive)

Nguyên nhân 100% accuracy:
  Pass 1 (done): Google-style section headers (Args:, Returns:, ...)  → đã fix
  Pass 2 (này):  Inline param docs  "  name (type): desc"  [26% AI vs 7% Human]
                 File length gap     AI median 62 lines vs Human median 19 lines

Script này loại bỏ:
1. Google-style docstring section headers  (Args:, Returns:, ...)
2. Inline parameter/attribute descriptions  (word (type): description)
3. Return type annotations                 (-> Type:)
4. Truncate AI files to max 40 lines      (giảm length gap 3.3x → ~1.5x)
5. Dọn dẹp blank lines thừa (max 1 liên tiếp)

Usage:
    python scripts/strip_style_artifacts.py
    python scripts/strip_style_artifacts.py --no-regen
"""

import re
import os
import sys
import shutil
import argparse
from pathlib import Path

# Google-style section headers to remove
GOOGLE_SECTIONS = {
    'Args', 'Arguments', 'Parameters', 'Params',
    'Returns', 'Return', 'Yields', 'Yield',
    'Raises', 'Raise', 'Except', 'Exceptions',
    'Examples', 'Example',
    'Notes', 'Note',
    'Attributes',
    'Todo',
    'References',
    'See Also',
    'Warnings', 'Warning',
    'Keyword Args', 'Keyword Arguments',
}

# Max lines for AI files (human median ≈ 19, p75 ≈ 32)
AI_MAX_LINES = 40


# ─── Step 1: Remove section headers + their indented content ────────────────

def strip_google_sections(code: str) -> tuple:
    """
    Remove Google-style docstring section headers and their content.
    e.g.:
        Args:
            x (int): The value.   ← both header and content removed
    Returns (cleaned_code, num_sections_removed)
    """
    lines = code.split('\n')
    result = []
    skip_indent = None
    removed = 0

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if skip_indent is not None:
                continue       # skip blank lines inside a removed section
            result.append(line)
            continue

        curr_indent = len(line) - len(line.lstrip())

        if skip_indent is not None:
            if curr_indent > skip_indent:
                continue       # still inside removed section
            else:
                skip_indent = None   # exited section

        m = re.match(r'^([ \t]+)([A-Z][A-Za-z ]+):\s*$', line)
        if m and m.group(2).strip() in GOOGLE_SECTIONS:
            skip_indent = len(m.group(1))
            removed += 1
            continue

        result.append(line)

    return '\n'.join(result), removed


# ─── Step 2: Remove inline "name (type): description" lines ─────────────────

# Matches lines like:
#     x (int): The value.
#     heap_type (str): One of 'min' or 'max'.
#     node (Node): Current tree node.
# These appear in docstrings WITHOUT a section header — our step-1 missed them.
_INLINE_PARAM = re.compile(
    r'(?m)^[ \t]{4,}\w[\w_]*\s+\([^)\n]{1,40}\):\s+\S[^\n]*$'
)

def strip_inline_param_docs(code: str) -> str:
    """Remove 'varname (Type): description' lines that appear without a header."""
    return _INLINE_PARAM.sub('', code)


# ─── Step 3: Remove return type annotations ──────────────────────────────────

def strip_return_annotations(code: str) -> str:
    """
    def foo(x) -> SomeType:  →  def foo(x):
    Handles: None, str, int, Optional[X], Dict[str, int], List[int], ...
    """
    return re.sub(r'\)\s*->\s*[^:\n]+\s*(?=:)', ')', code)


# ─── Step 4: Truncate to max lines ───────────────────────────────────────────

def truncate_file(code: str, max_lines: int = AI_MAX_LINES) -> str:
    """
    Keep only first max_lines lines.
    Reduces AI median from 62 → ~35 lines (human median 19, avg 28).
    """
    lines = code.split('\n')
    if len(lines) <= max_lines:
        return code
    return '\n'.join(lines[:max_lines])


# ─── Step 5: Clean up blank lines ────────────────────────────────────────────

def clean_blank_lines(code: str) -> str:
    """Reduce consecutive blank lines to at most 1."""
    return re.sub(r'\n{2,}', '\n', code)


# ─── Main processing ─────────────────────────────────────────────────────────

def process_ai_file(filepath: Path) -> tuple:
    """Apply all 5 steps to a single AI file. Returns (was_modified, sections_removed)."""
    try:
        original = filepath.read_text(encoding='utf-8', errors='ignore')

        code, sections_removed = strip_google_sections(original)
        code = strip_inline_param_docs(code)
        code = strip_return_annotations(code)
        code = truncate_file(code)
        code = clean_blank_lines(code)

        if code != original:
            filepath.write_text(code, encoding='utf-8')
            return True, sections_removed

        return False, 0

    except Exception as e:
        print(f"  Warning: {filepath.name}: {e}")
        return False, 0


def process_directory(directory: Path, label_prefix: str = '0_') -> dict:
    """Process all AI files (prefix 0_) in a directory."""
    if not directory.exists():
        return {'total': 0, 'modified': 0, 'sections': 0, 'skipped': True}

    files = sorted(f for f in directory.glob('*.py') if f.name.startswith(label_prefix))
    stats = {'total': len(files), 'modified': 0, 'sections': 0, 'skipped': False}

    for fp in files:
        modified, sections = process_ai_file(fp)
        if modified:
            stats['modified'] += 1
            stats['sections'] += sections

    return stats


def print_stats(name: str, stats: dict):
    if stats.get('skipped'):
        print(f"  {name}: not found, skipped")
        return
    pct = f"({stats['modified']/stats['total']*100:.0f}%)" if stats['total'] else ""
    print(f"  {name}: {stats['modified']}/{stats['total']} files modified {pct}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-regen', action='store_true',
                        help='Skip regenerating train/test splits')
    parser.add_argument('--lang', default='python', choices=['python', 'cpp'])
    args = parser.parse_args()

    base = Path(f'DATASETS/{args.lang.upper()}')

    print('=' * 60)
    print('STRIP STYLE ARTIFACTS v2 (aggressive)')
    print('=' * 60)
    print(f'Fixes: section headers, inline param docs, return annotations,')
    print(f'       truncate AI files to {AI_MAX_LINES} lines, clean blank lines')
    print()

    directories = {
        'raw/ai':       base / 'raw' / 'ai',
        'training_data': base / 'training_data',
        'testing_data':  base / 'testing_data',
    }

    total_modified = 0
    for name, directory in directories.items():
        stats = process_directory(directory)
        print_stats(name, stats)
        total_modified += stats['modified']

    print()
    print(f'Total files modified: {total_modified}')
    print('=' * 60)

    if not args.no_regen:
        print('\nRegenerating train/test splits from cleaned raw data...')
        for split_dir in [base / 'training_data', base / 'testing_data']:
            if split_dir.exists():
                shutil.rmtree(split_dir)
        os.system(f'python scripts/prepare_dataset.py --language {args.lang}')

    print('\nDone.')


if __name__ == '__main__':
    main()
