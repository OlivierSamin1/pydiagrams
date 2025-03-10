"""
PlantUML syntax parser for PyDiagrams.

This module provides a parser for PlantUML syntax to convert it to PyDiagrams internal representation.
It also includes functionality to generate diagrams using the PlantUML server.
"""

import base64
import re
import zlib
from typing import Dict, Any, List, Tuple, Optional
import requests

from pydiagrams.parsers.base_parser import BaseParser


class PlantUMLParser(BaseParser):
    """Parser for PlantUML diagram syntax."""

    # Default PlantUML server URL
    PLANTUML_SERVER = "http://www.plantuml.com/plantuml"

    def __init__(self):
        """Initialize the PlantUML parser."""
        super().__init__()
        self.diagram_type = None

    def parse(self, content: str = None) -> Dict[str, Any]:
        """
        Parse PlantUML syntax and return a dictionary representing the diagram.

        Args:
            content: The PlantUML syntax to parse (uses self.content if None)

        Returns:
            A dictionary representing the parsed diagram
        """
        if content is not None:
            self.content = content

        content = self._preprocess_content(self.content)
        self.diagram_type = self._detect_diagram_type(content)
        
        if self.diagram_type == 'class':
            self.diagram_data = self._parse_class_diagram(content)
        elif self.diagram_type == 'sequence':
            self.diagram_data = self._parse_sequence_diagram(content)
        elif self.diagram_type == 'usecase':
            self.diagram_data = self._parse_usecase_diagram(content)
        elif self.diagram_type == 'activity':
            self.diagram_data = self._parse_activity_diagram(content)
        elif self.diagram_type == 'component':
            self.diagram_data = self._parse_component_diagram(content)
        elif self.diagram_type == 'state':
            self.diagram_data = self._parse_state_diagram(content)
        elif self.diagram_type == 'deployment':
            self.diagram_data = self._parse_deployment_diagram(content)
        elif self.diagram_type == 'er':
            self.diagram_data = self._parse_er_diagram(content)
        else:
            # For unsupported diagram types, we'll use direct rendering via PlantUML server
            self.diagram_data = {
                'type': self.diagram_type,
                'raw_content': content
            }
        
        return self.diagram_data

    def generate_svg(self, output_path: str = None) -> str:
        """
        Generate an SVG diagram using the PlantUML server.

        Args:
            output_path: Path where to save the SVG (if None, returns the SVG content)

        Returns:
            SVG content as string if output_path is None, otherwise the output path
        """
        if not self.content:
            raise ValueError("No content to generate diagram from")

        svg_content = self._generate_from_server(self.content, 'svg')
        
        if output_path:
            # For SVG, we need to decode bytes to string if it's not already a string
            if isinstance(svg_content, bytes):
                svg_content = svg_content.decode('utf-8')
                
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            return output_path
        
        return svg_content

    def generate_png(self, output_path: str) -> str:
        """
        Generate a PNG diagram using the PlantUML server.

        Args:
            output_path: Path where to save the PNG

        Returns:
            The output path
        """
        if not self.content:
            raise ValueError("No content to generate diagram from")

        png_content = self._generate_from_server(self.content, 'png')
        
        # PNG is always binary data
        with open(output_path, 'wb') as f:
            f.write(png_content)
        
        return output_path

    def _preprocess_content(self, content: str) -> str:
        """
        Preprocess the content to remove unnecessary parts.

        Args:
            content: The raw content to preprocess

        Returns:
            Preprocessed content
        """
        # Remove leading/trailing whitespace
        content = content.strip()
        
        # Ensure start and end tags exist
        if not content.startswith('@start'):
            content = '@startuml\n' + content
        if not content.endswith('@end'):
            content = content + '\n@enduml'
        
        return content

    def _detect_diagram_type(self, content: str) -> str:
        """
        Detect the PlantUML diagram type from content.

        Args:
            content: The PlantUML content

        Returns:
            Diagram type ('class', 'sequence', 'component', etc.)
        """
        # Check for explicit start tag
        start_match = re.search(r'@start(\w+)', content)
        if start_match:
            diagram_type = start_match.group(1).lower()
            
            # Map to our standard types
            if diagram_type == "uml":
                # Need to determine the type from content
                if 'class ' in content:
                    return 'class'
                elif "participant " in content or "->" in content:
                    return 'sequence'
                elif 'usecase ' in content or 'actor ' in content:
                    return 'usecase'
                elif 'component ' in content:
                    return 'component'
                elif 'state ' in content:
                    return 'state'
                elif 'node ' in content or 'database ' in content:
                    return 'deployment'
                elif 'entity ' in content:
                    return 'er'
                else:
                    # Default to class if unclear
                    return 'class'
            else:
                return diagram_type  # 'mindmap', 'wbs', etc.
        
        # Otherwise try to guess from content
        if 'class ' in content:
            return 'class'
        elif 'participant ' in content or '->' in content:
            return 'sequence'
        elif 'usecase ' in content or 'actor ' in content:
            return 'usecase'
        elif '(*) ->' in content or 'start' in content:
            return 'activity'
        elif 'component ' in content:
            return 'component'
        elif 'state ' in content:
            return 'state'
        elif 'node ' in content or 'database ' in content:
            return 'deployment'
        elif 'entity ' in content:
            return 'er'
        else:
            # Default to class if unclear
            return 'class'

    def _parse_class_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML class diagram syntax.

        Args:
            content: The class diagram content to parse

        Returns:
            Dictionary representing the parsed class diagram
        """
        classes = []
        relationships = []
        
        # Extract classes
        class_pattern = r'class\s+([^\s{<]+)(?:\s*<.*>)?(?:\s+as\s+([^\s{]+))?(?:\s*{([^}]*)})?'
        class_matches = re.finditer(class_pattern, content, re.DOTALL)
        
        for match in class_matches:
            class_name = match.group(1)
            class_alias = match.group(2) or class_name
            class_body = match.group(3) or ""
            
            class_info = {
                'name': class_name,
                'alias': class_alias,
                'attributes': [],
                'methods': []
            }
            
            # Extract attributes and methods
            for line in class_body.strip().split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if '(' in line and ')' in line:  # Method
                    class_info['methods'].append(line)
                else:  # Attribute
                    class_info['attributes'].append(line)
            
            classes.append(class_info)
        
        # Extract relationships
        rel_pattern = r'([^\s<>]+)\s*([<|.o*][-.|]+[>|.o*])\s*([^\s:]+)(?:\s*:\s*(.+))?'
        rel_matches = re.finditer(rel_pattern, content)
        
        for match in rel_matches:
            source = match.group(1)
            relationship = match.group(2)
            target = match.group(3)
            label = match.group(4) or ""
            
            # Determine relationship type
            rel_type = 'association'
            if '<|' in relationship or '|>' in relationship:
                rel_type = 'inheritance'
            elif 'o' in relationship:
                rel_type = 'aggregation'
            elif '*' in relationship:
                rel_type = 'composition'
            
            relationships.append({
                'source': source,
                'target': target,
                'type': rel_type,
                'label': label
            })
        
        return {
            'type': 'class',
            'classes': classes,
            'relationships': relationships
        }

    def _parse_sequence_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML sequence diagram syntax.

        Args:
            content: The sequence diagram content to parse

        Returns:
            Dictionary representing the parsed sequence diagram
        """
        participants = []
        messages = []
        
        # Extract participants
        participant_pattern = r'(participant|actor)\s+([^\s]+)(?:\s+as\s+([^\s]+))?(?:\s+(.+))?'
        participant_matches = re.finditer(participant_pattern, content)
        
        for match in participant_matches:
            p_type = match.group(1)
            p_name = match.group(2)
            p_alias = match.group(3) or p_name
            p_label = match.group(4) or p_name
            
            participants.append({
                'type': p_type,
                'name': p_name,
                'alias': p_alias,
                'label': p_label
            })
        
        # Extract messages
        message_pattern = r'([^\s-]+)\s*(->|-->|\-\\\\|\\\\->|<-|<--)\s*([^\s:]+)(?:\s*:\s*(.+))?'
        message_matches = re.finditer(message_pattern, content)
        
        for match in message_matches:
            sender = match.group(1)
            arrow = match.group(2)
            receiver = match.group(3)
            message = match.group(4) or ""
            
            # Determine message style
            style = 'solid'
            if '--' in arrow:
                style = 'dashed'
            
            # Determine direction
            is_response = '<' in arrow
            
            messages.append({
                'sender': sender,
                'receiver': receiver,
                'message': message,
                'style': style,
                'is_response': is_response
            })
        
        return {
            'type': 'sequence',
            'participants': participants,
            'messages': messages
        }

    def _parse_usecase_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML use case diagram syntax.

        Args:
            content: The use case diagram content to parse

        Returns:
            Dictionary representing the parsed use case diagram
        """
        actors = []
        usecases = []
        relationships = []
        
        # Extract actors
        actor_pattern = r'actor\s+([^\s]+)(?:\s+as\s+([^\s]+))?(?:\s*(.+))?'
        actor_matches = re.finditer(actor_pattern, content)
        
        for match in actor_matches:
            actor_name = match.group(1)
            actor_alias = match.group(2) or actor_name
            actor_label = match.group(3) or actor_name
            
            actors.append({
                'name': actor_name,
                'alias': actor_alias,
                'label': actor_label
            })
        
        # Extract use cases
        usecase_pattern = r'usecase\s+(?:"([^"]+)"|([^\s]+))(?:\s+as\s+([^\s]+))?'
        usecase_matches = re.finditer(usecase_pattern, content)
        
        for match in usecase_matches:
            usecase_name = match.group(1) or match.group(2)
            usecase_alias = match.group(3) or usecase_name
            
            usecases.append({
                'name': usecase_name,
                'alias': usecase_alias
            })
        
        # Extract relationships
        rel_pattern = r'([^\s]+)\s+(--|\.\.|\(|<|>|\)|-up-|-down-|-left-|-right-)\s+([^\s:]+)(?:\s*:\s*(.+))?'
        rel_matches = re.finditer(rel_pattern, content)
        
        for match in rel_matches:
            source = match.group(1)
            relation = match.group(2)
            target = match.group(3)
            label = match.group(4) or ""
            
            relationships.append({
                'source': source,
                'target': target,
                'relation': relation,
                'label': label
            })
        
        return {
            'type': 'usecase',
            'actors': actors,
            'usecases': usecases,
            'relationships': relationships
        }

    def _parse_activity_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML activity diagram syntax.

        Args:
            content: The activity diagram content to parse

        Returns:
            Dictionary representing the parsed activity diagram
        """
        activities = []
        transitions = []
        
        # Extract activities, decisions, etc.
        activity_pattern = r':([^;]+);'
        activity_matches = re.finditer(activity_pattern, content)
        
        for match in activity_matches:
            activity_name = match.group(1).strip()
            activities.append({
                'name': activity_name,
                'type': 'activity'
            })
        
        # Extract decisions
        decision_pattern = r'if\s+\("([^"]+)"\)'
        decision_matches = re.finditer(decision_pattern, content)
        
        for match in decision_matches:
            decision_name = match.group(1).strip()
            activities.append({
                'name': decision_name,
                'type': 'decision'
            })
        
        # Extract transitions
        transition_pattern = r'([^\s->]+)\s*(-+>)\s*([^\s;:]+)(?:\s*:\s*(.+))?'
        transition_matches = re.finditer(transition_pattern, content)
        
        for match in transition_matches:
            source = match.group(1)
            target = match.group(3)
            label = match.group(4) or ""
            
            transitions.append({
                'source': source,
                'target': target,
                'label': label
            })
        
        return {
            'type': 'activity',
            'activities': activities,
            'transitions': transitions
        }

    def _parse_component_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML component diagram syntax.

        Args:
            content: The component diagram content to parse

        Returns:
            Dictionary representing the parsed component diagram
        """
        components = []
        interfaces = []
        relationships = []
        
        # Extract components
        component_pattern = r'component\s+([^\s\[]+)(?:\s+as\s+([^\s\[]+))?(?:\s*\[([^\]]*)\])?'
        component_matches = re.finditer(component_pattern, content)
        
        for match in component_matches:
            comp_name = match.group(1)
            comp_alias = match.group(2) or comp_name
            comp_label = match.group(3) or comp_name
            
            components.append({
                'name': comp_name,
                'alias': comp_alias,
                'label': comp_label
            })
        
        # Extract interfaces
        interface_pattern = r'interface\s+([^\s]+)(?:\s+as\s+([^\s]+))?'
        interface_matches = re.finditer(interface_pattern, content)
        
        for match in interface_matches:
            intf_name = match.group(1)
            intf_alias = match.group(2) or intf_name
            
            interfaces.append({
                'name': intf_name,
                'alias': intf_alias
            })
        
        # Extract relationships
        rel_pattern = r'([^\s]+)\s+(\(|\)|\[|\]|<|>|-+)\s+([^\s:]+)(?:\s*:\s*(.+))?'
        rel_matches = re.finditer(rel_pattern, content)
        
        for match in rel_matches:
            source = match.group(1)
            relation = match.group(2)
            target = match.group(3)
            label = match.group(4) or ""
            
            relationships.append({
                'source': source,
                'target': target,
                'relation': relation,
                'label': label
            })
        
        return {
            'type': 'component',
            'components': components,
            'interfaces': interfaces,
            'relationships': relationships
        }

    def _parse_state_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML state diagram syntax.

        Args:
            content: The state diagram content to parse

        Returns:
            Dictionary representing the parsed state diagram
        """
        states = []
        transitions = []
        
        # Extract states
        state_pattern = r'state\s+(?:"([^"]+)"|([^\s{:]+))(?:\s+as\s+([^\s{:]+))?'
        state_matches = re.finditer(state_pattern, content)
        
        for match in state_matches:
            state_name = match.group(1) or match.group(2)
            state_alias = match.group(3) or state_name
            
            states.append({
                'name': state_name,
                'alias': state_alias
            })
        
        # Extract transitions
        trans_pattern = r'([^\s:]+)\s*(-+>)\s*([^\s:]+)(?:\s*:\s*(.+))?'
        trans_matches = re.finditer(trans_pattern, content)
        
        for match in trans_matches:
            source = match.group(1)
            target = match.group(3)
            label = match.group(4) or ""
            
            transitions.append({
                'source': source,
                'target': target,
                'label': label
            })
        
        return {
            'type': 'state',
            'states': states,
            'transitions': transitions
        }

    def _parse_deployment_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML deployment diagram syntax.

        Args:
            content: The deployment diagram content to parse

        Returns:
            Dictionary representing the parsed deployment diagram
        """
        nodes = []
        artifacts = []
        relationships = []
        
        # Extract nodes (servers, devices, etc.)
        node_pattern = r'(node|cloud|database|frame)\s+(?:"([^"]+)"|([^\s\[]+))(?:\s+as\s+([^\s\[]+))?(?:\s*\[([^\]]*)\])?'
        node_matches = re.finditer(node_pattern, content)
        
        for match in node_matches:
            node_type = match.group(1)
            node_name = match.group(2) or match.group(3)
            node_alias = match.group(4) or node_name
            node_label = match.group(5) or node_name
            
            nodes.append({
                'type': node_type,
                'name': node_name,
                'alias': node_alias,
                'label': node_label
            })
        
        # Extract artifacts
        artifact_pattern = r'artifact\s+(?:"([^"]+)"|([^\s\[]+))(?:\s+as\s+([^\s\[]+))?(?:\s*\[([^\]]*)\])?'
        artifact_matches = re.finditer(artifact_pattern, content)
        
        for match in artifact_matches:
            art_name = match.group(1) or match.group(2)
            art_alias = match.group(3) or art_name
            art_label = match.group(4) or art_name
            
            artifacts.append({
                'name': art_name,
                'alias': art_alias,
                'label': art_label
            })
        
        # Extract relationships
        rel_pattern = r'([^\s]+)\s*(-+>|\.\.>|--|\.\.|<-+>)\s*([^\s:]+)(?:\s*:\s*(.+))?'
        rel_matches = re.finditer(rel_pattern, content)
        
        for match in rel_matches:
            source = match.group(1)
            relation = match.group(2)
            target = match.group(3)
            label = match.group(4) or ""
            
            relationships.append({
                'source': source,
                'target': target,
                'relation': relation,
                'label': label
            })
        
        return {
            'type': 'deployment',
            'nodes': nodes,
            'artifacts': artifacts,
            'relationships': relationships
        }

    def _parse_er_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse PlantUML ER diagram syntax.

        Args:
            content: The ER diagram content to parse

        Returns:
            Dictionary representing the parsed ER diagram
        """
        entities = []
        relationships = []
        
        # Extract entities
        entity_pattern = r'entity\s+(?:"([^"]+)"|([^\s{]+))(?:\s+as\s+([^\s{]+))?(?:\s*{([^}]*)})?'
        entity_matches = re.finditer(entity_pattern, content, re.DOTALL)
        
        for match in entity_matches:
            entity_name = match.group(1) or match.group(2)
            entity_alias = match.group(3) or entity_name
            entity_body = match.group(4) or ""
            
            entity = {
                'name': entity_name,
                'alias': entity_alias,
                'attributes': []
            }
            
            # Extract attributes
            for line in entity_body.strip().split('\n'):
                line = line.strip()
                if line:
                    entity['attributes'].append(line)
            
            entities.append(entity)
        
        # Extract relationships
        rel_pattern = r'([^\s"]+|"[^"]+")\s*(?:([#*o|])?-+([#*o|])?\s*([^\s"]+|"[^"]+")|([#*o|])?\.\.([#*o|])?\s*([^\s"]+|"[^"]+"))(?:\s*:\s*(.+))?'
        rel_matches = re.finditer(rel_pattern, content)
        
        for match in rel_matches:
            if match.group(4):  # Solid line relation
                source = match.group(1).strip('"')
                left_cardinality = match.group(2) or ""
                right_cardinality = match.group(3) or ""
                target = match.group(4).strip('"')
                style = 'solid'
            else:  # Dotted line relation
                source = match.group(1).strip('"')
                left_cardinality = match.group(5) or ""
                right_cardinality = match.group(6) or ""
                target = match.group(7).strip('"')
                style = 'dotted'
            
            label = match.group(8) or ""
            
            relationships.append({
                'source': source,
                'target': target,
                'left_cardinality': left_cardinality,
                'right_cardinality': right_cardinality,
                'label': label,
                'style': style
            })
        
        return {
            'type': 'er',
            'entities': entities,
            'relationships': relationships
        }

    def _generate_from_server(self, content: str, format_type: str = 'svg') -> bytes:
        """
        Generate diagram using PlantUML server.

        Args:
            content: PlantUML content
            format_type: Output format ('svg', 'png')

        Returns:
            Content in the specified format
        """
        plantuml_url = f"{self.PLANTUML_SERVER}/{format_type}"
        
        # Encode the PlantUML content
        encoded = self._encode_plantuml(content)
        url = f"{plantuml_url}/{encoded}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            raise RuntimeError(f"Error generating diagram from PlantUML server: {e}")

    @staticmethod
    def _encode_plantuml(text: str) -> str:
        """
        Encode PlantUML text for use with the PlantUML server.

        Args:
            text: PlantUML text

        Returns:
            Encoded string for URL
        """
        # Add the ~1 prefix to indicate DEFLATE encoding
        # Convert to UTF-8 and compress with zlib
        zlibbed = zlib.compress(text.encode('utf-8'))
        
        # Convert to base64 and replace unsafe characters
        compressed = base64.b64encode(zlibbed).decode('ascii')
        compressed = compressed.replace('+', '-').replace('/', '_')
        
        # Add ~1 prefix to indicate DEFLATE encoding
        return f"~1{compressed}" 