"""
Command-line interface for PyDiagrams.

This module provides a command-line interface for generating diagrams from Mermaid or PlantUML files.
"""

import argparse
import os
import sys
from pathlib import Path

from pydiagrams.parsers.diagram_utils import (
    generate_diagram_from_file,
    detect_diagram_file_type,
    is_diagram_file
)


def main():
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate diagrams from Mermaid or PlantUML files."
    )
    
    parser.add_argument(
        "file",
        help="Path to the Mermaid or PlantUML file"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Path to the output file (default: same name as input with appropriate extension)"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["svg", "png"],
        default="svg",
        help="Output format (default: svg)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Check if the input file exists
    input_file = Path(args.file)
    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Check if the input file is a Mermaid or PlantUML file
    if not is_diagram_file(input_file):
        print(f"Error: Not a Mermaid or PlantUML file: {input_file}")
        sys.exit(1)
    
    # Determine output path
    output_path = args.output
    if not output_path:
        output_path = input_file.with_suffix(f".{args.format}")
    
    if args.verbose:
        diagram_type = detect_diagram_file_type(input_file)
        print(f"Generating {args.format.upper()} diagram from {diagram_type.capitalize()} file: {input_file}")
        print(f"Output file: {output_path}")
    
    try:
        # Generate the diagram
        output_file = generate_diagram_from_file(
            input_file,
            output_path,
            args.format
        )
        
        if args.verbose:
            print(f"Successfully generated diagram: {output_file}")
    except Exception as e:
        print(f"Error generating diagram: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 