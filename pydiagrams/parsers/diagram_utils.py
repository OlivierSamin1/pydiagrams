"""
Utility functions for working with diagram files.

This module provides utility functions for working with Mermaid and PlantUML diagram files,
including file detection, parsing, and rendering.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Union, Dict, Any, Tuple

from pydiagrams.parsers.base_parser import BaseParser
from pydiagrams.parsers.mermaid_parser import MermaidParser
from pydiagrams.parsers.plantuml_parser import PlantUMLParser


def detect_diagram_file_type(file_path: Union[str, Path]) -> Optional[str]:
    """
    Detect the diagram type from a file.

    Args:
        file_path: Path to the file to analyze

    Returns:
        String identifying the diagram type ('mermaid', 'plantuml') or None if not a diagram file
    """
    return BaseParser.detect_file_type(file_path)


def parse_diagram_file(file_path: Union[str, Path]) -> Tuple[Dict[str, Any], BaseParser]:
    """
    Parse a diagram file and return the diagram data and parser instance.

    Args:
        file_path: Path to the diagram file

    Returns:
        A tuple containing the diagram data and the parser instance
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    diagram_type = detect_diagram_file_type(file_path)
    
    if diagram_type == 'mermaid':
        parser = MermaidParser.from_file(file_path)
        data = parser.parse()
        return data, parser
    elif diagram_type == 'plantuml':
        parser = PlantUMLParser.from_file(file_path)
        data = parser.parse()
        return data, parser
    else:
        raise ValueError(f"Unsupported diagram file type: {file_path}")


def generate_diagram_from_file(
    file_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    output_format: str = 'svg',
    dark_mode: bool = False,
    inline_resources: bool = False
) -> str:
    """
    Generate a diagram from a Mermaid or PlantUML file.

    Args:
        file_path: Path to the diagram file
        output_path: Path where to save the generated diagram (if None, it will use the input filename with appropriate extension)
        output_format: Output format ('svg', 'png', 'html', 'pdf')
        dark_mode: Whether to use dark mode for HTML output
        inline_resources: Whether to inline CSS and JS resources in HTML (avoids CORS issues)

    Returns:
        Path to the generated diagram file
    """
    file_path = Path(file_path)
    
    if not output_path:
        # Create output path based on input filename
        output_path = file_path.with_suffix(f'.{output_format}')
    else:
        output_path = Path(output_path)
    
    diagram_type = detect_diagram_file_type(file_path)
    
    if not diagram_type:
        raise ValueError(f"Could not determine diagram type for file: {file_path}")
    
    # Get diagram data from file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to use parsers if available
    try:
        data, parser = parse_diagram_file(file_path)
        # Add raw content to data
        data['raw_content'] = content
        # Add title if not present
        if 'title' not in data:
            data['title'] = file_path.stem
    except (ImportError, ModuleNotFoundError):
        # If parsers aren't available, create a simple data dictionary
        data = {
            'type': diagram_type,
            'raw_content': content,
            'title': file_path.stem
        }
        parser = None
        
    # Check which renderer to use based on output format
    if output_format.lower() == 'html':
        from pydiagrams.renderers.html_renderer import HTMLRenderer
        
        # Create an HTML renderer with dark mode option
        renderer = HTMLRenderer(dark_mode=dark_mode, inline_resources=inline_resources)
        
        # Render the diagram to HTML
        return renderer.render(data, str(output_path))
    elif diagram_type == 'mermaid':
        if output_format.lower() == 'svg':
            from pydiagrams.renderers.mermaid_renderer import MermaidRenderer
            renderer = MermaidRenderer()
            return renderer.render(data, str(output_path))
        elif output_format.lower() == 'png':
            from pydiagrams.renderers.mermaid_renderer import MermaidRenderer
            renderer = MermaidRenderer()
            return renderer.render_png(data, str(output_path))
        else:
            raise ValueError(f"Unsupported output format for Mermaid: {output_format}")
    elif diagram_type == 'plantuml':
        if parser and hasattr(parser, f'generate_{output_format.lower()}'):
            # Use the parser's generation methods if available
            generate_method = getattr(parser, f'generate_{output_format.lower()}')
            return generate_method(str(output_path))
        else:
            # Use our PlantUML renderer
            if output_format.lower() == 'svg':
                from pydiagrams.renderers.plantuml_renderer import PlantUMLRenderer
                renderer = PlantUMLRenderer()
                return renderer.render(data, str(output_path))
            elif output_format.lower() == 'png':
                from pydiagrams.renderers.plantuml_renderer import PlantUMLRenderer
                renderer = PlantUMLRenderer()
                return renderer.render_png(data, str(output_path))
            else:
                raise ValueError(f"Unsupported output format for PlantUML: {output_format}")
    else:
        raise ValueError(f"Unsupported diagram file type: {file_path}")
        
    return str(output_path)


def is_diagram_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a diagram file (Mermaid or PlantUML).

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file is a diagram file, False otherwise
    """
    return detect_diagram_file_type(file_path) is not None 