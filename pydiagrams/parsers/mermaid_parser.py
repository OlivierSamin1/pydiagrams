"""
Mermaid syntax parser for PyDiagrams.

This module provides a parser for Mermaid syntax to convert it to PyDiagrams internal representation.
"""

import re
from typing import Dict, Any, List, Tuple, Optional

from pydiagrams.parsers.base_parser import BaseParser


class MermaidParser(BaseParser):
    """Parser for Mermaid diagram syntax."""

    def __init__(self):
        """Initialize the Mermaid parser."""
        super().__init__()
        self.diagram_type = None

    def parse(self, content: str = None) -> Dict[str, Any]:
        """
        Parse Mermaid syntax and return a dictionary representing the diagram.

        Args:
            content: The Mermaid syntax to parse (uses self.content if None)

        Returns:
            A dictionary representing the parsed diagram
        """
        if content is not None:
            self.content = content

        content = self._preprocess_content(self.content)
        self.diagram_type = self._detect_diagram_type(content)
        
        if self.diagram_type == 'flowchart':
            self.diagram_data = self._parse_flowchart(content)
        elif self.diagram_type == 'sequence':
            self.diagram_data = self._parse_sequence_diagram(content)
        elif self.diagram_type == 'class':
            self.diagram_data = self._parse_class_diagram(content)
        elif self.diagram_type == 'state':
            self.diagram_data = self._parse_state_diagram(content)
        elif self.diagram_type == 'er':
            self.diagram_data = self._parse_er_diagram(content)
        else:
            raise ValueError(f"Unsupported Mermaid diagram type: {self.diagram_type}")
        
        return self.diagram_data

    def _preprocess_content(self, content: str) -> str:
        """
        Preprocess the content to remove unnecessary parts.

        Args:
            content: The raw content to preprocess

        Returns:
            Preprocessed content
        """
        # Remove Markdown code block markers if present
        content = re.sub(r'```mermaid\s*\n', '', content)
        content = re.sub(r'```\s*$', '', content)
        
        # Remove comments
        content = re.sub(r'%%.*?$', '', content, flags=re.MULTILINE)
        
        return content.strip()

    def _detect_diagram_type(self, content: str) -> str:
        """
        Detect the Mermaid diagram type from content.

        Args:
            content: The Mermaid content

        Returns:
            Diagram type ('flowchart', 'sequence', 'class', 'state', 'er')
        """
        first_line = content.strip().lower().split('\n')[0].strip().lower()
        
        if first_line.startswith(('graph ', 'flowchart ')):
            # Check for class diagram content if first line does not match
            if "class " in content and "{" in content and "}" in content:
                return "class"
            return 'flowchart'
        elif first_line.startswith('sequencediagram'):
            return 'sequence'
        elif first_line.startswith('classDiagram'):
            return 'class'
        elif first_line.startswith('stateDiagram'):
            return 'state'
        elif first_line.startswith('erDiagram'):
            return 'er'
        else:
            # Default to flowchart for unrecognized types
            # Check for class diagram content if first line does not match
            if "class " in content and "{" in content and "}" in content:
                return "class"
            return 'flowchart'

    def _parse_flowchart(self, content: str) -> Dict[str, Any]:
        """
        Parse Mermaid flowchart/graph syntax.

        Args:
            content: The flowchart content to parse

        Returns:
            Dictionary representing the parsed flowchart
        """
        nodes = []
        edges = []
        
        # Extract direction
        direction_match = re.search(r'graph\s+([TBLR]D|RL)', content)
        direction = direction_match.group(1) if direction_match else 'TD'
        
        # Extract nodes and edges
        lines = content.split('\n')
        for line in lines[1:]:  # Skip the first line which has the graph definition
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Check for node definitions
            node_match = re.search(r'^\s*([A-Za-z0-9_-]+)\s*\["?([^"]*)"?\]', line)
            if node_match:
                node_id, node_label = node_match.groups()
                nodes.append({
                    'id': node_id,
                    'label': node_label or node_id,
                    'shape': 'rectangle'
                })
                continue
                
            # Check for edge definitions
            edge_match = re.search(r'([A-Za-z0-9_-]+)\s*(-[->]|==|--[>x]|-.|-\|>|-o|<-[>x]|-\||o-)\s*([A-Za-z0-9_-]+)', line)
            if edge_match:
                source, edge_type, target = edge_match.groups()
                
                # Determine edge style based on edge_type
                style = 'solid'
                if '==' in edge_type:
                    style = 'bold'
                elif '--' in edge_type:
                    style = 'dashed'
                
                # Determine if there's an arrowhead
                directed = '>' in edge_type or 'x' in edge_type or 'o' in edge_type or '|' in edge_type
                
                edges.append({
                    'source': source,
                    'target': target,
                    'style': style,
                    'directed': directed
                })
        
        return {
            'type': 'flowchart',
            'direction': direction,
            'nodes': nodes,
            'edges': edges
        }

    def _parse_sequence_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse Mermaid sequence diagram syntax.

        Args:
            content: The sequence diagram content to parse

        Returns:
            Dictionary representing the parsed sequence diagram
        """
        actors = []
        messages = []
        
        lines = content.split('\n')
        for line in lines[1:]:  # Skip the first line with diagram definition
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Check for participant definitions
            participant_match = re.search(r'participant\s+([^\s]+)(?:\s+as\s+(.+))?', line)
            if participant_match:
                actor_id, actor_label = participant_match.groups()
                actors.append({
                    'id': actor_id,
                    'label': actor_label or actor_id
                })
                continue
                
            # Check for message definitions
            message_match = re.search(r'([^\s-]+)\s*(->>|-->|->|\.\.\>)\s*([^\s:]+)\s*:\s*(.+)', line)
            if message_match:
                sender, arrow, receiver, message_text = message_match.groups()
                
                # Determine message style based on arrow
                style = 'solid'
                if '-->' in arrow:
                    style = 'dashed'
                elif '..' in arrow:
                    style = 'dotted'
                
                messages.append({
                    'sender': sender,
                    'receiver': receiver,
                    'message': message_text,
                    'style': style
                })
        
        return {
            'type': 'sequence',
            'actors': actors,
            'messages': messages
        }

    def _parse_class_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse Mermaid class diagram syntax.

        Args:
            content: The class diagram content to parse

        Returns:
            Dictionary representing the parsed class diagram
        """
        classes = []
        relationships = []
        
        lines = content.split('\n')
        current_class = None
        
        for line in lines[1:]:  # Skip the first line with diagram definition
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Check for class definitions
            class_match = re.search(r'class\s+([^\s{]+)(\s*{)?', line)
            if class_match:
                class_name = class_match.group(1)
                current_class = {
                    'name': class_name,
                    'attributes': [],
                    'methods': []
                }
                classes.append(current_class)
                continue
                
            # Check for class member definitions
            if current_class and '{' in line:
                current_class = classes[-1]  # Make sure we're adding to the last class
                continue
                
            if current_class and '}' in line:
                current_class = None
                continue
                
            if current_class:
                # Check for attribute or method
                if '()' in line:
                    # It's a method
                    method_match = re.search(r'([^:]+)(?:\s*:\s*(.+))?', line)
                    if method_match:
                        method_name, return_type = method_match.groups()
                        method_name = method_name.strip()
                        current_class['methods'].append({
                            'name': method_name,
                            'return_type': return_type.strip() if return_type else None
                        })
                else:
                    # It's an attribute
                    attr_match = re.search(r'([^:]+)\s*:\s*(.+)', line)
                    if attr_match:
                        attr_name, attr_type = attr_match.groups()
                        current_class['attributes'].append({
                            'name': attr_name.strip(),
                            'type': attr_type.strip()
                        })
                continue
                
            # Check for relationship definitions
            rel_match = re.search(r'([^\s]+)\s+(\.|<\|--|o--|<--|\*--|<\.\.|\.\.|-->|--|\|>|o|>|\*)\s+([^\s:]+)(?:\s*:\s*(.+))?', line)
            if rel_match:
                source, relation_type, target, label = rel_match.groups()
                relationships.append({
                    'source': source,
                    'target': target,
                    'type': relation_type,
                    'label': label
                })
        
        return {
            'type': 'class',
            'classes': classes,
            'relationships': relationships
        }

    def _parse_state_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse Mermaid state diagram syntax.

        Args:
            content: The state diagram content to parse

        Returns:
            Dictionary representing the parsed state diagram
        """
        states = []
        transitions = []
        
        lines = content.split('\n')
        for line in lines[1:]:  # Skip the first line with diagram definition
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Check for state definitions
            state_match = re.search(r'state\s+"?([^"{\s]+)"?(?:\s+as\s+([^\s{]+))?(\s*{)?', line)
            if state_match:
                state_name, state_alias, has_nested = state_match.groups()
                states.append({
                    'name': state_name,
                    'alias': state_alias,
                    'is_container': bool(has_nested)
                })
                continue
                
            # Check for transition definitions
            trans_match = re.search(r'([^\s-]+)\s*-->\s*([^\s:]+)(?:\s*:\s*(.+))?', line)
            if trans_match:
                source, target, label = trans_match.groups()
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

    def _parse_er_diagram(self, content: str) -> Dict[str, Any]:
        """
        Parse Mermaid ER diagram syntax.

        Args:
            content: The ER diagram content to parse

        Returns:
            Dictionary representing the parsed ER diagram
        """
        entities = []
        relationships = []
        
        lines = content.split('\n')
        for line in lines[1:]:  # Skip the first line with diagram definition
            line = line.strip()
            if not line or line.startswith('%'):
                continue
                
            # Check for entity definitions
            entity_match = re.search(r'([A-Za-z0-9_-]+)\s*{', line)
            if entity_match:
                entity_name = entity_match.group(1)
                entities.append({
                    'name': entity_name,
                    'attributes': []
                })
                continue
                
            # Check for attribute definitions
            attr_match = re.search(r'([A-Za-z0-9_-]+)\s+([A-Za-z0-9_-]+)(?:\s+([A-Za-z0-9_-]+))?', line)
            if attr_match and entities:
                attr_name, attr_type, constraint = attr_match.groups()
                entities[-1]['attributes'].append({
                    'name': attr_name,
                    'type': attr_type,
                    'constraint': constraint
                })
                continue
                
            # Check for relationship definitions
            rel_match = re.search(r'([A-Za-z0-9_-]+)\s+(\|o|o\||\|\||\}o|o\{|\}\||\|\{|\.\.)\s*([A-Za-z0-9_-]+)\s*(\|o|o\||\|\||\}o|o\{|\}\||\|\{|\.\.)\s*([A-Za-z0-9_-]+)\s*:\s*"([^"]*)"', line)
            if rel_match:
                entity1, cardinality1, relationship_name, cardinality2, entity2, label = rel_match.groups()
                relationships.append({
                    'entity1': entity1,
                    'cardinality1': cardinality1,
                    'name': relationship_name,
                    'cardinality2': cardinality2,
                    'entity2': entity2,
                    'label': label
                })
        
        return {
            'type': 'er',
            'entities': entities,
            'relationships': relationships
        } 