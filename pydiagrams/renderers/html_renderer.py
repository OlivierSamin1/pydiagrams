"""
HTML renderer for Mermaid diagrams.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

THEMES = [
    "default", 
    "forest", 
    "dark", 
    "neutral", 
    "blue",
    "high-contrast"
]

class HTMLRenderer:
    """Renderer for diagrams in HTML format with themes and interactive features."""
    
    def __init__(
        self, 
        width: int = 800, 
        height: int = 600, 
        interactive: bool = True,
        dark_mode: bool = False,
        inline_resources: bool = True
    ):
        """
        Initialize HTML renderer.
        
        Args:
            width: Width of the diagram in pixels
            height: Height of the diagram in pixels
            interactive: Whether to make the diagram interactive
            dark_mode: Whether to use dark mode
            inline_resources: Whether to inline CSS and JS resources
        """
        self.width = width
        self.height = height
        self.interactive = interactive
        self.dark_mode = dark_mode
        self.inline_resources = inline_resources
        
        # Get templates directory
        self.templates_dir = Path(__file__).parent / "templates"
        
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")
    
    def get_template(self, template_name: str) -> str:
        """
        Get a template from the templates directory.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            str: Content of the template file
        """
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def inject_resources(self, html_content: str) -> str:
        """
        Inject CSS and JS resources inline into the HTML content if inline_resources is True.
        
        Args:
            html_content: HTML content to inject resources into
            
        Returns:
            str: HTML content with resources injected
        """
        if not self.inline_resources:
            return html_content
            
        # Read CSS file
        css_path = self.templates_dir / "themes.css"
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
                html_content = html_content.replace(
                    '<link rel="stylesheet" href="themes.css">',
                    f'<style>{css_content}</style>'
                )
        
        # Read JS file
        js_path = self.templates_dir / "themes.js"
        if js_path.exists():
            with open(js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
                html_content = html_content.replace(
                    '<script src="themes.js"></script>',
                    f'<script>{js_content}</script>'
                )
                
        # Read Mermaid JS
        mermaid_js_path = self.templates_dir / "mermaid.min.js"
        if mermaid_js_path.exists():
            with open(mermaid_js_path, 'r', encoding='utf-8') as f:
                mermaid_js_content = f.read()
                html_content = html_content.replace(
                    '<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>',
                    f'<script>{mermaid_js_content}</script>'
                )
        
        return html_content
    
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render a diagram to HTML.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: Path to save the rendered HTML
            
        Returns:
            str: Path to the rendered HTML file
        """
        if diagram_data['type'] != 'mermaid':
            raise ValueError(f"HTML renderer only supports Mermaid diagrams, got {diagram_data['type']}")
        
        # Get base HTML template
        base_template = self.get_template("base.html")
        
        # Get mermaid template
        mermaid_template = self.get_template("mermaid.html")
        
        # Set diagram content
        diagram_content = diagram_data['raw_content']
        
        # Get diagram title
        title = diagram_data.get('title', 'Mermaid Diagram')
        
        # Apply template
        mermaid_html = mermaid_template.replace("{{diagram_content}}", diagram_content)
        
        # Apply theme if specified
        theme = diagram_data.get('theme', 'default')
        if theme not in THEMES:
            print(f"Warning: Theme '{theme}' not found, using default theme instead")
            theme = 'default'
        
        # Replace theme and dark mode placeholders
        html_content = base_template.replace("{{title}}", title)
        html_content = html_content.replace("{{body_content}}", mermaid_html)
        html_content = html_content.replace("{{theme}}", theme)
        html_content = html_content.replace("{{dark_mode}}", str(self.dark_mode).lower())
        
        # Create width and height styles
        html_content = html_content.replace("{{width}}", str(self.width))
        html_content = html_content.replace("{{height}}", str(self.height))
        
        # Inject resources if requested
        if self.inline_resources:
            html_content = self.inject_resources(html_content)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path 