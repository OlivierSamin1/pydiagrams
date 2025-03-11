"""
Utility functions for working with diagram files.

This module provides utility functions for working with Mermaid and PlantUML diagram files,
including file detection, parsing, and rendering.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

def detect_diagram_file_type(file_path: str) -> str:
    """
    Detect the type of a diagram file based on its extension or content.
    
    Args:
        file_path: Path to the diagram file
        
    Returns:
        str: Type of diagram ('mermaid')
        
    Raises:
        ValueError: If the file type cannot be determined
    """
    path = Path(file_path)
    
    # Check by extension
    if path.suffix.lower() == '.mmd':
        return 'mermaid'
    
    # Check by content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for Mermaid patterns
            if any(keyword in content.lower() for keyword in 
                   ['graph ', 'flowchart ', 'sequencediagram', 'classDiagram', 'erDiagram']):
                return 'mermaid'
    except Exception as e:
        pass
        
    raise ValueError(f"Cannot determine diagram type for file: {file_path}")

def is_diagram_file(file_path: str) -> bool:
    """
    Check if a file is a supported diagram file.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        bool: True if the file is a supported diagram file, False otherwise
    """
    try:
        detect_diagram_file_type(file_path)
        return True
    except ValueError:
        return False

def parse_diagram_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a diagram file and return its contents.
    
    Args:
        file_path: Path to the diagram file
        
    Returns:
        Dict[str, Any]: Dictionary with diagram data
    """
    diagram_type = detect_diagram_file_type(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create a basic diagram data structure
    diagram_data = {
        'type': diagram_type,
        'raw_content': content,
        'title': Path(file_path).stem
    }
    
    return diagram_data

def generate_diagram_from_file(
    file_path: str, 
    output_path: Optional[str] = None, 
    output_format: str = 'svg',
    theme: Optional[str] = None,
    dark_mode: bool = False,
    inline_resources: bool = True
) -> str:
    """
    Generate a diagram from a file.
    
    Args:
        file_path: Path to the diagram file
        output_path: Path to save the output (if None, uses the same name as input file)
        output_format: Output format ('svg', 'png', 'html')
        theme: Theme to use for the diagram (HTML output only)
        dark_mode: Whether to use dark mode (HTML output only)
        inline_resources: Whether to inline resources in HTML output
        
    Returns:
        str: Path to the generated diagram
    """
    # Parse the diagram file to get its contents and type
    diagram_data = parse_diagram_file(file_path)
    
    # Determine output path if not provided
    if output_path is None:
        input_path = Path(file_path)
        output_path = str(input_path.with_suffix(f'.{output_format}'))
    
    # Handle different output formats
    if output_format == 'html':
        # Import HTML renderer
        from pydiagrams.renderers.html_renderer import HTMLRenderer
        
        # Create renderer with options
        renderer = HTMLRenderer(
            width=800, 
            height=600, 
            interactive=True,
            dark_mode=dark_mode,
            inline_resources=inline_resources
        )
        
        # If a theme is specified, add it to the diagram data
        if theme:
            diagram_data['theme'] = theme
        
        # Render the diagram to HTML
        output_path = renderer.render(diagram_data, output_path)
    else:
        # For other formats, we need to implement rendering logic
        # Currently we'll just use Mermaid renderer
        try:
            from pydiagrams.renderers.mermaid_renderer import MermaidRenderer
            renderer = MermaidRenderer()
            output_path = renderer.render(diagram_data, output_path, output_format=output_format)
        except ImportError:
            try:
                # Fallback to a basic file copy for now
                # This should be replaced with actual rendering logic
                from shutil import copyfile
                copyfile(file_path, output_path)
                print(f"Warning: SVG/PNG rendering not implemented yet. Copied file to {output_path}")
            except Exception as e:
                print(f"Error creating {output_format} output: {e}")
                # Just return the file_path as-is
                return output_path
    
    return output_path 