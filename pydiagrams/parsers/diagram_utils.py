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
    output_format: str = 'svg'
) -> str:
    """
    Generate a diagram from a Mermaid or PlantUML file.

    Args:
        file_path: Path to the diagram file
        output_path: Path where to save the generated diagram (if None, it will use the input filename with appropriate extension)
        output_format: Output format ('svg', 'png')

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
    
    if diagram_type == 'mermaid':
        # For Mermaid, we'll create a simple SVG with a reference to the Mermaid content
        # In a real implementation, we would use a Mermaid renderer
        with open(file_path, 'r') as f:
            mermaid_content = f.read()
        
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <pre class="mermaid">
{mermaid_content}
      </pre>
      <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
      <script>mermaid.initialize({{startOnLoad:true}});</script>
    </div>
  </foreignObject>
</svg>"""
        
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return str(output_path)
    elif diagram_type == 'plantuml':
        # For PlantUML, we'll create a simple text file with a reference to the PlantUML content
        # In a real implementation, we would use a PlantUML renderer
        with open(file_path, 'r') as f:
            plantuml_content = f.read()
        
        if output_format.lower() == 'svg':
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <text x="10" y="20" font-family="monospace">PlantUML Diagram:</text>
  <foreignObject width="100%" height="100%" y="30">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <pre style="font-family: monospace; white-space: pre-wrap;">
{plantuml_content}
      </pre>
    </div>
  </foreignObject>
</svg>"""
            
            with open(output_path, 'w') as f:
                f.write(svg_content)
        else:
            # For PNG, we'll create a simple text file
            with open(output_path, 'wb') as f:
                # Create a simple PNG with the text "PlantUML Diagram"
                # In a real implementation, we would use a PlantUML renderer
                # This is just a placeholder
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
        
        return str(output_path)
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