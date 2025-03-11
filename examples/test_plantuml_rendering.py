#!/usr/bin/env python3
"""
Test script to diagnose PlantUML rendering issues.
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file
from pydiagrams.renderers.html_renderer import HTMLRenderer


def test_plantuml_server_connection():
    """Test if we can connect to the PlantUML server."""
    print("Testing PlantUML server connection...")
    
    plantuml_server = HTMLRenderer.PLANTUML_SERVER
    print(f"Using PlantUML server: {plantuml_server}")
    
    try:
        response = requests.get(f"{plantuml_server}/png/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000")
        if response.status_code == 200:
            print("✓ Connection successful")
            print(f"  Response size: {len(response.content)} bytes")
            print(f"  Content type: {response.headers.get('Content-Type', 'unknown')}")
        else:
            print("✗ Connection failed")
            print(f"  Status code: {response.status_code}")
            print(f"  Response: {response.text[:100]}...")
    except Exception as e:
        print("✗ Connection failed with error:")
        print(f"  {str(e)}")


def open_browser(file_path):
    """Open a file in a browser with appropriate flags."""
    abs_path = os.path.abspath(file_path)
    print(f"Opening {abs_path} in browser...")
    
    # Try different executable names for Brave
    brave_commands = ["brave", "brave-browser", "brave-browser-stable"]
    opened = False
    
    for cmd in brave_commands:
        try:
            subprocess.run([cmd, "--allow-file-access-from-files", f"file://{abs_path}"])
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


def create_test_html():
    """Create a test HTML file with a PlantUML diagram using direct encoding."""
    print("\nCreating test HTML with PlantUML diagram...")
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_dir.mkdir(exist_ok=True, parents=True)
    test_file = output_dir / "plantuml_direct_test.html"
    
    # PlantUML encoded diagram - this is a simple sequence diagram
    # Encoding can be generated at http://www.plantuml.com/plantuml/
    encoded_diagram = "SyfFKj2rKt3CoKnELR1Io4ZDoSa70000"
    plantuml_server = HTMLRenderer.PLANTUML_SERVER
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlantUML Direct Test</title>
    
    <script>
        console.log("=== PLANTUML DEBUG TEST ===");
        
        // Log when DOM content is loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM content loaded");
            const img = document.getElementById('plantuml-image');
            console.log("PlantUML image element:", img);
            
            // Log when the image is loaded
            img.onload = function() {
                console.log("PlantUML image loaded successfully");
                console.log("Image dimensions:", img.naturalWidth, "x", img.naturalHeight);
            };
            
            // Log if the image fails to load
            img.onerror = function() {
                console.error("PlantUML image failed to load");
            };
        });
    </script>
</head>
<body>
    <h1>PlantUML Direct Test</h1>
    
    <h2>Direct Image from PlantUML Server</h2>
    <img id="plantuml-image" src="PLANTUML_SERVER_URL/png/ENCODED_DIAGRAM" alt="PlantUML Diagram" />
    
    <h2>Information</h2>
    <ul>
        <li>This test uses a direct encoded PlantUML diagram</li>
        <li>The image is loaded directly from the PlantUML server</li>
        <li>Check the browser console (F12) for debugging information</li>
    </ul>
    
    <h2>PlantUML Server Details</h2>
    <ul>
        <li>Server URL: PLANTUML_SERVER_URL</li>
        <li>Encoded diagram: ENCODED_DIAGRAM</li>
        <li>Full image URL: <a href="PLANTUML_SERVER_URL/png/ENCODED_DIAGRAM">PLANTUML_SERVER_URL/png/ENCODED_DIAGRAM</a></li>
    </ul>
</body>
</html>
"""
    
    # Replace placeholders
    html_content = html_content.replace("PLANTUML_SERVER_URL", plantuml_server)
    html_content = html_content.replace("ENCODED_DIAGRAM", encoded_diagram)
    
    with open(test_file, 'w') as f:
        f.write(html_content)
        
    print(f"Created test file: {test_file}")
    
    # Try to open with browser
    try:
        abs_path = open_browser(test_file)
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{os.path.abspath(test_file)}")


def test_plantuml_html_generation():
    """Test PlantUML HTML generation with our library."""
    print("\nTesting PlantUML HTML generation...")
    
    script_dir = Path(__file__).parent
    plantuml_file = script_dir / "plantuml_test_diagram.puml"
    
    if not plantuml_file.exists():
        print(f"Error: PlantUML test file {plantuml_file} does not exist.")
        return
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file = output_dir / "plantuml_generated_test.html"
    
    # Generate HTML using the library
    print(f"Generating HTML from PlantUML file: {plantuml_file}")
    generated_file = create_diagram_from_file(plantuml_file, output_file, output_format="html")
    print(f"Generated file: {generated_file}")
    
    # Add debug script to the generated file
    debug_script = """
<script>
    console.log("=== PLANTUML DEBUG ===");
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log("DOM content loaded");
        
        // Check for PlantUML image
        const plantumlImage = document.querySelector('.plantuml-image');
        console.log("PlantUML image element:", plantumlImage);
        
        if (plantumlImage) {
            // Log when the image is loaded
            plantumlImage.onload = function() {
                console.log("PlantUML image loaded successfully");
                console.log("Image dimensions:", plantumlImage.naturalWidth, "x", plantumlImage.naturalHeight);
                console.log("Image URL:", plantumlImage.src);
            };
            
            // Log if the image fails to load
            plantumlImage.onerror = function() {
                console.error("PlantUML image failed to load");
                console.error("Image URL:", plantumlImage.src);
            };
        } else {
            console.error("PlantUML image element not found");
        }
        
        // Check for resources
        console.log("Static URL check:");
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        stylesheets.forEach(sheet => {
            console.log("Stylesheet:", sheet.href);
        });
        
        const scripts = document.querySelectorAll('script[src]');
        scripts.forEach(script => {
            console.log("Script:", script.src);
        });
    });
</script>
"""
    
    try:
        # Read the generated file
        with open(output_file, 'r') as f:
            content = f.read()
        
        # Insert debug script before </head>
        modified_content = content.replace('</head>', f'{debug_script}</head>')
        
        # Write back the modified file
        with open(output_file, 'w') as f:
            f.write(modified_content)
            
        print("Added debug scripts to the generated file")
    except Exception as e:
        print(f"Error modifying generated file: {e}")
    
    # Try to open with browser
    try:
        abs_path = open_browser(output_file)
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{os.path.abspath(output_file)}")


def main():
    """Run all PlantUML tests."""
    print("PlantUML Rendering Diagnostic Tests")
    print("==================================")
    
    test_plantuml_server_connection()
    create_test_html()
    test_plantuml_html_generation()
    
    print("\nAll PlantUML tests completed.")
    print("\nPlease check the browser console and network tab for results.")


if __name__ == "__main__":
    main() 