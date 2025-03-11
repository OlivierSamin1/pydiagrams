"""
Mermaid renderer for SVG and PNG output.
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class MermaidRenderer:
    """Renderer for Mermaid diagrams."""
    
    def __init__(self):
        """Initialize the Mermaid renderer."""
        # Check if mmdc (Mermaid CLI) is installed
        self.has_mmdc = self._check_mmdc_installed()
        
        if not self.has_mmdc:
            print("Warning: 'mmdc' (Mermaid CLI) not found. Using fallback renderer.", file=sys.stderr)
            print("For best results, install the Mermaid CLI with: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
    
    def _check_mmdc_installed(self) -> bool:
        """
        Check if mmdc (Mermaid CLI) is installed.
        
        Returns:
            bool: True if mmdc is available, False otherwise
        """
        try:
            subprocess.run(['mmdc', '--version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          check=False)
            return True
        except FileNotFoundError:
            return False
    
    def render(self, diagram_data: Dict[str, Any], output_path: str, output_format: str = 'svg') -> str:
        """
        Render a Mermaid diagram to SVG or PNG.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: Path to save the rendered diagram
            output_format: Output format ('svg' or 'png')
            
        Returns:
            str: Path to the rendered diagram
        """
        if diagram_data['type'] != 'mermaid':
            raise ValueError(f"Mermaid renderer only supports Mermaid diagrams, got {diagram_data['type']}")
        
        diagram_content = diagram_data['raw_content']
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Choose rendering method
        if self.has_mmdc:
            return self._render_with_mmdc(diagram_content, output_path, output_format)
        else:
            return self._render_fallback(diagram_content, output_path, output_format)
    
    def _render_with_mmdc(self, diagram_content: str, output_path: str, output_format: str) -> str:
        """
        Render a Mermaid diagram using the Mermaid CLI.
        
        Args:
            diagram_content: Mermaid diagram content
            output_path: Path to save the rendered diagram
            output_format: Output format ('svg' or 'png')
            
        Returns:
            str: Path to the rendered diagram
        """
        # Create a temporary file for the Mermaid content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
            temp_file.write(diagram_content)
            temp_path = temp_file.name
        
        try:
            # Run mmdc
            cmd = [
                'mmdc',
                '-i', temp_path,
                '-o', output_path,
                '-t', 'default',  # TODO: Add support for themes
                '-b', 'transparent'
            ]
            
            if output_format == 'png':
                cmd.extend(['-p'])
            
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            return output_path
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_path)
            except Exception:
                pass
    
    def _render_fallback(self, diagram_content: str, output_path: str, output_format: str) -> str:
        """
        Fallback renderer when mmdc is not available.
        
        For now, just writes the Mermaid content to the output file with
        a message indicating that mmdc should be installed.
        
        Args:
            diagram_content: Mermaid diagram content
            output_path: Path to save the rendered diagram
            output_format: Output format ('svg' or 'png')
            
        Returns:
            str: Path to the output file
        """
        # Write the Mermaid content to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(diagram_content)
            f.write("\n\n# Note: Install Mermaid CLI for proper rendering: npm install -g @mermaid-js/mermaid-cli")
        
        print(f"Warning: Using fallback renderer. The output file contains the raw Mermaid content.", file=sys.stderr)
        return output_path 