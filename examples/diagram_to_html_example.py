#!/usr/bin/env python3
"""
Example demonstrating how to generate HTML diagrams from Mermaid or PlantUML files.
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
    
    # Process the Mermaid file to HTML
    print(f"Processing Mermaid file to HTML: {mermaid_file}")
    mermaid_html = output_dir / "mermaid_class_diagram.html"
    mermaid_output = create_diagram_from_file(mermaid_file, mermaid_html, output_format="html")
    print(f"Generated HTML: {mermaid_output}")
    
    # Process the PlantUML file to HTML
    print(f"\nProcessing PlantUML file to HTML: {plantuml_file}")
    plantuml_html = output_dir / "plantuml_sequence_diagram.html"
    plantuml_output = create_diagram_from_file(plantuml_file, plantuml_html, output_format="html")
    print(f"Generated HTML: {plantuml_output}")
    
    # Ask to open the files in a browser
    print("\nDo you want to open these files in your browser? (y/n)")
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


if __name__ == "__main__":
    main() 