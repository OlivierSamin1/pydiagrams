#!/usr/bin/env python3
"""
Example demonstrating how to generate diagrams from Mermaid or PlantUML files.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import (
    detect_diagram_file_type,
    parse_diagram_file,
    generate_diagram_from_file,
    is_diagram_file
)


def main():
    """Run the example."""
    # Define paths to the example diagram files
    script_dir = Path(__file__).parent
    mermaid_file = script_dir / "mermaid_class_diagram.mmd"
    plantuml_file = script_dir / "plantuml_sequence_diagram.puml"
    output_dir = script_dir.parent / "output"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Process the Mermaid file
    print(f"Processing Mermaid file: {mermaid_file}")
    if is_diagram_file(mermaid_file):
        diagram_type = detect_diagram_file_type(mermaid_file)
        print(f"Detected diagram type: {diagram_type}")
        
        # Parse the diagram
        data, parser = parse_diagram_file(mermaid_file)
        print(f"Parsed diagram data: {data['type']} diagram with {len(data.get('classes', []))} classes")
        
        # Generate the diagram
        output_file = output_dir / "mermaid_class_diagram.svg"
        result = generate_diagram_from_file(mermaid_file, output_file)
        print(f"Generated diagram: {result}")
    else:
        print(f"Not a valid diagram file: {mermaid_file}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Process the PlantUML file
    print(f"Processing PlantUML file: {plantuml_file}")
    if is_diagram_file(plantuml_file):
        diagram_type = detect_diagram_file_type(plantuml_file)
        print(f"Detected diagram type: {diagram_type}")
        
        # Parse the diagram
        data, parser = parse_diagram_file(plantuml_file)
        print(f"Parsed diagram data: {data['type']} diagram with {len(data.get('participants', []))} participants")
        
        # Generate the diagram as SVG
        output_file = output_dir / "plantuml_sequence_diagram.svg"
        result = generate_diagram_from_file(plantuml_file, output_file, "svg")
        print(f"Generated SVG diagram: {result}")
        
        # Generate the diagram as PNG
        output_file = output_dir / "plantuml_sequence_diagram.png"
        result = generate_diagram_from_file(plantuml_file, output_file, "png")
        print(f"Generated PNG diagram: {result}")
    else:
        print(f"Not a valid diagram file: {plantuml_file}")


if __name__ == "__main__":
    main() 