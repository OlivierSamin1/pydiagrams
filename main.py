#!/usr/bin/env python3
"""
Main script for PyDiagrams project.
This script provides a command-line interface to common tasks.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

def generate_examples():
    """Generate example Mermaid files for all diagram types"""
    print("Generating example files...")
    
    script_path = Path(__file__).parent / "scripts" / "generate_examples.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], check=True)
    else:
        print(f"Error: Script not found at {script_path}")
        return False
    
    return True

def generate_outputs():
    """Generate HTML outputs from example files"""
    print("Generating HTML outputs...")
    
    script_path = Path(__file__).parent / "scripts" / "generate_outputs.py"
    if script_path.exists():
        subprocess.run([sys.executable, str(script_path)], check=True)
    else:
        print(f"Error: Script not found at {script_path}")
        return False
    
    return True

def fix_renderers():
    """Fix diagram rendering issues"""
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
