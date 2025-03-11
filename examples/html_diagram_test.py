#!/usr/bin/env python3
"""
Diagnostic test script for debugging HTML diagram rendering issues.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydiagrams import create_diagram_from_file


def create_debug_html(mermaid_content, output_path):
    """Create a direct HTML file with debug output."""
    debug_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagram Debug Test</title>
    
    <script>
        console.log("=== DIAGRAM DEBUG TEST ===");
        console.log("Document loaded at:", new Date().toISOString());
        
        // Log when DOM content is loaded
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM content loaded");
            console.log("Looking for .mermaid element:", document.querySelector('.mermaid'));
            console.log("Looking for #diagram element:", document.getElementById('diagram'));
            
            // Check which scripts are loaded
            const scripts = document.querySelectorAll('script');
            console.log("Scripts loaded:", scripts.length);
            scripts.forEach((script, i) => {
                console.log(`Script ${i+1}:`, script.src || 'inline script');
            });
            
            // Check which stylesheets are loaded
            const styles = document.querySelectorAll('link[rel="stylesheet"]');
            console.log("Stylesheets loaded:", styles.length);
            styles.forEach((style, i) => {
                console.log(`Stylesheet ${i+1}:`, style.href);
            });
        });
    </script>
    
    <!-- Load Mermaid directly from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    
    <script>
        window.addEventListener('DOMContentLoaded', function() {
            console.log("Initializing Mermaid...");
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default'
            });
            console.log("Mermaid initialized");
        });
    </script>
</head>
<body>
    <h1>Diagram Debug Test</h1>
    
    <h2>Direct Mermaid Rendering (CDN)</h2>
    <div class="mermaid">""" + mermaid_content + """
    </div>
    
    <h2>Information</h2>
    <ul>
        <li>Check the browser console (F12 or right-click > Inspect > Console) for debug information</li>
        <li>Look for any error messages related to script loading or diagram rendering</li>
        <li>Make sure you opened this file with the <code>--allow-file-access-from-files</code> flag</li>
    </ul>
</body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(debug_html)


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


def test_with_simple_diagram():
    """Test with a simple hardcoded Mermaid diagram."""
    print("=== Test 1: Simple Hardcoded Diagram ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    test_file = output_dir / "simple_diagram_test.html"
    
    # Create a simple Mermaid diagram
    mermaid_content = """graph TD
    A[Client] --> B[Server]
    B --> C[Database]"""
    
    # Create a debug HTML file
    create_debug_html(mermaid_content, test_file)
    
    print(f"Created test file: {test_file}")
    
    # Try to open with browser
    try:
        abs_path = open_browser(test_file)
        
        print("Instructions:")
        print("1. Check the browser console (F12)")
        print("2. Look for errors or warnings")
        print("3. Check if the diagram is rendered")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{os.path.abspath(test_file)}")


def test_generated_html():
    """Test with a diagram generated by the library."""
    print("\n=== Test 2: Generated HTML Diagram ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create a test Mermaid file
    script_dir = Path(__file__).parent
    mermaid_file = script_dir / "test_diagram.mmd"
    
    # Create the test diagram file if it doesn't exist
    if not mermaid_file.exists():
        with open(mermaid_file, 'w') as f:
            f.write("""graph TD
    A[Client] --> B[Server]
    B --> C[Database]
    C --> D[Storage]
    A --> D
""")
    
    # Generate HTML using the library
    output_file = output_dir / "generated_diagram_test.html"
    generated_file = create_diagram_from_file(mermaid_file, output_file, output_format="html")
    
    print(f"Generated HTML file: {generated_file}")
    
    # Add debug script to the generated file
    debug_script = """
