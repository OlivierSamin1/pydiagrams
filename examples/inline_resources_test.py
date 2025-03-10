#!/usr/bin/env python3
"""
Test script to verify that inline resources work correctly.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file


def open_browser(file_path):
    """Open a file in a browser with appropriate flags."""
    abs_path = os.path.abspath(file_path)
    print(f"Opening {abs_path} in browser...")
    
    # Try different executable names for Brave
    brave_commands = ["brave", "brave-browser", "brave-browser-stable"]
    opened = False
    
    for cmd in brave_commands:
        try:
            subprocess.run([cmd, f"file://{abs_path}"])
            opened = True
            break
        except FileNotFoundError:
            continue
    
    if not opened:
        # As a fallback, try the default browser
        if sys.platform == "linux":
            subprocess.run(["xdg-open", f"file://{abs_path}"])
        elif sys.platform == "darwin":
            subprocess.run(["open", f"file://{abs_path}"])
        elif sys.platform == "win32":
            os.startfile(abs_path)
        else:
            print("Could not determine how to open browser on this platform.")
    
    return abs_path


def test_with_inline_resources():
    """Test generating HTML with inline resources."""
    print("=== Test: HTML Generation with Inline Resources ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "inline_test"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Use the test Mermaid file
    script_dir = Path(__file__).parent
    mermaid_file = script_dir / "test_diagram.mmd"
    
    if not mermaid_file.exists():
        print(f"Error: Test file {mermaid_file} does not exist.")
        return
    
    # Generate HTML with inline resources
    output_file = output_dir / "inline_resources_test.html"
    print(f"Generating HTML with inline resources from: {mermaid_file}")
    create_diagram_from_file(
        mermaid_file, 
        output_file, 
        output_format="html", 
        inline_resources=True
    )
    
    print(f"Generated file: {output_file}")
    
    # Check the file size
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size} bytes")
    
    # Open in browser
    try:
        abs_path = open_browser(output_file)
        print("\nInstructions:")
        print("1. The diagram should render properly without any error messages in the console")
        print("2. Dark mode toggle should work")
        print("3. Pan and zoom should work")
        print("4. Export options should work")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file: file://{os.path.abspath(output_file)}")


def test_with_plantuml():
    """Test generating PlantUML HTML with inline resources."""
    print("\n=== Test: PlantUML HTML Generation with Inline Resources ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "inline_test"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Use the test PlantUML file
    script_dir = Path(__file__).parent
    plantuml_file = script_dir / "plantuml_test_diagram.puml"
    
    if not plantuml_file.exists():
        print(f"Error: Test file {plantuml_file} does not exist.")
        return
    
    # Generate HTML with inline resources
    output_file = output_dir / "plantuml_inline_resources_test.html"
    print(f"Generating HTML with inline resources from: {plantuml_file}")
    create_diagram_from_file(
        plantuml_file, 
        output_file, 
        output_format="html", 
        inline_resources=True
    )
    
    print(f"Generated file: {output_file}")
    
    # Check the file size
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size} bytes")
    
    # Open in browser
    try:
        abs_path = open_browser(output_file)
        print("\nInstructions:")
        print("1. The diagram should render properly without any error messages in the console")
        print("2. Dark mode toggle should work")
        print("3. Pan and zoom should work")
        print("4. Export options should work")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file: file://{os.path.abspath(output_file)}")


def main():
    """Run all tests."""
    print("PyDiagrams Inline Resources Test")
    print("================================")
    
    test_with_inline_resources()
    test_with_plantuml()
    
    print("\nAll tests completed.")
    print("Check the browser to verify that diagrams are displayed correctly without CORS issues.")


if __name__ == "__main__":
    main() 