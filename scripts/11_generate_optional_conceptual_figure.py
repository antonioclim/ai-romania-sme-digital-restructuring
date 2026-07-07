from __future__ import annotations
"""Compatibility wrapper for optional conceptual figure generation."""
import runpy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    runpy.run_path(str(ROOT / 'scripts' / '06_generate_figures.py'), run_name='__main__')
