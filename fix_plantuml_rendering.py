#!/usr/bin/env python3
"""
Script to fix PlantUML rendering issues in the generated HTML files
"""
import os
import sys
import webbrowser
import zlib
import base64
import requests
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# PlantUML server URLs to try (in order)
PLANTUML_SERVERS = [
    "http://www.plantuml.com/plantuml",
    "https://www.plantuml.com/plantuml",
    "http://plantuml.com/plantuml",
    "https://plantuml.com/plantuml"
]

def encode_plantuml(text):
    """Encode PlantUML text for use with the PlantUML server"""
    # Add the ~1 prefix to indicate DEFLATE encoding
    # Convert to UTF-8 and compress with zlib
    zlibbed = zlib.compress(text.encode('utf-8'))
    
    # Convert to base64 and replace unsafe characters
    compressed = base64.b64encode(zlibbed).decode('ascii')
    compressed = compressed.replace('+', '-').replace('/', '_')
    
    # Add ~1 prefix to indicate DEFLATE encoding
    return f"~1{compressed}"

def download_plantuml_svg(content, output_path=None):
    """
    Download PlantUML diagram as SVG using multiple server options and fallbacks
    Returns the SVG content as string or None if failed
    """
    encoded = encode_plantuml(content)
    
    for server in PLANTUML_SERVERS:
        try:
            url = f"{server}/svg/{encoded}"
            print(f"Trying to download from: {url}")
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200 and response.text.startswith("<svg"):
                print(f"Successfully downloaded SVG from {server}")
                
                # Save to file if output path is provided
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"Saved SVG to {output_path}")
                
                return response.text
            else:
                print(f"Failed to get valid SVG from {server} (status: {response.status_code})")
        except Exception as e:
            print(f"Error accessing {server}: {e}")
    
    print("Failed to download PlantUML diagram from any server")
    return None

def create_data_uri_svg(svg_content):
    """Convert SVG content to a data URI for embedding in HTML"""
    if not svg_content:
        return None
    
    svg_bytes = svg_content.encode('utf-8')
    b64_svg = base64.b64encode(svg_bytes).decode('ascii')
    return f"data:image/svg+xml;base64,{b64_svg}"

def create_enhanced_plantuml_html(output_path, plantuml_content, svg_content=None):
    """
    Create an improved PlantUML HTML file with multiple fallback options
    
    Args:
        output_path: Path to save the HTML file
        plantuml_content: The raw PlantUML content
        svg_content: Pre-downloaded SVG content (optional)
    """
    # Encode for PlantUML server
    encoded = encode_plantuml(plantuml_content)
    
    # If we have SVG content, create a data URI for direct embedding
    data_uri = create_data_uri_svg(svg_content) if svg_content else None
    
    # Add different rendering options with fallbacks
    img_src = ""
    if data_uri:
        img_src = f'<img id="diagram-svg-embed" src="{data_uri}" alt="PlantUML Diagram (Embedded)">'
    
    # Always include server URLs as fallbacks
    server_imgs = ""
    for i, server in enumerate(PLANTUML_SERVERS):
        server_imgs += f'<img id="diagram-svg-{i}" src="{server}/svg/{encoded}" alt="PlantUML Diagram (Server {i+1})" ' + \
                     f'onerror="this.style.display=\'none\'" style="display:none;">\n    '
    
    # Create the HTML content with all fallback options
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlantUML Diagram</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333333;
        }}
        
        .dark-mode {{
            background-color: #1e1e1e;
            color: #e0e0e0;
        }}
        
        .dark-mode pre {{
            background-color: #2d2d2d;
            color: #e0e0e0;
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
            text-align: center;
        }}
        
        img {{
            max-width: 100%;
            margin: 0 auto;
            display: block;
        }}
        
        pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            text-align: left;
            overflow-x: auto;
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
        
        .error-message {{
            color: #d32f2f;
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #d32f2f;
            border-radius: 4px;
            display: none;
        }}
        
        #rendering-options {{
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .rendering-option {{
            padding: 8px 16px;
            background-color: #f0f0f0;
            border-radius: 4px;
            cursor: pointer;
        }}
        
        .rendering-option:hover {{
            background-color: #e0e0e0;
        }}
        
        .dark-mode .rendering-option {{
            background-color: #2d2d2d;
        }}
        
        .dark-mode .rendering-option:hover {{
            background-color: #3d3d3d;
        }}
        
        .loading {{
            margin: 20px auto;
            text-align: center;
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Try to display the diagram with fallbacks
            tryLoadDiagram();
            
            // Toggle dark mode
            const darkModeBtn = document.getElementById('dark-mode-btn');
            if (darkModeBtn) {{
                darkModeBtn.addEventListener('click', function() {{
                    document.body.classList.toggle('dark-mode');
                }});
            }}
        }});
        
        function tryLoadDiagram() {{
            // First try the embedded SVG if it exists
            const embeddedImg = document.getElementById('diagram-svg-embed');
            let hasDisplayed = false;
            
            if (embeddedImg) {{
                embeddedImg.style.display = 'block';
                embeddedImg.onerror = function() {{
                    this.style.display = 'none';
                    tryServerImages();
                }};
                embeddedImg.onload = function() {{
                    hasDisplayed = true;
                }};
            }} else {{
                tryServerImages();
            }}
            
            // Function to try all server images in sequence
            function tryServerImages() {{
                for (let i = 0; i < {len(PLANTUML_SERVERS)}; i++) {{
                    const img = document.getElementById(`diagram-svg-${{i}}`);
                    if (img) {{
                        img.style.display = 'block';
                        img.onerror = function() {{
                            this.style.display = 'none';
                            // If this is the last image and none worked, show error
                            if (i === {len(PLANTUML_SERVERS) - 1} && !hasDisplayed) {{
                                showError();
                            }}
                        }};
                        img.onload = function() {{
                            hasDisplayed = true;
                        }};
                    }}
                }}
            }}
            
            // Show error message if no images could be loaded
            function showError() {{
                const errorDiv = document.getElementById('error-message');
                if (errorDiv) {{
                    errorDiv.style.display = 'block';
                }}
            }}
        }}
    </script>
