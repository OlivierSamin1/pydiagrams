"""
PyDiagrams: A Python library for generating Mermaid diagrams.

PyDiagrams makes it easy to create, customize, and export diagrams from Mermaid syntax.
The library supports generation of SVG, PNG, and interactive HTML diagrams with theme customization.
"""

__version__ = "1.0.0"
__author__ = "Olivier Samin"

from typing import Optional

from pydiagrams.parsers.diagram_utils import (
    generate_diagram_from_file,
    detect_diagram_file_type,
    is_diagram_file
)


def create_diagram_from_file(
    file_path: str,
    output_path: Optional[str] = None,
    output_format: str = 'svg',
    theme: Optional[str] = None,
    dark_mode: bool = False,
    inline_resources: bool = True
) -> str:
    """
    Generate a diagram from a Mermaid file.
    
    Args:
        file_path: Path to the Mermaid file
        output_path: Path to save the output (if None, uses the same name as input file)
        output_format: Output format ('svg', 'png', 'html')
        theme: Theme to use for the diagram (HTML output only)
            Supported themes: 'default', 'forest', 'dark', 'neutral', 'blue', 'high-contrast'
        dark_mode: Whether to use dark mode (HTML output only)
        inline_resources: Whether to inline resources in HTML output for better portability
        
    Returns:
        str: Path to the generated diagram file
        
    Raises:
        ValueError: If the file is not a valid Mermaid file
        FileNotFoundError: If the file does not exist
    """
    return generate_diagram_from_file(
        file_path, 
        output_path, 
        output_format,
        theme,
        dark_mode,
        inline_resources
    ) 