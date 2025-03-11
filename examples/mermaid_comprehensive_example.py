#!/usr/bin/env python3
"""
Comprehensive example showcasing PyDiagrams features with Mermaid diagrams.

This example demonstrates:
1. Generating SVG and PNG diagrams
2. Creating interactive HTML diagrams with themes
3. Using dark mode and theming
4. Using inline resources for better portability
"""

import os
import sys
import webbrowser
from pathlib import Path

# Add parent directory to path if running the script directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file


def main():
    """Run the comprehensive example."""
    # Define paths
    current_dir = Path(__file__).parent
    example_dir = current_dir / "mermaid_examples"
    output_dir = current_dir.parent / "output" / "comprehensive_example"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find example Mermaid files
    mermaid_files = list(example_dir.glob("*.mmd"))
    
    if not mermaid_files:
        print("No Mermaid example files found in:", example_dir)
        print("Creating a sample Mermaid file for demonstration...")
        
        # Create a sample Mermaid file
        example_dir.mkdir(exist_ok=True)
        sample_file = example_dir / "sample_flowchart.mmd"
        
        with open(sample_file, "w") as f:
            f.write("""graph TD
    A[Start] --> B{Is it a Mermaid diagram?}
    B -->|Yes| C[Process with PyDiagrams]
    B -->|No| D[Unsupported]
    C --> E[Export as SVG]
    C --> F[Export as PNG]
    C --> G[Create interactive HTML]
    G --> H[Apply themes]
    G --> I[Toggle dark mode]
    G --> J[Add zooming and panning]
""")
        
        mermaid_files = [sample_file]
    
    # Part 1: Basic SVG and PNG Generation
    print("\n=== Part 1: Basic Diagram Generation ===")
    
    # Choose a file to use for the examples
    mermaid_file = mermaid_files[0]
    print(f"Using Mermaid file: {mermaid_file}")
    
    # Generate SVG
    svg_output = output_dir / "diagram.svg"
    svg_path = create_diagram_from_file(
        str(mermaid_file),
        str(svg_output),
        output_format="svg"
    )
    print(f"Generated SVG: {svg_path}")
    
    # Generate PNG
    png_output = output_dir / "diagram.png"
    png_path = create_diagram_from_file(
        str(mermaid_file),
        str(png_output),
        output_format="png"
    )
    print(f"Generated PNG: {png_path}")
    
    # Part 2: Interactive HTML with Themes
    print("\n=== Part 2: Interactive HTML with Themes ===")
    
    # Generate default interactive HTML
    html_default_output = output_dir / "default_interactive.html"
    html_default_path = create_diagram_from_file(
        str(mermaid_file),
        str(html_default_output),
        output_format="html",
        theme="default",
        inline_resources=True
    )
    print(f"Generated interactive HTML with default theme: {html_default_path}")
    
    # Generate blue themed interactive HTML with dark mode
    html_themed_output = output_dir / "themed_interactive.html"
    html_themed_path = create_diagram_from_file(
        str(mermaid_file),
        str(html_themed_output),
        output_format="html",
        theme="blue",
        dark_mode=True,
        inline_resources=True
    )
    print(f"Generated interactive HTML with blue theme and dark mode: {html_themed_path}")
    
    # Part 3: Accessibility Options
    print("\n=== Part 3: Accessibility Options ===")
    
    # Generate high-contrast HTML
    html_accessible_output = output_dir / "accessible_interactive.html"
    html_accessible_path = create_diagram_from_file(
        str(mermaid_file),
        str(html_accessible_output),
        output_format="html",
        theme="high-contrast",
        inline_resources=True
    )
    print(f"Generated accessible HTML with high-contrast theme: {html_accessible_path}")
    
    # Open HTML files in browser
    print("\n=== Output Files ===")
    print(f"All generated files are in: {output_dir}")
    
    # Ask if user wants to open HTML examples
    open_browser = input("\nOpen HTML examples in browser? (y/n): ").lower() == 'y'
    
    if open_browser:
        print("Opening HTML examples in browser...")
        webbrowser.open(f"file://{html_default_path}")
        webbrowser.open(f"file://{html_themed_path}")
        webbrowser.open(f"file://{html_accessible_path}")
        
        print("\n=== Interactive Features ===")
        print("The HTML files include interactive features:")
        print("- Zoom and pan capabilities")
        print("- Theme selection (default, forest, dark, neutral, blue, high-contrast)")
        print("- Dark mode toggle")
        print("- Export options (SVG, PNG)")
        print("- Responsive design for different devices")
    
    # Show command-line equivalent commands
    print("\n=== Command-Line Equivalents ===")
    print("You can achieve the same results with these CLI commands:")
    print(f"pydiagrams {mermaid_file} -o {svg_output} -f svg")
    print(f"pydiagrams {mermaid_file} -o {png_output} -f png")
    print(f"pydiagrams {mermaid_file} -o {html_default_output} -f html --inline-resources")
    print(f"pydiagrams {mermaid_file} -o {html_themed_output} -f html --theme blue --dark-mode --inline-resources")
    print(f"pydiagrams {mermaid_file} -o {html_accessible_output} -f html --theme high-contrast --inline-resources")


if __name__ == "__main__":
    main() 