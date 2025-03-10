#!/usr/bin/env python3
"""
Example demonstrating how to export diagrams to various formats with enhanced quality.
"""

import os
import sys
import webbrowser
import subprocess
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
    
    # Process the Mermaid file to HTML
    print(f"Processing Mermaid file to HTML: {mermaid_file}")
    mermaid_html = output_dir / "mermaid_export_example.html"
    mermaid_output = create_diagram_from_file(mermaid_file, mermaid_html, output_format="html")
    print(f"Generated HTML: {mermaid_output}")
    
    # Process the PlantUML file to HTML
    print(f"\nProcessing PlantUML file to HTML: {plantuml_file}")
    plantuml_html = output_dir / "plantuml_export_example.html"
    plantuml_output = create_diagram_from_file(plantuml_file, plantuml_html, output_format="html")
    print(f"Generated HTML: {plantuml_output}")
    
    # Generate direct exports for comparison
    print("\nGenerating direct exports for comparison:")
    
    # Mermaid SVG
    mermaid_svg = output_dir / "mermaid_direct_export.svg"
    create_diagram_from_file(mermaid_file, mermaid_svg, output_format="svg")
    print(f"Generated Mermaid SVG: {mermaid_svg}")
    
    # PlantUML SVG
    plantuml_svg = output_dir / "plantuml_direct_export.svg"
    create_diagram_from_file(plantuml_file, plantuml_svg, output_format="svg")
    print(f"Generated PlantUML SVG: {plantuml_svg}")
    
    # PlantUML PNG
    plantuml_png = output_dir / "plantuml_direct_export.png"
    create_diagram_from_file(plantuml_file, plantuml_png, output_format="png")
    print(f"Generated PlantUML PNG: {plantuml_png}")
    
    # Ask to open the HTML files in a browser
    print("\nDo you want to open the HTML files in your browser to test the export functionality? (y/n)")
    choice = input().strip().lower()
    
    if choice in ('y', 'yes'):
        print("Opening files in browser...")
        
        # Open Mermaid HTML in browser
        mermaid_url = f"file://{mermaid_output}"
        webbrowser.open(mermaid_url)
        
        # Wait a moment before opening the second file
        import time
        time.sleep(1)
        
        # Open PlantUML HTML in browser
        plantuml_url = f"file://{plantuml_output}"
        webbrowser.open(plantuml_url)
        
        print("\nIn the browser, you can:")
        print("1. Use the 'Export' button to open the export dialog")
        print("2. Choose a filename and quality setting")
        print("3. Export to SVG, PNG, or PDF format")
        print("4. Compare the quality with the direct exports")


if __name__ == "__main__":
    main() 