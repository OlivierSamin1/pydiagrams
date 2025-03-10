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
        choices=["svg", "png", "html", "pdf"],
        default="svg",
        help="Output format (default: svg)"
    )
    
    parser.add_argument(
        "-q", "--quality",
        type=float,
        default=2.0,
        help="Quality factor for export (1.0-3.0, default: 2.0)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the resulting file after generation (particularly useful for HTML)"
    )
    
    parser.add_argument(
        "--theme",
        choices=["default", "blue", "green", "purple", "high-contrast"],
        default="default",
        help="Theme for HTML output (default: default)"
    )
    
    parser.add_argument(
        "--dark-mode",
        action="store_true",
        help="Use dark mode for HTML output"
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
        print(f"Quality: {args.quality}")
        if args.format == "html":
            print(f"Theme: {args.theme}")
            print(f"Dark mode: {'enabled' if args.dark_mode else 'disabled'}")
    
    try:
        # Generate the diagram
        output_file = generate_diagram_from_file(
            input_file,
            output_path,
            args.format,
            args.theme,
            args.dark_mode
        )
        
        if args.verbose:
            print(f"Successfully generated diagram: {output_file}")
            
        # Open the file if requested
        if args.open:
            if args.verbose:
                print(f"Opening {output_file}...")
                
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{output_file}"')
            elif sys.platform == 'win32':  # Windows
                os.system(f'start "" "{output_file}"')
            else:  # Linux and others
                os.system(f'xdg-open "{output_file}"')
    except Exception as e:
        print(f"Error generating diagram: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 