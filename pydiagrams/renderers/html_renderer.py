"""
HTML Renderer for PyDiagrams.

This module provides functionality to render diagrams as interactive HTML.
"""

import os
import base64
import zlib
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader


class HTMLRenderer:
    def _convert_plantuml_to_mermaid(self, content):
        """
        Convert PlantUML diagram to Mermaid format
        
        Args:
            content: PlantUML diagram content
            
        Returns:
            Mermaid diagram content
        """
        import re
        
        # Remove @startuml and @enduml tags
        content = re.sub(r'@startuml.*?\n', '', content)
        content = re.sub(r'@enduml.*?\n', '', content)
        
        # Detect diagram type
        content_lower = content.lower()
        if "actor" in content_lower or "participant" in content_lower or "->" in content_lower and not "class" in content_lower:
            # Sequence diagram
            # Convert title
            title_match = re.search(r'title\s+(.*?)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                content = re.sub(r'title\s+.*?\n', '', content)
                mermaid_title = f"sequenceDiagram\n    title: {title}\n"
            else:
                mermaid_title = "sequenceDiagram\n"
            
            # Convert participants
            participant_pattern = r'participant\s+"([^"]+)"\s+as\s+(\w+)'
            actor_pattern = r'actor\s+"([^"]+)"\s+as\s+(\w+)'
            database_pattern = r'database\s+"([^"]+)"\s+as\s+(\w+)'
            
            def convert_participant_line(match):
                name = match.group(1)
                alias = match.group(2)
                return f"    participant {alias} as \"{name}\""
            
            content = re.sub(participant_pattern, convert_participant_line, content)
            content = re.sub(actor_pattern, lambda m: f"    actor {m.group(2)} as \"{m.group(1)}\"", content)
            content = re.sub(database_pattern, lambda m: f"    participant {m.group(2)} as \"{m.group(1)}\"", content)
            
            # Simple participants without quotes or aliases
            content = re.sub(r'participant\s+(\w+)\s*$', r'    participant \1', content, flags=re.MULTILINE)
            content = re.sub(r'actor\s+(\w+)\s*$', r'    actor \1', content, flags=re.MULTILINE)
            content = re.sub(r'database\s+(\w+)\s*$', r'    participant \1', content, flags=re.MULTILINE)
            
            # Convert arrows
            content = re.sub(r'(\w+)\s*->\s*(\w+)\s*:\s*(.*?)$', r'    \1->>\2: \3', content, flags=re.MULTILINE)
            content = re.sub(r'(\w+)\s*-->\s*(\w+)\s*:\s*(.*?)$', r'    \1-->>\2: \3', content, flags=re.MULTILINE)
            
            # Handle activation/deactivation
            content = re.sub(r'activate\s+(\w+)', r'    activate \1', content)
            content = re.sub(r'deactivate\s+(\w+)', r'    deactivate \1', content)
            
            # Handle notes
            content = re.sub(r'note\s+(?:left|right)\s+of\s+(\w+)\s*:\s*(.*?)$', 
                            r'    Note \1: \2', content, flags=re.MULTILINE)
            
            return mermaid_title + content.strip()
        
        elif "class" in content_lower or "<|--" in content_lower:
            # Class diagram
            mermaid_content = "classDiagram\n"
            
            # Placeholder for full class diagram conversion
            return mermaid_content + "    " + content.strip().replace('\n', '\n    ')
            
        else:
            # Default to flowchart for other diagram types
            return f"graph TD\n    A[PlantUML converted to Mermaid]\n    B[Some features may not be fully supported]\n    A --> B"
    
    """Renderer for HTML output format."""
    
    # Default PlantUML server URL
    PLANTUML_SERVER = "http://www.plantuml.com/plantuml"
    
    def __init__(self, width: int = 800, height: int = 600, interactive: bool = True, 
                 dark_mode: bool = False, inline_resources: bool = False):
        """
        Initialize the HTML renderer.
        
        Args:
            width: Canvas width
            height: Canvas height
            interactive: Whether to enable interactive features
            dark_mode: Whether to use dark mode
            inline_resources: Whether to inline CSS and JS resources (avoids CORS issues)
        """
        self.width = width
        self.height = height
        self.interactive = interactive
        self.dark_mode = dark_mode
        self.inline_resources = inline_resources
        
        # Set up Jinja2 environment
        templates_dir = Path(__file__).parent / 'templates'
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Static files directory
        self.static_dir = Path(__file__).parent / 'static'
        
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
        
        # Create a directory for static files if not inlining resources
        output_path_obj = Path(output_path)
        static_url = f"{output_path_obj.stem}_files"
        
        if not self.inline_resources:
            static_output_dir = output_path_obj.parent / static_url
            if not static_output_dir.exists():
                static_output_dir.mkdir(exist_ok=True)
                
                # Copy CSS files
                css_dir = static_output_dir / 'css'
                css_dir.mkdir(exist_ok=True)
                shutil.copy(self.static_dir / 'css' / 'themes.css', css_dir)
                
                # Copy JS files
                js_dir = static_output_dir / 'js'
                js_dir.mkdir(exist_ok=True)
                shutil.copy(self.static_dir / 'js' / 'themes.js', js_dir)
        
        # Prepare context for template
        context = {
            'title': diagram_data.get('title', f'{diagram_type.capitalize()} Diagram'),
            'width': self.width,
            'height': self.height,
            'interactive': self.interactive,
            'dark_mode': self.dark_mode,
            'inline_resources': self.inline_resources,
            'static_url': static_url
        }
        
        # If inlining resources, add the CSS and JS content to the context
        if self.inline_resources:
            css_file = self.static_dir / 'css' / 'themes.css'
            js_file = self.static_dir / 'js' / 'themes.js'
            
            with open(css_file, 'r', encoding='utf-8') as f:
                context['inline_css'] = f.read()
                
            with open(js_file, 'r', encoding='utf-8') as f:
                context['inline_js'] = f.read()
                
            # Set Mermaid to use UMD/IIFE format instead of ESM for better compatibility
            context['use_mermaid_umd'] = True
        
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
            
            # Convert PlantUML to Mermaid as a fallback
            try:
                context['mermaid_content'] = self._convert_plantuml_to_mermaid(context['diagram_content'])
            except Exception as e:
                print(f"Warning: Failed to convert PlantUML to Mermaid: {e}")
                # Safely escape any quotes in the error message
                error_msg = str(e).replace('"', '\\"')
                context['mermaid_content'] = f"graph TD\n    A[Error converting PlantUML to Mermaid]"
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