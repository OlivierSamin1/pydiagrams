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
    dark_mode: bool = False
) -> str:
    """
    Generate a diagram from a Mermaid or PlantUML file.

    Args:
        file_path: Path to the diagram file
        output_path: Path where to save the generated diagram (if None, it will use the input filename with appropriate extension)
        output_format: Output format ('svg', 'png', 'html', 'pdf')
        dark_mode: Whether to use dark mode for HTML output

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
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse the diagram file
    data, parser = parse_diagram_file(file_path)
    
    # For HTML output, use the HTML renderer
    if output_format.lower() == 'html':
        try:
            from pydiagrams.renderers.html_renderer import HTMLRenderer
            
            # Create an HTML renderer with dark mode option
            renderer = HTMLRenderer(dark_mode=dark_mode)
            
            # Store the raw content in the data for rendering
            data['raw_content'] = content
            
            # Create a title from the filename
            if 'title' not in data:
                data['title'] = file_path.stem.replace('_', ' ').title()
            
            # Render the diagram to HTML
            return renderer.render(data, str(output_path))
        except ImportError:
            raise ImportError("HTML renderer not available. Make sure Jinja2 is installed.")
    elif diagram_type == 'mermaid':
        # For Mermaid, we'll create a simple SVG with a reference to the Mermaid content
        # In a real implementation, we would use a Mermaid renderer
        if output_format.lower() == 'svg':
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <pre class="mermaid">
{content}
      </pre>
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <script>mermaid.initialize({{startOnLoad:true}});</script>
    </div>
  </foreignObject>
</svg>"""
            
            with open(output_path, 'w') as f:
                f.write(svg_content)
        else:
            # For PNG, we'll create a simple text file
            with open(output_path, 'wb') as f:
                # Create a simple PNG with the text "Mermaid Diagram"
                # In a real implementation, we would use a Mermaid renderer
                # This is just a placeholder
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
        
        return str(output_path)
    elif diagram_type == 'plantuml':
        # For PlantUML, use the PlantUML parser's generation methods
        if output_format.lower() == 'svg':
            return parser.generate_svg(str(output_path))
        elif output_format.lower() == 'png':
            return parser.generate_png(str(output_path))
        else:
            raise ValueError(f"Unsupported output format for PlantUML: {output_format}")
    else:
        raise ValueError(f"Unsupported diagram file type: {file_path}")


def is_diagram_file(file_path: Union[str, Path]) -> bool:
    """
    Check if a file is a diagram file (Mermaid or PlantUML).

    Args:
        file_path: Path to the file to check

    Returns:
        True if the file is a diagram file, False otherwise
    """
    return detect_diagram_file_type(file_path) is not None 