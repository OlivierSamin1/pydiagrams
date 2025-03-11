#!/usr/bin/env python3
"""
Script to add PlantUML to Mermaid conversion to PyDiagrams for better diagram rendering
"""
import os
import re
import sys
import shutil
from pathlib import Path

# Function to convert PlantUML to Mermaid (copied from convert_plantuml_to_mermaid.py)
def convert_plantuml_to_mermaid(content):
    """
    Convert PlantUML diagram to Mermaid format based on diagram type
    """
    content = content.lower()
    
    # Detect diagram type
    if "actor" in content or "participant" in content or "->" in content and not "class" in content:
        diagram_type = "sequence"
    elif "class" in content or "<|--" in content:
        diagram_type = "class"
    elif "state" in content:
        diagram_type = "state"
    elif "entity" in content or "}|--||" in content:
        diagram_type = "er"
    elif "component" in content or "package" in content or "[" in content and "]" in content:
        diagram_type = "component"
    else:
        diagram_type = "sequence"  # Default to sequence diagram
    
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    if diagram_type == "sequence":
        # Convert title
        title_match = re.search(r'title\s+(.*?)$', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            content = re.sub(r'title\s+.*?\n', '', content)
            mermaid_title = f"sequenceDiagram\n    title: {title}\n"
        else:
            mermaid_title = "sequenceDiagram\n"
        
        # Convert participants
        participant_pattern = r'participant\s+"([^"]+)"\s+as\s+(\w+)'
        actor_pattern = r'actor\s+"([^"]+)"\s+as\s+(\w+)'
        database_pattern = r'database\s+"([^"]+)"\s+as\s+(\w+)'
        
        def convert_participant_line(match):
            name = match.group(1)
            alias = match.group(2)
            return f"    participant {alias} as \"{name}\""
        
        content = re.sub(participant_pattern, convert_participant_line, content)
        content = re.sub(actor_pattern, lambda m: f"    actor {m.group(2)} as \"{m.group(1)}\"", content)
        content = re.sub(database_pattern, lambda m: f"    participant {m.group(2)} as \"{m.group(1)}\"", content)
        
        # Simple participants without quotes or aliases
        content = re.sub(r'participant\s+(\w+)\s*$', r'    participant \1', content, flags=re.MULTILINE)
        content = re.sub(r'actor\s+(\w+)\s*$', r'    actor \1', content, flags=re.MULTILINE)
        content = re.sub(r'database\s+(\w+)\s*$', r'    participant \1', content, flags=re.MULTILINE)
        
        # Convert arrows
        content = re.sub(r'(\w+)\s*->\s*(\w+)\s*:\s*(.*?)$', r'    \1->>\2: \3', content, flags=re.MULTILINE)
        content = re.sub(r'(\w+)\s*-->\s*(\w+)\s*:\s*(.*?)$', r'    \1-->>\2: \3', content, flags=re.MULTILINE)
        
        # Handle activation/deactivation
        content = re.sub(r'activate\s+(\w+)', r'    activate \1', content)
        content = re.sub(r'deactivate\s+(\w+)', r'    deactivate \1', content)
        
        # Handle notes
        content = re.sub(r'note\s+(?:left|right)\s+of\s+(\w+)\s*:\s*(.*?)$', 
                         r'    Note \1: \2', content, flags=re.MULTILINE)
        
        return mermaid_title + content.strip()
    
    elif diagram_type == "class":
        # Start with class diagram declaration
        mermaid_content = "classDiagram\n"
        
        # Convert class definitions
        class_pattern = r'class\s+(\w+)(?:\s*{([^}]*)})?'
        
        def convert_class(match):
            class_name = match.group(1)
            members = match.group(2) if match.group(2) else ""
            
            # Format members if present
            if members:
                formatted_members = []
                for line in members.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Convert attributes and methods
                    if ':' in line:  # It's already in Mermaid format
                        formatted_members.append(f"    {line}")
                    elif '(' in line:  # It's a method
                        method_name = line.split('(')[0].strip()
                        formatted_members.append(f"    +{method_name}()")
                    else:  # It's an attribute
                        formatted_members.append(f"    +{line} : string")
                
                if formatted_members:
                    return f"class {class_name} {{\n" + "\n".join(formatted_members) + "\n}"
                else:
                    return f"class {class_name}"
            else:
                return f"class {class_name}"
        
        content = re.sub(class_pattern, convert_class, content)
        
        # Convert relationships
        # Inheritance
        content = re.sub(r'(\w+)\s+<\|\-\-\s+(\w+)', r'    \2 --|> \1', content)
        
        # Composition
        content = re.sub(r'(\w+)\s+\*\-\-\s+(\w+)', r'    \1 *-- \2', content)
        
        # Aggregation
        content = re.sub(r'(\w+)\s+o\-\-\s+(\w+)', r'    \1 o-- \2', content)
        
        # Association with label
        content = re.sub(r'(\w+)\s+\-\-\s+(\w+)\s*:\s*(.*?)$', r'    \1 -- \2 : \3', content, flags=re.MULTILINE)
        
        # Simple association
        content = re.sub(r'(\w+)\s+\-\-\s+(\w+)', r'    \1 -- \2', content)
        
        return mermaid_content + content.strip()
    
    elif diagram_type == "component":
        # Start with flowchart declaration
        mermaid_content = "graph TD\n"
        
        # Convert components
        component_pattern = r'\[([^\]]+)\]'
        content = re.sub(component_pattern, r'    \1[\1]', content)
        
        # Convert interfaces
        interface_pattern = r'\(\)\s*"([^"]+)"'
        content = re.sub(interface_pattern, r'    \1((\1))', content)
        
        # Convert databases
        database_pattern = r'database\s*"([^"]+)"'
        content = re.sub(database_pattern, r'    \1[(\1)]', content)
        
        # Convert packages
        package_start_pattern = r'package\s*"([^"]+)"\s*{'
        package_end_pattern = r'}'
        
        def convert_package(match):
            package_name = match.group(1)
            return f"    subgraph \"{package_name}\""
        
        content = re.sub(package_start_pattern, convert_package, content)
        content = re.sub(package_end_pattern, r'    end', content)
        
        # Convert relationships
        content = re.sub(r'(\w+)\s*-+>\s*(\w+)', r'    \1 --> \2', content)
        
        # Convert labels
        content = re.sub(r'(\w+)\s*-+>\s*(\w+)\s*:\s*([^\n]+)', r'    \1 -->|\3| \2', content)
        
        return mermaid_content + content.strip()
    
    else:
        return f"graph TD\n    A[\"This diagram type ({diagram_type}) is not fully supported - Converted from PlantUML\"]"

# Check if the renderer template needs to be updated
def update_html_renderer_template():
    print("Looking for HTML renderer to update...")
    
    # Find the pydiagrams directory
    pydiagrams_dir = Path.cwd() / "pydiagrams"
    if not pydiagrams_dir.exists():
        print("Error: Could not find the pydiagrams directory in the current working directory.")
        return False
    
    # Find the plantuml.html template
    plantuml_template_path = pydiagrams_dir / "renderers" / "templates" / "plantuml.html"
    if not plantuml_template_path.exists():
        print("Error: Could not find the plantuml.html template.")
        return False
    
    # Backup the original template
    backup_path = plantuml_template_path.with_suffix(".html.bak")
    if not backup_path.exists():
        shutil.copy2(plantuml_template_path, backup_path)
        print(f"Backed up original template to {backup_path}")
    
    # Read the mermaid.html template
    mermaid_template_path = pydiagrams_dir / "renderers" / "templates" / "mermaid.html"
    if not mermaid_template_path.exists():
        print("Error: Could not find the mermaid.html template.")
        return False
    
    with open(mermaid_template_path, 'r', encoding='utf-8') as f:
        mermaid_template_content = f.read()
    
    # Create a new PlantUML template that uses Mermaid
    plantuml_mermaid_template = mermaid_template_content.replace(
        "{% block diagram %}\n<div class=\"mermaid\">\n{{ diagram_content | safe }}\n</div>\n{% endblock %}",
        "{% block diagram %}\n<div class=\"mermaid\">\n{{ mermaid_content | safe }}\n</div>\n{% endblock %}"
    )
    
    # Write the modified template back
    with open(plantuml_template_path, 'w', encoding='utf-8') as f:
        f.write(plantuml_mermaid_template)
    
    print(f"Updated {plantuml_template_path} to use Mermaid for rendering PlantUML diagrams")
    return True

# Check if the HTML renderer needs to be updated
def update_html_renderer():
    print("Looking for HTML renderer to update...")
    
    # Find the pydiagrams directory
    pydiagrams_dir = Path.cwd() / "pydiagrams"
    if not pydiagrams_dir.exists():
        print("Error: Could not find the pydiagrams directory in the current working directory.")
        return False
    
    # Find the HTML renderer
    html_renderer_path = pydiagrams_dir / "renderers" / "html_renderer.py"
    if not html_renderer_path.exists():
        print("Error: Could not find the HTML renderer at the expected path.")
        return False
    
    # Backup the original renderer
    backup_path = html_renderer_path.with_suffix(".py.bak")
    if not backup_path.exists():
        shutil.copy2(html_renderer_path, backup_path)
        print(f"Backed up original renderer to {backup_path}")
    
    # Read the HTML renderer
    with open(html_renderer_path, 'r', encoding='utf-8') as f:
        renderer_content = f.read()
    
    # Check if the renderer already includes the conversion function
    if "convert_plantuml_to_mermaid" in renderer_content:
        print("HTML renderer already includes the PlantUML to Mermaid conversion function.")
        return True
    
    # Add the conversion function
    conversion_code = """
    def _convert_plantuml_to_mermaid(self, content):
        \"\"\"
        Convert PlantUML diagram to Mermaid format
        
        Args:
            content: PlantUML diagram content
            
        Returns:
            Mermaid diagram content
        \"\"\"
        import re
        
        # Remove @startuml and @enduml tags
        content = re.sub(r'@startuml.*?\\n', '', content)
        content = re.sub(r'@enduml.*?\\n', '', content)
        
        # Detect diagram type
        content_lower = content.lower()
        if "actor" in content_lower or "participant" in content_lower or "->" in content_lower and not "class" in content_lower:
            # Sequence diagram
            # Convert title
            title_match = re.search(r'title\\s+(.*?)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
                content = re.sub(r'title\\s+.*?\\n', '', content)
                mermaid_title = f"sequenceDiagram\\n    title: {title}\\n"
            else:
                mermaid_title = "sequenceDiagram\\n"
            
            # Convert participants
            participant_pattern = r'participant\\s+"([^"]+)"\\s+as\\s+(\\w+)'
            actor_pattern = r'actor\\s+"([^"]+)"\\s+as\\s+(\\w+)'
            database_pattern = r'database\\s+"([^"]+)"\\s+as\\s+(\\w+)'
            
            def convert_participant_line(match):
                name = match.group(1)
                alias = match.group(2)
                return f"    participant {alias} as \\"{name}\\""
            
            content = re.sub(participant_pattern, convert_participant_line, content)
            content = re.sub(actor_pattern, lambda m: f"    actor {m.group(2)} as \\"{m.group(1)}\\"", content)
            content = re.sub(database_pattern, lambda m: f"    participant {m.group(2)} as \\"{m.group(1)}\\"", content)
            
            # Simple participants without quotes or aliases
            content = re.sub(r'participant\\s+(\\w+)\\s*$', r'    participant \\1', content, flags=re.MULTILINE)
            content = re.sub(r'actor\\s+(\\w+)\\s*$', r'    actor \\1', content, flags=re.MULTILINE)
            content = re.sub(r'database\\s+(\\w+)\\s*$', r'    participant \\1', content, flags=re.MULTILINE)
            
            # Convert arrows
            content = re.sub(r'(\\w+)\\s*->\\s*(\\w+)\\s*:\\s*(.*?)$', r'    \\1->>\\2: \\3', content, flags=re.MULTILINE)
            content = re.sub(r'(\\w+)\\s*-->\\s*(\\w+)\\s*:\\s*(.*?)$', r'    \\1-->>\\2: \\3', content, flags=re.MULTILINE)
            
            # Handle activation/deactivation
            content = re.sub(r'activate\\s+(\\w+)', r'    activate \\1', content)
            content = re.sub(r'deactivate\\s+(\\w+)', r'    deactivate \\1', content)
            
            # Handle notes
            content = re.sub(r'note\\s+(?:left|right)\\s+of\\s+(\\w+)\\s*:\\s*(.*?)$', 
                            r'    Note \\1: \\2', content, flags=re.MULTILINE)
            
            return mermaid_title + content.strip()
        
        elif "class" in content_lower or "<|--" in content_lower:
            # Class diagram
            mermaid_content = "classDiagram\\n"
            
            # Placeholder for full class diagram conversion
            return mermaid_content + "    " + content.strip().replace('\\n', '\\n    ')
            
        else:
            # Default to flowchart for other diagram types
            return f"graph TD\\n    A[PlantUML converted to Mermaid]\\n    B[Some features may not be fully supported]\\n    A --> B"
    """
    
    # Modify the renderer method for PlantUML
    renderer_modification = """
    elif diagram_type == 'plantuml':
            template = self.env.get_template('plantuml.html')
            # Add the raw PlantUML content to the context
            context['diagram_content'] = diagram_data.get('raw_content', '')
            # Generate image URL for PlantUML
            encoded_content = self._encode_plantuml(context['diagram_content'])
            context['diagram_image_url'] = f"{self.PLANTUML_SERVER}/svg/{encoded_content}"
            context['plantuml_server'] = self.PLANTUML_SERVER
            
            # Convert PlantUML to Mermaid as a fallback
            try:
                context['mermaid_content'] = self._convert_plantuml_to_mermaid(context['diagram_content'])
            except Exception as e:
                print(f"Warning: Failed to convert PlantUML to Mermaid: {e}")
                context['mermaid_content'] = f"graph TD\\n    A[Error converting PlantUML to Mermaid: {str(e).replace('"', '\\\\"')}]"
    """
    
    # Add the conversion function to the renderer class
    updated_content = renderer_content.replace(
        "class HTMLRenderer:",
        "class HTMLRenderer:" + conversion_code
    )
    
    # Modify the render method to include Mermaid conversion for PlantUML
    updated_content = updated_content.replace(
        """        elif diagram_type == 'plantuml':
            template = self.env.get_template('plantuml.html')
            # Add the raw PlantUML content to the context
            context['diagram_content'] = diagram_data.get('raw_content', '')
            # Generate image URL for PlantUML
            encoded_content = self._encode_plantuml(context['diagram_content'])
            context['diagram_image_url'] = f"{self.PLANTUML_SERVER}/svg/{encoded_content}"
            context['plantuml_server'] = self.PLANTUML_SERVER""",
        renderer_modification
    )
    
    # Write the modified renderer back
    with open(html_renderer_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Updated {html_renderer_path} to include PlantUML to Mermaid conversion")
    return True

def main():
    print("PyDiagrams Mermaid Renderer Fix Tool")
    print("===================================")
    
    # Update the HTML renderer to include PlantUML to Mermaid conversion
    if update_html_renderer():
        print("Successfully updated the HTML renderer.")
    else:
        print("Failed to update the HTML renderer.")
    
    # Update the PlantUML template to use Mermaid
    if update_html_renderer_template():
        print("Successfully updated the PlantUML template.")
    else:
        print("Failed to update the PlantUML template.")
    
    print("\nImportant: You need to regenerate any existing HTML outputs to use the updated renderer.")
    print("Run 'python generate_outputs.py' to regenerate all example diagrams.")

if __name__ == "__main__":
    main() 