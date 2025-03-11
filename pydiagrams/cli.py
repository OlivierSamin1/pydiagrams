#!/usr/bin/env python3
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
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        description='Generate diagrams from Mermaid files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate SVG from a Mermaid file (default)
  pydiagrams my_diagram.mmd -o output.svg
  
  # Generate PNG from a Mermaid file
  pydiagrams my_diagram.mmd -o output.png -f png
  
  # Generate interactive HTML with a theme and dark mode
  pydiagrams my_diagram.mmd -o output.html -f html --theme blue --dark-mode
  
  # Generate HTML with inline resources for better portability
  pydiagrams my_diagram.mmd -o output.html -f html --inline-resources
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Input diagram file (Mermaid .mmd)'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='Output file path (default: same as input with appropriate extension)'
    )
    
    parser.add_argument(
        '-f', '--format',
        dest='output_format',
        choices=['svg', 'png', 'html'],
        default='svg',
        help='Output format (default: svg)'
    )
    
    parser.add_argument(
        '--theme',
        dest='theme',
        choices=['default', 'forest', 'dark', 'neutral', 'blue', 'high-contrast'],
        default='default',
        help='Theme for HTML output (default: default)'
    )
    
    parser.add_argument(
        '--dark-mode',
        dest='dark_mode',
        action='store_true',
        help='Use dark mode for HTML output'
    )
    
    parser.add_argument(
        '--inline-resources',
        dest='inline_resources',
        action='store_true',
        help='Inline CSS and JS resources in HTML output for better portability'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}", file=sys.stderr)
        return 1
    
    try:
        # Detect diagram type to validate it's supported
        diagram_type = detect_diagram_file_type(args.input_file)
        
        if diagram_type != 'mermaid':
            print(f"Error: Only Mermaid diagrams are supported. Found: {diagram_type}", file=sys.stderr)
            return 1
            
        # Set output file if not provided
        if not args.output_file:
            input_path = Path(args.input_file)
            args.output_file = str(input_path.with_suffix(f'.{args.output_format}'))
        
        # Generate the diagram
        output_path = generate_diagram_from_file(
            args.input_file,
            args.output_file,
            output_format=args.output_format,
            theme=args.theme,
            dark_mode=args.dark_mode,
            inline_resources=args.inline_resources
        )
        
        print(f"Generated {args.output_format.upper()} diagram: {output_path}")
        return 0
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main()) 