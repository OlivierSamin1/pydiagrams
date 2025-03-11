#!/usr/bin/env python3
"""
Script to fix HTML renderer issues and create direct HTML diagrams
"""
import os
import sys
import webbrowser
import zlib
import base64
from pathlib import Path

# Example diagrams to use for testing
EXAMPLE_MERMAID = """
classDiagram
    class Customer {
        -String name
        -String email
        +register()
        +login()
    }
    class Order {
        -int id
        -Date date
        +create()
        +cancel()
    }
    Customer "1" -- "*" Order: places
"""

EXAMPLE_PLANTUML = """# PlantUML support disabled"""

def create_mermaid_html(output_path, content=None):
    """Create a direct Mermaid HTML file"""
    if content is None:
        content = EXAMPLE_MERMAID
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Diagram</title>
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
        
        .buttons {{
            margin-top: 20px;
            text-align: center;
        }}
        
        button {{
            padding: 8px 16px;
            background-color: #4a86e8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 0 5px;
        }}
        
        button:hover {{
            background-color: #3a76d8;
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
            
            // Toggle dark mode
            const darkModeButton = document.getElementById('dark-mode');
            darkModeButton.addEventListener('click', function() {{
                document.body.classList.toggle('dark-mode');
                
                if (document.body.classList.contains('dark-mode')) {{
                    document.body.style.backgroundColor = '#1e1e1e';
                    document.body.style.color = '#e0e0e0';
                    mermaid.initialize({{
                        theme: 'dark'
                    }});
                }} else {{
                    document.body.style.backgroundColor = '#ffffff';
                    document.body.style.color = '#333333';
                    mermaid.initialize({{
                        theme: 'default'
                    }});
                }}
                
                // Re-render the diagram
                const container = document.querySelector(".mermaid");
                const source = container.textContent.trim();
                container.innerHTML = source;
                mermaid.init(undefined, '.mermaid');
            }});
        }});
    </script>
</head>
<body>
    <h1>Mermaid Diagram</h1>
    <div class="container">
        <div class="mermaid">
{content}
        </div>
        <div class="buttons">
            <button id="dark-mode">Toggle Dark Mode</button>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return output_path

def create_plantuml_html(output_path, content=None):
    """PlantUML support disabled"""
    print("PlantUML support is disabled")
    return None

def process_example_files():
    """Process all example files in the examples directory"""
    current_dir = Path.cwd()
    examples_dir = current_dir / "examples"
    output_dir = current_dir / "fixed_output"
    output_dir.mkdir(exist_ok=True)
    
    # Get all example files
    example_files = []
    for ext in [".mmd"]:
        example_files.extend(list(examples_dir.glob(f"*{ext}")))
    
    print(f"Found {len(example_files)} example files.")
    
    # Process each file
    successful_outputs = []
    for example_file in example_files:
        output_file = output_dir / f"{example_file.stem}.html"
        print(f"Processing {example_file}...")
        
        try:
            # Read the content of the example file
            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Determine diagram type and create appropriate HTML
            if example_file.suffix.lower() == ".mmd":
                output_path = create_mermaid_html(output_file, content)
            else:  # .puml
                output_path = create_plantuml_html(output_file, content)
            
            successful_outputs.append(output_path)
            print(f"Created {output_file}")
        except Exception as e:
            print(f"Error processing {example_file}: {e}")
    
    # Open all successful outputs in browser
    print(f"\nGenerated {len(successful_outputs)} HTML files.")
    if successful_outputs:
        print("Opening HTML files in browser...")
        for output_path in successful_outputs:
            file_url = f"file://{output_path.absolute()}"
            print(f"Opening {file_url}")
            webbrowser.open_new_tab(file_url)

def main():
    # Create direct examples first for testing
    output_dir = Path.cwd() / "direct_examples"
    output_dir.mkdir(exist_ok=True)
    
    mermaid_path = create_mermaid_html(output_dir / "mermaid_example.html")
    # PlantUML support disabled
    
    print(f"Created direct example files in {output_dir}")
    
    # Open example files in browser
    webbrowser.open(f"file://{mermaid_path}")
    # PlantUML support disabled
    
    # Process all example files
    process_example_files()

if __name__ == "__main__":
    main() 