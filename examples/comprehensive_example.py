#!/usr/bin/env python3
"""
Comprehensive example demonstrating all features of PyDiagrams.

This example shows how to:
1. Generate diagrams from Mermaid and PlantUML files
2. Use different output formats (SVG, PNG, HTML, PDF)
3. Apply themes and styling
4. Use the interactive features
"""

import os
import sys
import webbrowser
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file


def main():
    """Run the comprehensive example."""
    # Define paths to the example diagram files
    script_dir = Path(__file__).parent
    mermaid_file = script_dir / "mermaid_class_diagram.mmd"
    plantuml_file = script_dir / "plantuml_sequence_diagram.puml"
    output_dir = script_dir.parent / "output" / "comprehensive_example"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print("PyDiagrams Comprehensive Example")
    print("================================\n")
    
    # Part 1: Basic diagram generation
    print("Part 1: Basic Diagram Generation")
    print("-------------------------------")
    
    # Generate SVG from Mermaid
    mermaid_svg = output_dir / "mermaid_diagram.svg"
    create_diagram_from_file(mermaid_file, mermaid_svg)
    print(f"Generated SVG from Mermaid: {mermaid_svg}")
    
    # Generate PNG from PlantUML
    plantuml_png = output_dir / "plantuml_diagram.png"
    create_diagram_from_file(plantuml_file, plantuml_png, output_format="png")
    print(f"Generated PNG from PlantUML: {plantuml_png}")
    
    # Part 2: Interactive HTML with themes
    print("\nPart 2: Interactive HTML with Themes")
    print("-----------------------------------")
    
    # Generate HTML with default theme
    mermaid_html = output_dir / "mermaid_interactive.html"
    create_diagram_from_file(mermaid_file, mermaid_html, output_format="html")
    print(f"Generated interactive HTML from Mermaid: {mermaid_html}")
    
    # Generate HTML with blue theme and dark mode
    plantuml_html = output_dir / "plantuml_interactive.html"
    create_diagram_from_file(
        plantuml_file, 
        plantuml_html, 
        output_format="html",
        theme="blue",
        dark_mode=True
    )
    print(f"Generated interactive HTML from PlantUML (Blue theme, Dark mode): {plantuml_html}")
    
    # Part 3: Accessibility options
    print("\nPart 3: Accessibility Options")
    print("----------------------------")
    
    # Generate HTML with high contrast theme
    accessibility_html = output_dir / "accessibility_example.html"
    create_diagram_from_file(
        mermaid_file, 
        accessibility_html, 
        output_format="html",
        theme="high-contrast"
    )
    print(f"Generated accessible HTML diagram: {accessibility_html}")
    
    # Ask to open the examples
    print("\nDo you want to open the interactive examples in your browser? (y/n)")
    choice = input().strip().lower()
    
    if choice in ('y', 'yes'):
        print("Opening examples in browser...")
        
        # Open the interactive examples
        webbrowser.open(f"file://{mermaid_html}")
        
        # Wait a moment before opening the next file
        import time
        time.sleep(1)
        
        webbrowser.open(f"file://{plantuml_html}")
        
        print("\nInteractive Features:")
        print("1. Zoom and Pan: Use the zoom controls or mouse wheel to zoom, click and drag to pan")
        print("2. Theme Selection: Use the theme selector in the top-right corner")
        print("3. Dark Mode: Toggle dark mode with the button in the top-right corner")
        print("4. Export: Click the Export button to save as SVG, PNG, or PDF")
        
        print("\nCommand-line Equivalent:")
        print(f"pydiagrams {mermaid_file} -o {mermaid_html} -f html --open")
        print(f"pydiagrams {plantuml_file} -o {plantuml_html} -f html --theme blue --dark-mode --open")


if __name__ == "__main__":
    main() 