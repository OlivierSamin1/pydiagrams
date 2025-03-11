#!/usr/bin/env python3
"""
Script to generate HTML outputs for all example files and open them in the browser
"""
import os
import sys
import subprocess
import webbrowser
import inspect
import json
from time import sleep
from pathlib import Path

# Add the project root to Python path
current_dir = Path(__file__).resolve().parent
project_root = current_dir
sys.path.insert(0, str(project_root))

# Import generate_diagram_from_file function directly
try:
    from pydiagrams.parsers.diagram_utils import generate_diagram_from_file
    from pydiagrams import create_diagram_from_file
    FUNCTION_AVAILABLE = True
except ImportError:
    FUNCTION_AVAILABLE = False
    print("Warning: Could not import PyDiagrams functions. Will use CLI method instead.")

# File paths
examples_dir = project_root / "examples"
output_dir = project_root / "output"
output_dir.mkdir(exist_ok=True)

# Get all example files
example_files = []
for ext in [".mmd"]:
    example_files.extend(list(examples_dir.glob(f"*{ext}")))

print(f"Found {len(example_files)} example files.")

# Function to check if file exists and read its contents
def get_file_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# Function to directly create HTML file with embedded diagram
def create_direct_html(input_file, output_file):
    # Determine diagram type and read content
    input_path = Path(input_file)
    diagram_type = "mermaid" if input_path.suffix.lower() == ".mmd" else "plantuml"
    
    with open(input_path, 'r', encoding='utf-8') as f:
        diagram_content = f.read().strip()
    
    # Only support Mermaid diagrams

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{input_path.stem}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333333;
        }}
        
        .mermaid {{
            max-width: 100%;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                fontFamily: '"Courier New", Courier, monospace'
            }});
        }});
    </script>
</head>
<body>
    <h1>{input_path.stem}</h1>
    <div class="container">
        <div class="mermaid">
{diagram_content}
        </div>
    </div>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created direct HTML file: {output_file}")
    return output_file

# Function to convert a file using direct function call
def convert_using_function(input_file, output_file):
    try:
        # First check if the function exists and has the right parameters
        if not FUNCTION_AVAILABLE:
            return None
            
        output_path = create_diagram_from_file(
            str(input_file),
            str(output_file),
            output_format="html",
            inline_resources=True
        )
        
        # Verify the file was created and has content
        if not os.path.exists(output_path) or os.path.getsize(output_path) < 100:
            print(f"Function created a file but it may be incomplete, falling back to direct method")
            return create_direct_html(input_file, output_file)
            
        print(f"Generated {output_path} using function call")
        return output_path
    except Exception as e:
        print(f"Error generating diagram using function: {e}")
        
        # Fall back to direct HTML creation
        return create_direct_html(input_file, output_file)

# Function to convert a file using CLI
def convert_using_cli(input_file, output_file):
    try:
        # Construct the command
        command = [
            "python", "-m", "pydiagrams.cli",
            str(input_file),
            "-o", str(output_file),
            "-f", "html",
            "--inline-resources"
        ]
        
        # Run the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Verify the file was created and has content
            if not os.path.exists(output_file) or os.path.getsize(output_file) < 100:
                print(f"CLI created a file but it may be incomplete, falling back to direct method")
                return create_direct_html(input_file, output_file)
                
            print(f"Generated {output_file} using CLI")
            return output_file
        else:
            print(f"Error running CLI: {result.stderr}")
            
            # Fall back to direct HTML creation
            return create_direct_html(input_file, output_file)
    except Exception as e:
        print(f"Error running CLI command: {e}")
        
        # Fall back to direct HTML creation
        return create_direct_html(input_file, output_file)

# Process each example file
successful_outputs = []

for example_file in example_files:
    # Create output path
    output_name = f"{example_file.stem}.html"
    output_file = output_dir / output_name
    
    print(f"\nProcessing {example_file}...")
    
    # Try using function first if available
    if FUNCTION_AVAILABLE:
        output_path = convert_using_function(example_file, output_file)
        if output_path:
            successful_outputs.append(output_path)
    else:
        # Fall back to CLI
        output_path = convert_using_cli(example_file, output_file)
        if output_path:
            successful_outputs.append(str(output_path))

# Open all successful outputs in browser
print(f"\nGenerated {len(successful_outputs)} HTML files.")
if successful_outputs:
    print("Opening HTML files in browser...")
    for output_path in successful_outputs:
        # Convert to absolute path with file:// prefix for browser
        file_url = f"file://{os.path.abspath(output_path)}"
        print(f"Opening {file_url}")
        webbrowser.open_new_tab(file_url)
        # Short delay to prevent overwhelming the browser
        sleep(0.5) 