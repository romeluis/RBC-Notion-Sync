"""
Utility functions for tests
"""

from pathlib import Path
from typing import List, Optional


def find_qfx_files(base_path: Optional[Path] = None) -> List[Path]:
    """
    Find QFX files in the input directory relative to the project root.
    
    Args:
        base_path: Base path to search from. If None, uses the current file's parent.
        
    Returns:
        List of QFX file paths found in the input directory.
    """
    if base_path is None:
        # Assume we're being called from src/ directory
        base_path = Path(__file__).parent.parent
    
    input_dir = base_path / "input"
    
    # Look for QFX files (both lowercase and uppercase extensions)
    qfx_files = []
    qfx_files.extend(input_dir.glob("*.qfx"))
    qfx_files.extend(input_dir.glob("*.QFX"))
    
    return qfx_files


def get_test_qfx_file(base_path: Optional[Path] = None) -> Optional[Path]:
    """
    Get the first available QFX file for testing purposes.
    
    Args:
        base_path: Base path to search from. If None, uses the current file's parent.
        
    Returns:
        Path to the first QFX file found, or None if no files found.
    """
    qfx_files = find_qfx_files(base_path)
    return qfx_files[0] if qfx_files else None


def print_qfx_file_info(base_path: Optional[Path] = None) -> bool:
    """
    Print information about QFX files found in the input directory.
    
    Args:
        base_path: Base path to search from. If None, uses the current file's parent.
        
    Returns:
        True if QFX files were found, False otherwise.
    """
    if base_path is None:
        base_path = Path(__file__).parent.parent
    
    input_dir = base_path / "input"
    qfx_files = find_qfx_files(base_path)
    
    print(f"Input directory: {input_dir}")
    print(f"Found {len(qfx_files)} QFX file(s)")
    
    if qfx_files:
        for i, qfx_file in enumerate(qfx_files, 1):
            print(f"  {i}. {qfx_file.name}")
        return True
    else:
        print("💡 Please add a QFX file to the input directory")
        return False
