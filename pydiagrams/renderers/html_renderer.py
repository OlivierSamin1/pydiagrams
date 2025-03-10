"""
HTML Renderer for PyDiagrams.

This module provides functionality to render diagrams as interactive HTML.
"""

import os
import base64
import zlib
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader


class HTMLRenderer:
    """Renderer for HTML output format."""
    
    # Default PlantUML server URL
    PLANTUML_SERVER = "http://www.plantuml.com/plantuml"
    
    def __init__(self, width: int = 800, height: int = 600, interactive: bool = True):
        """
        Initialize the HTML renderer.
        
        Args:
            width: Canvas width
            height: Canvas height
            interactive: Whether to enable interactive features
        """
        self.width = width
        self.height = height
        self.interactive = interactive
        
        # Set up Jinja2 environment
        templates_dir = Path(__file__).parent / 'templates'
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render diagram data to an HTML file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # Create the output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Get diagram type and content
        diagram_type = diagram_data.get('type', 'unknown')
        
        # Prepare context for template
        context = {
            'title': diagram_data.get('title', f'{diagram_type.capitalize()} Diagram'),
            'width': self.width,
            'height': self.height,
            'interactive': self.interactive,
        }
        
        # Choose the appropriate template based on diagram type
        if diagram_type == 'mermaid':
            template = self.env.get_template('mermaid.html')
            # Add the raw Mermaid content to the context
            context['diagram_content'] = diagram_data.get('raw_content', '')
        elif diagram_type == 'plantuml':
            template = self.env.get_template('plantuml.html')
            # Add the raw PlantUML content to the context
            context['diagram_content'] = diagram_data.get('raw_content', '')
            # Generate image URL for PlantUML
            encoded_content = self._encode_plantuml(context['diagram_content'])
            context['diagram_image_url'] = f"{self.PLANTUML_SERVER}/svg/{encoded_content}"
            context['plantuml_server'] = self.PLANTUML_SERVER
        else:
            # For other diagram types, we'll need to implement custom templates
            # For now, let's use a generic template
            template = self.env.get_template('base.html')
            context['diagram_content'] = 'Unsupported diagram type'
        
        # Render the template
        html_content = template.render(**context)
        
        # Write the HTML to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _encode_plantuml(self, text: str) -> str:
        """
        Encode PlantUML text for use with the PlantUML server.

        Args:
            text: PlantUML text

        Returns:
            Encoded string for URL
        """
        # Add the ~1 prefix to indicate DEFLATE encoding
        # Convert to UTF-8 and compress with zlib
        zlibbed = zlib.compress(text.encode('utf-8'))
        
        # Convert to base64 and replace unsafe characters
        compressed = base64.b64encode(zlibbed).decode('ascii')
        compressed = compressed.replace('+', '-').replace('/', '_')
        
        # Add ~1 prefix to indicate DEFLATE encoding
        return f"~1{compressed}" 