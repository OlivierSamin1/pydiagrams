#!/usr/bin/env python3
"""
Script to restructure the PyDiagrams project for better organization.
"""
import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create a better organized directory structure"""
    current_dir = Path.cwd()
    
    # Create new directory structure
    scripts_dir = current_dir / "scripts"
    examples_dir = current_dir / "examples"
    outputs_dir = current_dir / "outputs"
    tests_dir = current_dir / "tests"
    docs_dir = current_dir / "docs"
    
    # Create directories if they don't exist
    for dir_path in [scripts_dir, examples_dir, outputs_dir, tests_dir, docs_dir]:
        dir_path.mkdir(exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Move existing scripts to scripts directory
    script_files = [
        "fix_diagram_generation.py",
        "fix_html_renderer.py",
        "generate_examples.py",
        "generate_outputs.py",
        "mermaid_only.py"
    ]
    
    for script_file in script_files:
        source_path = current_dir / script_file
        if source_path.exists():
            target_path = scripts_dir / script_file
            shutil.copy2(source_path, target_path)
            print(f"Moved {script_file} to scripts directory")
    
    # Create a README.md file for the scripts directory
    with open(scripts_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write("""# PyDiagrams Scripts

This directory contains utility scripts for the PyDiagrams project.

## Scripts

- `fix_diagram_generation.py`: Diagnoses and fixes diagram generation issues
- `fix_html_renderer.py`: Creates direct HTML diagrams without using the PyDiagrams renderer
- `generate_examples.py`: Generates example Mermaid files for all diagram types
- `generate_outputs.py`: Generates HTML outputs from example files
- `mermaid_only.py`: Modifies scripts to only support Mermaid diagrams (disables PlantUML)
""")
    
    # Create subdirectories in examples
    for subdir in ["architectural", "entity", "code", "uml"]:
        (examples_dir / subdir).mkdir(exist_ok=True)
        print(f"Created directory: {examples_dir / subdir}")
    
    # Create subdirectories in outputs
    for subdir in ["architectural", "entity", "code", "uml"]:
        (outputs_dir / subdir).mkdir(exist_ok=True)
        print(f"Created directory: {outputs_dir / subdir}")
    
    # Create a README.md file for the project
    with open(current_dir / "README.md", 'a', encoding='utf-8') as f:
        f.write("""

## Project Structure

- `scripts/`: Utility scripts for diagram generation and testing
- `examples/`: Example Mermaid diagram files
  - `architectural/`: Architectural diagram examples
  - `entity/`: Entity diagram examples
  - `code/`: Code diagram examples
  - `uml/`: UML diagram examples
- `outputs/`: Generated HTML diagram outputs
- `tests/`: Test scripts and files
- `docs/`: Documentation files
- `pydiagrams/`: Main library code
""")
    
    print("\nProject structure has been reorganized.")

def create_automation_script():
    """Create a main.py script in the root to automate common tasks"""
    current_dir = Path.cwd()
    main_script_path = current_dir / "main.py"
    
    content = """#!/usr/bin/env python3
\"\"\"
Main script for PyDiagrams project.
This script provides a command-line interface to common tasks.
\"\"\"
import argparse
import os
import subprocess
import sys
from pathlib import Path

def generate_examples():
    \"\"\"Generate example Mermaid files for all diagram types\"\"\"
    print("Generating example files...")
    
    script_path = Path(__file__).parent / "scripts" / "generate_examples.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], check=True)
    else:
        print(f"Error: Script not found at {script_path}")
        return False
    
    return True

def generate_outputs():
    \"\"\"Generate HTML outputs from example files\"\"\"
    print("Generating HTML outputs...")
    
    script_path = Path(__file__).parent / "scripts" / "generate_outputs.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], check=True)
    else:
        print(f"Error: Script not found at {script_path}")
        return False
    
    return True

def fix_renderers():
    \"\"\"Fix diagram rendering issues\"\"\"
    print("Fixing diagram renderers...")
    
    script_path = Path(__file__).parent / "scripts" / "fix_html_renderer.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], check=True)
    else:
        print(f"Error: Script not found at {script_path}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="PyDiagrams Project Automation")
    
    # Add commands
    parser.add_argument(
        'command', 
        choices=['examples', 'outputs', 'fix', 'all'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'examples':
        generate_examples()
    elif args.command == 'outputs':
        generate_outputs()
    elif args.command == 'fix':
        fix_renderers()
    elif args.command == 'all':
        if generate_examples():
            if generate_outputs():
                fix_renderers()

if __name__ == "__main__":
    main()
"""
    
    with open(main_script_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Make the script executable
    os.chmod(main_script_path, 0o755)
    
    print(f"Created main automation script: {main_script_path}")

def main():
    print("Restructuring PyDiagrams project...")
    
    # Create new directory structure
    create_directory_structure()
    
    # Create automation script
    create_automation_script()
    
    print("\nDone! Project structure has been reorganized.")
    print("You can now use the main.py script to automate common tasks:")
    print("  python main.py examples  # Generate example files")
    print("  python main.py outputs   # Generate HTML outputs")
    print("  python main.py fix       # Fix diagram renderers")
    print("  python main.py all       # Run all commands in sequence")

if __name__ == "__main__":
    main() 