</head>
<body>
    <h1>PlantUML Diagram</h1>
    <div class="container">
        <!-- Embedded SVG (if available) -->
        {img_src}
        
        <!-- Server fallbacks -->
        {server_imgs}
        
        <!-- Error message -->
        <div id="error-message" class="error-message">
            Could not load the PlantUML diagram. Please check your internet connection or try one of the options below.
            <div id="rendering-options">
                <div class="rendering-option" onclick="window.open('http://www.plantuml.com/plantuml/uml/{encoded}', '_blank')">
                    Open on PlantUML server
                </div>
                <div class="rendering-option" onclick="copyContent()">
                    Copy PlantUML code to clipboard
                </div>
            </div>
        </div>
        
        <div class="buttons">
            <button id="dark-mode-btn">Toggle Dark Mode</button>
        </div>
        
        <h2>PlantUML Source:</h2>
        <pre><code>{plantuml_content}</code></pre>
    </div>
    <script>
        function copyContent() {{
            const text = document.querySelector('pre code').textContent;
            navigator.clipboard.writeText(text)
                .then(() => alert('PlantUML code copied to clipboard'))
                .catch(err => alert('Failed to copy: ' + err));
        }}
    </script>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_path

def process_plantuml_files():
    """Find and fix all PlantUML files in the examples directory"""
    current_dir = Path.cwd()
    examples_dir = current_dir / "examples"
    output_dir = current_dir / "plantuml_fixed"
    output_dir.mkdir(exist_ok=True)
    
    # Find all PlantUML files
    plantuml_files = list(examples_dir.glob("*.puml"))
    
    print(f"Found {len(plantuml_files)} PlantUML files")
    
    # Function to process a single file
    def process_file(file_path):
        try:
            output_file = output_dir / f"{file_path.stem}.html"
            svg_file = output_dir / f"{file_path.stem}.svg"
            
            print(f"Processing {file_path}...")
            
            # Read PlantUML content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Try to download SVG in advance
            svg_content = download_plantuml_svg(content, svg_file)
            
            # Create enhanced HTML with fallbacks
            html_path = create_enhanced_plantuml_html(output_file, content, svg_content)
            
            print(f"Created {html_path}")
            return html_path
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    # Process all files in parallel
    with ThreadPoolExecutor(max_workers=min(len(plantuml_files), 5)) as executor:
        results = list(executor.map(process_file, plantuml_files))
    
    # Filter out None results
    successful_outputs = [r for r in results if r]
    
    # Open all successful outputs in browser
    print(f"\nGenerated {len(successful_outputs)} HTML files.")
    if successful_outputs:
        print("Opening HTML files in browser...")
        for output_path in successful_outputs:
            file_url = f"file://{output_path.absolute()}"
            print(f"Opening {file_url}")
            webbrowser.open_new_tab(file_url)

if __name__ == "__main__":
    process_plantuml_files() 