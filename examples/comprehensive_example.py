#!/usr/bin/env python3
"""
Comprehensive example demonstrating all features of PyDiagrams.

This example shows how to:
1. Generate diagrams from Mermaid and PlantUML files
2. Use different output formats (SVG, PNG, HTML, PDF)
3. Apply dark mode styling
4. Use the interactive features
"""

import os
import sys
import subprocess
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
    
    # Part 2: Interactive HTML with light/dark mode
    print("\nPart 2: Interactive HTML")
    print("----------------------")
    
    # Generate HTML with light mode
    mermaid_html = output_dir / "mermaid_interactive.html"
    create_diagram_from_file(mermaid_file, mermaid_html, output_format="html")
    print(f"Generated interactive HTML from Mermaid: {mermaid_html}")
    
    # Generate HTML with dark mode
    plantuml_html = output_dir / "plantuml_interactive_dark.html"
    create_diagram_from_file(
        plantuml_file, 
        plantuml_html, 
        output_format="html",
        dark_mode=True
    )
    print(f"Generated interactive HTML from PlantUML with dark mode: {plantuml_html}")
    
    # Ask to open the interactive examples in your browser? (y/n)
    choice = input("Do you want to open the interactive examples in Brave browser? (y/n): ").strip().lower()
    
    if choice in ('y', 'yes'):
        print("Opening examples in Brave browser...")
        
        try:
            # Use absolute paths for the files
            mermaid_html_abs = os.path.abspath(mermaid_html)
            plantuml_html_abs = os.path.abspath(plantuml_html)
            
            # Open with Brave using command-line arguments to allow file access
            subprocess.run(["brave-browser", "--allow-file-access-from-files", f"file://{mermaid_html_abs}"])
            
            # Wait a moment before opening the next file
            import time
            time.sleep(1)
            
            subprocess.run(["brave-browser", "--allow-file-access-from-files", f"file://{plantuml_html_abs}"])
            
            print("\nInteractive Features:")
            print("1. Zoom and Pan: Use the zoom controls or mouse wheel to zoom, click and drag to pan")
            print("2. Dark Mode: Toggle dark mode with the button in the top-right corner")
            print("3. Export: Click the Export button to save as SVG, PNG, or PDF")
            
            print("\nCommand-line Equivalent:")
            print(f"pydiagrams {mermaid_file} -o {mermaid_html} -f html --open")
            print(f"pydiagrams {plantuml_file} -o {plantuml_html} -f html --dark-mode --open")
        except Exception as e:
            print(f"Error opening browser: {e}")
            print("You can manually open the files in Brave with the --allow-file-access-from-files flag:")
            print(f"brave-browser --allow-file-access-from-files file://{mermaid_html_abs}")
            print(f"brave-browser --allow-file-access-from-files file://{plantuml_html_abs}")


if __name__ == "__main__":
    main() 