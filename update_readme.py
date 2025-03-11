#!/usr/bin/env python3
"""
Script to update the README.md file with information about the fixed PlantUML rendering
"""
import os
from pathlib import Path

def update_readme():
    """
    Update the README.md file with information about the PlantUML rendering fix
    """
    readme_path = Path.cwd() / "README.md"
    
    if not readme_path.exists():
        print(f"README.md not found at {readme_path}")
        return
    
    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Section to add
    plantuml_section = """
## Viewing PlantUML Diagrams Locally

To view PlantUML diagrams locally without CORS or server issues, use the fixed renderer:

```bash
# Install the required library
pip install requests

# Run the PlantUML fixer script
python fix_plantuml_rendering.py
```

This will:
1. Pre-download SVG renderings of your PlantUML diagrams
2. Create standalone HTML files with the diagrams embedded
3. Provide fallback rendering options if the primary method fails
4. Open the diagrams in your browser

The fixed HTML files will be in the `plantuml_fixed` directory and include:
- Embedded SVG content (no network requests needed)
- Dark mode support
- Source code display
- Multiple fallback rendering options

For more details, see the `plantuml_fixed/README.md` file.
"""
    
    # Check if the command line section already exists
    if "## Viewing PlantUML Diagrams Locally" in content:
        print("PlantUML section already exists in README.md")
        return
    
    # Find a good insertion point - after the Command Line section
    if "## Command Line" in content:
        parts = content.split("## Command Line")
        command_line_section = parts[1].split("##")[0] if len(parts[1].split("##")) > 1 else parts[1]
        new_content = "## Command Line" + command_line_section + plantuml_section + "\n##" + "##".join(parts[1].split("##")[1:])
        updated_content = parts[0] + new_content
    else:
        # If there's no Command Line section, add it near the end
        updated_content = content + "\n" + plantuml_section
    
    # Write the updated content back to the README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Updated README.md with PlantUML rendering information")

if __name__ == "__main__":
    update_readme() 