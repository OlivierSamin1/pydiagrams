#!/usr/bin/env python3
"""
Script to refocus the PyDiagrams library to support only Mermaid diagrams,
disabling PlantUML support.
"""
import sys
from pathlib import Path

def update_generate_examples_script():
    """Update generate_examples.py to only create Mermaid examples"""
    file_path = Path.cwd() / "generate_examples.py"
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found, skipping")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove PlantUML examples
    updated_content = content
    
    # Find the examples dictionary and modify it
    import re
    
    # Pattern to match the examples dictionary definition
    pattern = r'examples\s*=\s*\{[^}]*\}'
    
    # Check if we have dictionary content
    if not re.search(pattern, content, re.DOTALL):
        print(f"Could not find examples dictionary in {file_path}")
        return False
    
    # Extract the dictionary content
    examples_dict_match = re.search(pattern, content, re.DOTALL)
    examples_dict_str = examples_dict_match.group(0)
    
    # Remove all PlantUML examples and convert any diagram definitions to Mermaid
    # We'll remove any dictionary entries where the content includes @startuml
    lines = examples_dict_str.split('\n')
    filtered_lines = []
    skip_until_end_of_block = False
    
    for line in lines:
        if '@startuml' in line:
            skip_until_end_of_block = True
            continue
        
        if skip_until_end_of_block:
            if '"""' in line or "'''" in line:  # End of multiline string
                skip_until_end_of_block = False
            continue
            
        filtered_lines.append(line)
    
    # Reconstruct the dictionary
    updated_dict_str = '\n'.join(filtered_lines)
    
    # Replace the original dictionary with our updated one
    updated_content = content.replace(examples_dict_match.group(0), updated_dict_str)
    
    # Update the file extension logic to only look for .mmd files
    updated_content = re.sub(
        r'file_extension\s*=\s*".puml"\s*if\s*"@startuml"\s*in\s*content\s*else\s*".mmd"',
        'file_extension = ".mmd"',
        updated_content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path} to only generate Mermaid examples")
    return True

def update_generate_outputs_script():
    """Update generate_outputs.py to only process Mermaid files"""
    file_path = Path.cwd() / "generate_outputs.py"
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found, skipping")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the file extension pattern to only look for .mmd files
    import re
    updated_content = re.sub(
        r'for ext in \[".mmd", ".puml"\]:',
        'for ext in [".mmd"]:',
        content
    )
    
    # Remove PlantUML specific code in create_direct_html
    pattern = r'if diagram_type == "mermaid":(.*?)else:  # PlantUML(.*?)with open\(output_file, \'w\', encoding=\'utf-8\'\) as f:'
    match = re.search(pattern, updated_content, re.DOTALL)
    
    if match:
        mermaid_block = match.group(1)
        # Keep only the Mermaid part and remove the else block
        replacement = f'# Only support Mermaid diagrams\n{mermaid_block}\n    with open(output_file, \'w\', encoding=\'utf-8\') as f:'
        updated_content = re.sub(pattern, replacement, updated_content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path} to only process Mermaid files")
    return True

def update_fix_html_renderer_script():
    """Update fix_html_renderer.py to only support Mermaid diagrams"""
    file_path = Path.cwd() / "fix_html_renderer.py"
    
    if not file_path.exists():
        print(f"Warning: {file_path} not found, skipping")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove PlantUML example
    import re
    updated_content = re.sub(
        r'EXAMPLE_PLANTUML = """.*?"""',
        'EXAMPLE_PLANTUML = """# PlantUML support disabled"""',
        content,
        flags=re.DOTALL
    )
    
    # Remove create_plantuml_html function
    pattern = r'def create_plantuml_html\(.*?\):(.*?)return output_path'
    match = re.search(pattern, updated_content, re.DOTALL)
    
    if match:
        replacement = 'def create_plantuml_html(output_path, content=None):\n    """PlantUML support disabled"""\n    print("PlantUML support is disabled")\n    return None'
        updated_content = re.sub(pattern, replacement, updated_content, flags=re.DOTALL)
    
    # Update process_example_files to only process .mmd files
    updated_content = re.sub(
        r'for ext in \[".mmd", ".puml"\]:',
        'for ext in [".mmd"]:',
        updated_content
    )
    
    # Update the main function to not create PlantUML examples
    pattern = r'plantuml_path = create_plantuml_html\(.*?\)'
    updated_content = re.sub(pattern, '# PlantUML support disabled', updated_content)
    
    # Update the main function to not open PlantUML examples
    pattern = r'webbrowser.open\(f"file://\{plantuml_path\}"\)'
    updated_content = re.sub(pattern, '# PlantUML support disabled', updated_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {file_path} to only support Mermaid diagrams")
    return True

def main():
    print("Refocusing PyDiagrams to support only Mermaid diagrams...")
    
    # Update each script
    update_generate_examples_script()
    update_generate_outputs_script()
    update_fix_html_renderer_script()
    
    print("\nDone! PyDiagrams now only supports Mermaid diagrams.")
    print("The following files have been modified:")
    print("- generate_examples.py")
    print("- generate_outputs.py")
    print("- fix_html_renderer.py")

if __name__ == "__main__":
    main() 