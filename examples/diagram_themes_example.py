#!/usr/bin/env python3
"""
Example demonstrating the theme system for HTML diagrams.
"""

import os
import sys
import webbrowser
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file


def main():
    """Run the example."""
    # Define paths to the example diagram files
    script_dir = Path(__file__).parent
    mermaid_file = script_dir / "mermaid_class_diagram.mmd"
    plantuml_file = script_dir / "plantuml_sequence_diagram.puml"
    output_dir = script_dir.parent / "output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Generate diagrams with different themes
    themes = {
        'default': 'Default theme with standard colors',
        'blue': 'Blue theme with Google-inspired colors',
        'green': 'Green theme with nature-inspired colors',
        'purple': 'Purple theme with creative colors',
        'high-contrast': 'High contrast theme for accessibility'
    }
    
    # Process the Mermaid file with different themes
    print("Generating Mermaid diagrams with different themes:")
    mermaid_outputs = {}
    
    for theme, description in themes.items():
        # Light mode
        output_file = output_dir / f"mermaid_{theme}_light.html"
        mermaid_outputs[f"{theme}_light"] = create_diagram_from_file(
            mermaid_file, 
            output_file, 
            output_format="html",
            theme=theme,
            dark_mode=False
        )
        print(f"  - {theme} (light): {output_file}")
        
        # Dark mode
        output_file = output_dir / f"mermaid_{theme}_dark.html"
        mermaid_outputs[f"{theme}_dark"] = create_diagram_from_file(
            mermaid_file, 
            output_file, 
            output_format="html",
            theme=theme,
            dark_mode=True
        )
        print(f"  - {theme} (dark): {output_file}")
    
    # Process the PlantUML file with different themes
    print("\nGenerating PlantUML diagrams with different themes:")
    plantuml_outputs = {}
    
    for theme, description in themes.items():
        # Light mode
        output_file = output_dir / f"plantuml_{theme}_light.html"
        plantuml_outputs[f"{theme}_light"] = create_diagram_from_file(
            plantuml_file, 
            output_file, 
            output_format="html",
            theme=theme,
            dark_mode=False
        )
        print(f"  - {theme} (light): {output_file}")
        
        # Dark mode
        output_file = output_dir / f"plantuml_{theme}_dark.html"
        plantuml_outputs[f"{theme}_dark"] = create_diagram_from_file(
            plantuml_file, 
            output_file, 
            output_format="html",
            theme=theme,
            dark_mode=True
        )
        print(f"  - {theme} (dark): {output_file}")
    
    # Ask to open some examples
    print("\nDo you want to open some example diagrams in your browser? (y/n)")
    choice = input().strip().lower()
    
    if choice in ('y', 'yes'):
        print("Opening examples in browser...")
        
        # Open a few examples
        examples_to_open = [
            ('default_light', mermaid_outputs['default_light']),
            ('default_dark', mermaid_outputs['default_dark']),
            ('blue_light', plantuml_outputs['blue_light']),
            ('high-contrast_dark', plantuml_outputs['high-contrast_dark'])
        ]
        
        for name, path in examples_to_open:
            print(f"Opening {name}: {path}")
            webbrowser.open(f"file://{path}")
            
            # Wait a moment before opening the next file
            import time
            time.sleep(1)
        
        print("\nIn the browser, you can:")
        print("1. Use the theme selector in the top-right corner to switch between themes")
        print("2. Toggle dark mode with the button in the top-right corner")
        print("3. Zoom and pan the diagram")
        print("4. Export the diagram to SVG, PNG, or PDF")


if __name__ == "__main__":
    main() 