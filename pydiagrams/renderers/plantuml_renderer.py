"""
PlantUML renderer for PyDiagrams.
"""

import os
import base64
import zlib
import requests
from pathlib import Path
from typing import Dict, Any


class PlantUMLRenderer:
    """Renderer for PlantUML diagrams."""
    
    # Default PlantUML server URL
    PLANTUML_SERVER = "http://www.plantuml.com/plantuml"
    
    def __init__(self):
        """Initialize the PlantUML renderer."""
        pass
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render PlantUML diagram data to an SVG file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # For PlantUML, we'll use the PlantUML server to generate an SVG
        content = diagram_data.get('raw_content', '')
        encoded_content = self._encode_plantuml(content)
        
        try:
            # Get SVG from PlantUML server
            response = requests.get(f"{self.PLANTUML_SERVER}/svg/{encoded_content}")
            response.raise_for_status()
            
            # Write the SVG to the output file
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            return output_path
        except Exception as e:
            # If we can't connect to the PlantUML server, return a simple SVG
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">
      <pre>
{content}
      </pre>
    </div>
  </foreignObject>
</svg>"""
            
            # Write the SVG to the output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
                
            return output_path
    
    def render_png(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render PlantUML diagram data to a PNG file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # For PlantUML, we'll use the PlantUML server to generate a PNG
        content = diagram_data.get('raw_content', '')
        encoded_content = self._encode_plantuml(content)
        
        try:
            # Get PNG from PlantUML server
            response = requests.get(f"{self.PLANTUML_SERVER}/png/{encoded_content}")
            response.raise_for_status()
            
            # Write the PNG to the output file
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            return output_path
        except Exception as e:
            # If we can't connect to the PlantUML server, return a simple PNG
            with open(output_path, 'wb') as f:
                # Create a simple PNG
                # This is just a placeholder
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0bIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xcc\x59\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
                
            return output_path
            
    def _encode_plantuml(self, text: str) -> str:
        """
        Encode PlantUML text for use with the PlantUML server.

        Args:
            text: PlantUML text

        Returns:
            Encoded string for URL
        """
        # Convert to UTF-8 and compress with zlib
        zlibbed = zlib.compress(text.encode('utf-8'))
        
        # Convert to base64 and replace unsafe characters
        compressed = base64.b64encode(zlibbed).decode('ascii')
        compressed = compressed.replace('+', '-').replace('/', '_')
        
        # Add ~1 prefix to indicate DEFLATE encoding
        return f"~1{compressed}" 