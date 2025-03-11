#!/usr/bin/env python3
"""
Script to convert PlantUML diagrams to Mermaid format
"""
import os
import re
import sys
from pathlib import Path

def convert_sequence_diagram(content):
    """
    Convert PlantUML sequence diagram to Mermaid format
    """
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    # Convert title
    title_match = re.search(r'title\s+(.*?)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        content = re.sub(r'title\s+.*?\n', '', content)
        mermaid_title = f"sequenceDiagram\n    title: {title}\n"
    else:
        mermaid_title = "sequenceDiagram\n"
    
    # Convert participants
    # In PlantUML: participant "Name" as Alias
    # In Mermaid: participant Alias as "Name"
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
    # PlantUML: A -> B: Message
    # Mermaid: A->>B: Message
    content = re.sub(r'(\w+)\s*->\s*(\w+)\s*:\s*(.*?)$', r'    \1->>\2: \3', content, flags=re.MULTILINE)
    content = re.sub(r'(\w+)\s*-->\s*(\w+)\s*:\s*(.*?)$', r'    \1-->>\2: \3', content, flags=re.MULTILINE)
    
    # Handle activation/deactivation
    content = re.sub(r'activate\s+(\w+)', r'    activate \1', content)
    content = re.sub(r'deactivate\s+(\w+)', r'    deactivate \1', content)
    
    # Handle notes
    content = re.sub(r'note\s+(?:left|right)\s+of\s+(\w+)\s*:\s*(.*?)$', 
                     r'    Note \1: \2', content, flags=re.MULTILINE)
    
    return mermaid_title + content.strip()

def convert_class_diagram(content):
    """
    Convert PlantUML class diagram to Mermaid format
    """
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    # Start with class diagram declaration
    mermaid_content = "classDiagram\n"
    
    # Convert class definitions
    # PlantUML: class ClassName { members }
    # Mermaid: class ClassName { members }
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
    # PlantUML: ClassA -- ClassB : Label
    # Mermaid: ClassA -- ClassB : Label
    
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

def convert_component_diagram(content):
    """
    Convert PlantUML component diagram to Mermaid format
    """
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    # Start with flowchart declaration
    mermaid_content = "graph TD\n"
    
    # Convert components
    # PlantUML: [Component]
    # Mermaid: Component[Component]
    component_pattern = r'\[([^\]]+)\]'
    content = re.sub(component_pattern, r'    \1[\1]', content)
    
    # Convert interfaces
    # PlantUML: () "Interface"
    # Mermaid: Interface((Interface))
    interface_pattern = r'\(\)\s*"([^"]+)"'
    content = re.sub(interface_pattern, r'    \1((\1))', content)
    
    # Convert databases
    # PlantUML: database "Database"
    # Mermaid: Database[(Database)]
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
    # PlantUML: ComponentA -> ComponentB
    # Mermaid: ComponentA --> ComponentB
    content = re.sub(r'(\w+)\s*-+>\s*(\w+)', r'    \1 --> \2', content)
    
    # Convert labels
    # PlantUML: ComponentA -> ComponentB : Label
    # Mermaid: ComponentA -->|Label| ComponentB
    content = re.sub(r'(\w+)\s*-+>\s*(\w+)\s*:\s*([^\n]+)', r'    \1 -->|\3| \2', content)
    
    return mermaid_content + content.strip()

def convert_state_diagram(content):
    """
    Convert PlantUML state diagram to Mermaid format
    """
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    # Start with stateDiagram declaration
    mermaid_content = "stateDiagram-v2\n"
    
    # Convert states
    # PlantUML: state "State Name" as S1
    # Mermaid: S1: State Name
    state_pattern = r'state\s+"([^"]+)"\s+as\s+(\w+)'
    content = re.sub(state_pattern, r'    \2: \1', content)
    
    # Convert simple states
    # PlantUML: state StateName
    # Mermaid: StateName
    content = re.sub(r'state\s+(\w+)(?!\s*:)', r'    \1', content)
    
    # Convert start and end states
    # PlantUML: [*] -> State1
    # Mermaid: [*] --> State1
    content = re.sub(r'\[\*\]\s*-+>\s*(\w+)', r'    [*] --> \1', content)
    content = re.sub(r'(\w+)\s*-+>\s*\[\*\]', r'    \1 --> [*]', content)
    
    # Convert transitions
    # PlantUML: State1 -> State2 : Event
    # Mermaid: State1 --> State2 : Event
    content = re.sub(r'(\w+)\s*-+>\s*(\w+)(?:\s*:\s*([^\n]*))?', 
                     lambda m: f"    {m.group(1)} --> {m.group(2)}{': ' + m.group(3) if m.group(3) else ''}", 
                     content)
    
    # Convert compound states
    content = re.sub(r'state\s+(\w+)\s*{([^}]*)}', 
                  lambda m: f"    state {m.group(1)} {{\n" + 
                            '\n'.join([f"        {line.strip()}" for line in m.group(2).strip().split('\n')]) + 
                            "\n    }",
                  content)
    
    return mermaid_content + content.strip()

def convert_er_diagram(content):
    """
    Convert PlantUML ER diagram to Mermaid format
    """
    # Remove @startuml and @enduml tags
    content = re.sub(r'@startuml.*?\n', '', content)
    content = re.sub(r'@enduml.*?\n', '', content)
    
    # Start with erDiagram declaration
    mermaid_content = "erDiagram\n"
    
    # Convert entity definitions
    # PlantUML: entity Entity { attributes }
    # Mermaid: ENTITY { attributes }
    entity_pattern = r'entity\s+(\w+)(?:\s*{([^}]*)})?'
    
    def convert_entity(match):
        entity_name = match.group(1).upper()
        attributes = match.group(2) if match.group(2) else ""
        
        # Format attributes if present
        if attributes:
            formatted_attrs = []
            for line in attributes.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # Convert attributes
                if ':' in line:  # It's already in format name : type
                    formatted_attrs.append(f"        {line}")
                else:  # Add default type
                    formatted_attrs.append(f"        {line} : string")
            
            if formatted_attrs:
                return f"    {entity_name} {{\n" + "\n".join(formatted_attrs) + "\n    }"
            else:
                return f"    {entity_name}"
        else:
            return f"    {entity_name}"
    
    content = re.sub(entity_pattern, convert_entity, content)
    
    # Convert relationships
    # PlantUML: Entity1 }|--|| Entity2
    # Mermaid: ENTITY1 ||--o{ ENTITY2 : "relationship"
    
    # One-to-many
    content = re.sub(r'(\w+)\s+}o?--\|\|?\s+(\w+)(?:\s*:\s*([^\n]+))?', 
                     lambda m: f"    {m.group(1).upper()} ||--o{{ {m.group(2).upper()}" + 
                               (f" : \"{m.group(3)}\"" if m.group(3) else ""),
                     content)
    
    # Many-to-one
    content = re.sub(r'(\w+)\s+\|\|?--o?{\s+(\w+)(?:\s*:\s*([^\n]+))?', 
                     lambda m: f"    {m.group(1).upper()} }}o--|| {m.group(2).upper()}" + 
                               (f" : \"{m.group(3)}\"" if m.group(3) else ""),
                     content)
    
    # One-to-one
    content = re.sub(r'(\w+)\s+\|--\|\s+(\w+)(?:\s*:\s*([^\n]+))?', 
                     lambda m: f"    {m.group(1).upper()} ||--|| {m.group(2).upper()}" + 
                               (f" : \"{m.group(3)}\"" if m.group(3) else ""),
                     content)
    
    # Many-to-many
    content = re.sub(r'(\w+)\s+}--{\s+(\w+)(?:\s*:\s*([^\n]+))?', 
                     lambda m: f"    {m.group(1).upper()} }}o--o{{ {m.group(2).upper()}" + 
                               (f" : \"{m.group(3)}\"" if m.group(3) else ""),
                     content)
    
    return mermaid_content + content.strip()

def detect_diagram_type(content):
    """
    Detect the type of PlantUML diagram based on content
    """
    content = content.lower()
    
    if "actor" in content or "participant" in content or "->" in content and not "class" in content:
        return "sequence"
    elif "class" in content or "<|--" in content:
        return "class"
    elif "state" in content:
        return "state"
    elif "entity" in content or "}|--||" in content:
        return "er"
    elif "component" in content or "package" in content or "[" in content and "]" in content:
        return "component"
    else:
        return "sequence"  # Default to sequence diagram

def convert_plantuml_to_mermaid(content):
    """
    Convert PlantUML diagram to Mermaid format based on diagram type
    """
    diagram_type = detect_diagram_type(content)
    
    if diagram_type == "sequence":
        return convert_sequence_diagram(content)
    elif diagram_type == "class":
        return convert_class_diagram(content)
    elif diagram_type == "component":
        return convert_component_diagram(content)
    elif diagram_type == "state":
        return convert_state_diagram(content)
    elif diagram_type == "er":
        return convert_er_diagram(content)
    else:
        return f"graph TD\n    A[\"Could not convert diagram type: {diagram_type}\"]"

def create_mermaid_html(output_path, content):
    """
    Create a Mermaid HTML file from the given content
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Diagram (Converted from PlantUML)</title>
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
        
        .note {{
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin-top: 20px;
            border-radius: 4px;
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
    <h1>Diagram (Converted from PlantUML)</h1>
    <div class="container">
        <div class="mermaid">
{content}
        </div>
        <div class="buttons">
            <button id="dark-mode">Toggle Dark Mode</button>
        </div>
        <div class="note">
            <p><strong>Note:</strong> This diagram was automatically converted from PlantUML to Mermaid format.</p>
        </div>
    </div>
</body>
</html>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return output_path

def process_plantuml_files():
    """
    Process all PlantUML files in the examples directory
    """
    current_dir = Path.cwd()
    examples_dir = current_dir / "examples"
    output_dir = current_dir / "converted_output"
    output_dir.mkdir(exist_ok=True)
    
    # Get all PlantUML files
    plantuml_files = list(examples_dir.glob("*.puml"))
    
    print(f"Found {len(plantuml_files)} PlantUML files.")
    
    # Process each file
    successful_outputs = []
    for plantuml_file in plantuml_files:
        mermaid_output_file = output_dir / f"{plantuml_file.stem}_mermaid.html"
        print(f"Processing {plantuml_file}...")
        
        try:
            # Read the content of the PlantUML file
            with open(plantuml_file, 'r', encoding='utf-8') as f:
                plantuml_content = f.read().strip()
            
            # Convert to Mermaid
            mermaid_content = convert_plantuml_to_mermaid(plantuml_content)
            
            # Create HTML file with Mermaid content
            output_path = create_mermaid_html(mermaid_output_file, mermaid_content)
            
            successful_outputs.append(output_path)
            print(f"Created {mermaid_output_file}")
        except Exception as e:
            print(f"Error processing {plantuml_file}: {e}")
    
    # Open all successful outputs in browser
    if successful_outputs:
        print(f"\nGenerated {len(successful_outputs)} converted files.")
        print("Opening files in browser...")
        import webbrowser
        for output_path in successful_outputs:
            file_url = f"file://{output_path.absolute()}"
            print(f"Opening {file_url}")
            webbrowser.open_new_tab(file_url)

def main():
    print("PlantUML to Mermaid Converter")
    print("=============================")
    
    # Process PlantUML files in examples directory
    process_plantuml_files()

if __name__ == "__main__":
    main() 