<script>
    console.log("=== PYDIAGRAMS DEBUG ===");
    console.log("Document loaded at:", new Date().toISOString());
    
    // Log when DOM content is loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log("DOM content loaded");
        console.log("Looking for .mermaid element:", document.querySelector('.mermaid'));
        console.log("Looking for #diagram element:", document.getElementById('diagram'));
        
        // Check which scripts are loaded
        const scripts = document.querySelectorAll('script');
        console.log("Scripts loaded:", scripts.length);
        scripts.forEach((script, i) => {
            console.log(`Script ${i+1}:`, script.src || 'inline script');
        });
        
        // Check which stylesheets are loaded
        const styles = document.querySelectorAll('link[rel="stylesheet"]');
        console.log("Stylesheets loaded:", styles.length);
        styles.forEach((style, i) => {
            console.log(`Stylesheet ${i+1}:`, style.href);
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
    except Exception as e:
        print(f"Error modifying generated file: {e}")
    
    # Try to open with browser
    try:
        abs_path = open_browser(output_file)
        
        print("Instructions:")
        print("1. Check the browser console (F12)")
        print("2. Look for errors or warnings")
        print("3. Check if the diagram is rendered")
        print("4. Note any missing resources")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{os.path.abspath(output_file)}")


def test_network_requests():
    """Test to inspect network requests to static resources."""
    print("\n=== Test 3: Network Request Inspection ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Copy static files to a relative path for debugging
    static_src_dir = Path(__file__).parent.parent / "pydiagrams" / "renderers" / "static"
    static_dst_dir = output_dir / "static"
    
    if static_src_dir.exists():
        # Copy the static directory
        shutil.copytree(static_src_dir, static_dst_dir, dirs_exist_ok=True)
        print(f"Copied static files to: {static_dst_dir}")
    
    # Create a test HTML file that loads resources from relative path
    test_file = output_dir / "network_test.html"
    
    network_test_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Request Test</title>
    
    <!-- Load our resources from relative path -->
    <link rel="stylesheet" href="static/css/themes.css">
    <script src="static/js/themes.js"></script>
    
    <!-- Load Mermaid from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    
    <script>
        console.log("=== NETWORK REQUEST TEST ===");
        
        // Log all network requests
        const originalFetch = window.fetch;
        window.fetch = function() {
            console.log("Fetch request:", arguments[0]);
            return originalFetch.apply(this, arguments);
        }
        
        // Initialize Mermaid
        document.addEventListener('DOMContentLoaded', function() {
            console.log("Initializing Mermaid...");
            mermaid.initialize({
                startOnLoad: true,
                theme: 'default'
            });
            
            // Check if resources are loaded
            setTimeout(function() {
                const themesLoaded = document.querySelector('link[href="static/css/themes.css"]');
                console.log("themes.css loaded:", themesLoaded !== null);
                
                const themeJsLoaded = document.querySelector('script[src="static/js/themes.js"]');
                console.log("themes.js loaded:", themeJsLoaded !== null);
                
                const mermaidLoaded = document.querySelector('script[src*="mermaid"]');
                console.log("mermaid.js loaded:", mermaidLoaded !== null);
                
                // Check computed styles to see if CSS is applied
                const body = document.body;
                const styles = window.getComputedStyle(body);
                console.log("Body background color:", styles.backgroundColor);
                console.log("Body font family:", styles.fontFamily);
            }, 1000);
        });
    </script>
</head>
<body>
    <h1>Network Request Test</h1>
    
    <h2>Mermaid Diagram</h2>
    <div class="mermaid">
        graph TD
        A[Client] --> B[Server]
        B --> C[Database]
    </div>
    
    <h2>Instructions</h2>
    <ul>
        <li>Open the browser Developer Tools (F12)</li>
        <li>Go to the Network tab</li>
        <li>Reload the page</li>
        <li>Check which resources are loaded successfully and which are failing</li>
    </ul>
</body>
</html>
"""
    
    with open(test_file, 'w') as f:
        f.write(network_test_html)
    
    print(f"Created network test file: {test_file}")
    
    # Try to open with browser
    try:
        abs_path = open_browser(test_file)
        
        print("Instructions:")
        print("1. Open the Network tab in Developer Tools")
        print("2. Reload the page")
        print("3. Check which resources are loaded successfully")
        print("4. Look for any 404 errors or blocked requests")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{os.path.abspath(test_file)}")


def test_with_alternate_browser():
    """Test with a different browser (Firefox)."""
    print("\n=== Test 4: Alternate Browser Test ===")
    
    output_dir = Path(__file__).parent.parent / "output" / "diagram_tests"
    output_file = output_dir / "generated_diagram_test.html"
    
    if not output_file.exists():
        print(f"Test file {output_file} does not exist. Run test_generated_html() first.")
        return
    
    print(f"Using existing test file: {output_file}")
    
    # Try to open with Firefox
    try:
        abs_path = os.path.abspath(output_file)
        print(f"Opening {abs_path} in Firefox...")
        
        # Try with firefox
        try:
            subprocess.run(["firefox", f"file://{abs_path}"])
        except FileNotFoundError:
            # If firefox is not available, try with the generic 'x-www-browser'
            try:
                subprocess.run(["x-www-browser", f"file://{abs_path}"])
            except FileNotFoundError:
                print("Firefox not found. You can manually open the file.")
                
        print("Instructions:")
        print("1. Check if the diagram is displayed in Firefox")
        print("2. Compare with the results in other browsers")
    except Exception as e:
        print(f"Error opening browser: {e}")
        print(f"You can manually open the file:")
        print(f"  file://{abs_path}")


def main():
    """Run all tests."""
    print("PyDiagrams HTML Rendering Diagnostic Tests")
    print("==========================================")
    
    # Run all tests
    test_with_simple_diagram()
    test_generated_html()
    test_network_requests()
    test_with_alternate_browser()
    
    print("\nAll tests completed. Please check the browser console for results.")
    print("\nExpected resources to be loaded:")
    print("1. CSS files:")
    print("   - [output_filename]_files/css/themes.css")
    print("2. JavaScript files:")
    print("   - [output_filename]_files/js/themes.js")
    print("   - For Mermaid: https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs")
    print("   - For exports: CDN links to jspdf and html2canvas")


if __name__ == "__main__":
    main() 