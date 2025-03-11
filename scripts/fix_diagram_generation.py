#!/usr/bin/env python3
"""
Script to diagnose and fix diagram generation issues.
This creates a simple test HTML file with embedded diagram code.
"""
import os
import sys
from pathlib import Path

# Sample diagrams for testing
MERMAID_SAMPLE = """
classDiagram
    class Customer {
        -String name
        -String email
        -String address
        +register()
        +login()
        +updateProfile()
    }
    
    class Order {
        -int orderNumber
        -Date orderDate
        -String status
        +placeOrder()
        +cancelOrder()
        +ship()
    }
    
    Customer "1" -- "0..*" Order : places
"""

PLANTUML_SAMPLE = """
@startuml
actor User
participant "Web UI" as UI
participant "API Server" as API
participant "Database" as DB

User -> UI: Register
UI -> API: POST /register
API -> DB: Insert User
DB --> API: User Created
API --> UI: Registration Success
UI --> User: Show Success Message
@enduml
"""

# Create a simple HTML test file with Mermaid
def create_mermaid_test(output_dir):
    output_path = output_dir / "test_mermaid.html"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Test</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
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
    <h1>Mermaid Test Diagram</h1>
    <div class="mermaid">
{MERMAID_SAMPLE}
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created Mermaid test file at: {output_path}")
    return output_path

# Create a simple HTML test file with PlantUML
def create_plantuml_test(output_dir):
    output_path = output_dir / "test_plantuml.html"
    
    # Encode PlantUML for server usage
    import zlib
    import base64
    
    zlibbed = zlib.compress(PLANTUML_SAMPLE.encode('utf-8'))
    compressed = base64.b64encode(zlibbed).decode('ascii')
    compressed = compressed.replace('+', '-').replace('/', '_')
    encoded_content = f"~1{compressed}"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlantUML Test</title>
</head>
<body>
    <h1>PlantUML Test Diagram</h1>
    <div>
        <img src="http://www.plantuml.com/plantuml/svg/{encoded_content}" alt="PlantUML Diagram">
    </div>
    <h2>Original PlantUML Code:</h2>
    <pre>{PLANTUML_SAMPLE}</pre>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created PlantUML test file at: {output_path}")
    return output_path

# Check and fix the templates
def check_templates():
    print("Checking templates to identify issues...")
    
    # Find the template directory
    current_dir = Path.cwd()
    template_dir = current_dir / "pydiagrams" / "renderers" / "templates"
    
    if not template_dir.exists():
        print(f"Template directory not found at {template_dir}")
        return False
    
    # Check if the mermaid.html template needs fixes
    mermaid_file = template_dir / "mermaid.html"
    if mermaid_file.exists():
        with open(mermaid_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the mermaid div is properly configured
        if "{{ diagram_content | safe }}" in content and "<div class=\"mermaid\">" not in content:
            print("Issue found in mermaid.html: missing mermaid div wrapper")
            
            # Fix by ensuring the diagram content is wrapped in a mermaid div
            fixed_content = content.replace(
                "{% block diagram %}{{ diagram_content | safe }}{% endblock %}", 
                "{% block diagram %}<div class=\"mermaid\">{{ diagram_content | safe }}</div>{% endblock %}"
            )
            
            with open(mermaid_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print("Fixed mermaid.html template")
    
    return True

def main():
    print("Running diagram generation diagnostic and fix script")
    
    # Create output directory
    output_dir = Path.cwd() / "test_output"
    output_dir.mkdir(exist_ok=True)
    
    # Create test files
    mermaid_path = create_mermaid_test(output_dir)
    plantuml_path = create_plantuml_test(output_dir)
    
    # Check and fix templates
    templates_ok = check_templates()
    
    # Open the test files in browser
    import webbrowser
    webbrowser.open(f"file://{mermaid_path.absolute()}")
    webbrowser.open(f"file://{plantuml_path.absolute()}")
    
    print("\nDiagnostic script completed.")
    print("The test files have been opened in your browser.")
    print("If the diagrams are visible in these test files but not in your generated files,")
    print("there may be an issue with how PyDiagrams is generating the content.")
    
    if templates_ok:
        print("\nYou may need to regenerate your output files after the template fixes.")
        print("Run 'python generate_outputs.py' again to regenerate the diagrams.")
    
if __name__ == "__main__":
    main() 