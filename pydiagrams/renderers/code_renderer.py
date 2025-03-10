#!/usr/bin/env python3
"""
Code Diagram Renderer module for PyDiagrams.

This module provides a renderer for Code Diagrams using Graphviz.
"""

import os
from typing import Dict, List, Optional, Set, Tuple, Any
import graphviz

from pydiagrams.diagrams.code.code_diagram import (
    CodeDiagram,
    CodeElement,
    Module,
    Class,
    Interface,
    Function,
    Variable,
    Enum,
    CodeRelationship,
    CodeElementType,
    RelationshipType,
    AccessModifier
)


class CodeRenderer:
    """Renderer for Code Diagrams using Graphviz."""
    
    def __init__(self, diagram: CodeDiagram):
        """
        Initialize the Code Diagram renderer.
        
        Args:
            diagram: The Code Diagram to render
        """
        self.diagram = diagram
        self.graph = None
        
        # Mapping of access modifiers to symbols
        self.access_symbols = {
            AccessModifier.PUBLIC: "+",
            AccessModifier.PRIVATE: "-",
            AccessModifier.PROTECTED: "#",
            AccessModifier.PACKAGE: "~",
            AccessModifier.INTERNAL: "^"
        }
        
        # Mapping of relationship types to edge styles
        self.relationship_styles = {
            RelationshipType.IMPORT: {
                'style': 'dashed',
                'color': '#4C566A',
                'arrowhead': 'vee',
                'label': 'imports'
            },
            RelationshipType.INHERITANCE: {
                'style': 'solid',
                'color': '#5E81AC',
                'arrowhead': 'empty',
                'label': 'extends'
            },
            RelationshipType.IMPLEMENTATION: {
                'style': 'dashed',
                'color': '#5E81AC',
                'arrowhead': 'empty',
                'label': 'implements'
            },
            RelationshipType.DEPENDENCY: {
                'style': 'dashed',
                'color': '#BF616A',
                'arrowhead': 'vee',
                'label': 'uses'
            },
            RelationshipType.COMPOSITION: {
                'style': 'solid',
                'color': '#D08770',
                'arrowhead': 'diamond',
                'label': 'has'
            },
            RelationshipType.AGGREGATION: {
                'style': 'solid',
                'color': '#EBCB8B',
                'arrowhead': 'odiamond',
                'label': 'has'
            },
            RelationshipType.CALL: {
                'style': 'solid',
                'color': '#A3BE8C',
                'arrowhead': 'vee',
                'label': 'calls'
            },
            RelationshipType.ACCESS: {
                'style': 'dotted',
                'color': '#B48EAD',
                'arrowhead': 'vee',
                'label': 'accesses'
            },
            RelationshipType.REFERENCE: {
                'style': 'dashed',
                'color': '#88C0D0',
                'arrowhead': 'vee',
                'label': 'references'
            }
        }
        
        # Element colors based on type
        self.element_colors = {
            CodeElementType.MODULE: "#ECEFF4",
            CodeElementType.CLASS: "#E5E9F0",
            CodeElementType.INTERFACE: "#D8DEE9",
            CodeElementType.FUNCTION: "#E5E9F0",
            CodeElementType.VARIABLE: "#E5E9F0",
            CodeElementType.ENUM: "#E5E9F0"
        }
        
        # Element header colors based on type
        self.header_colors = {
            CodeElementType.MODULE: "#8FBCBB",
            CodeElementType.CLASS: "#88C0D0",
            CodeElementType.INTERFACE: "#81A1C1",
            CodeElementType.FUNCTION: "#A3BE8C",
            CodeElementType.VARIABLE: "#D08770",
            CodeElementType.ENUM: "#B48EAD"
        }
    
    def _setup_graph(self):
        """Setup the graphviz graph with proper attributes."""
        self.graph = graphviz.Digraph(
            name=self.diagram.name,
            comment=self.diagram.description,
            format='svg',
            engine='dot'
        )
        
        # Set global graph attributes
        self.graph.attr(
            rankdir='TB',  # Top to Bottom layout
            splines='ortho',
            nodesep='0.8',
            ranksep='1.0',
            fontname='Arial',
            fontsize='12',
            dpi='300'
        )
        
        # Set default node and edge attributes
        self.graph.attr('node', shape='plain', fontname='Arial', fontsize='10')
        self.graph.attr('edge', fontname='Arial', fontsize='9')
    
    def _get_access_symbol(self, access_modifier: Optional[AccessModifier]) -> str:
        """Get the symbol representing an access modifier."""
        if access_modifier is None:
            return ""
        return self.access_symbols.get(access_modifier, "")
    
    def _format_function_signature(self, function: Function) -> str:
        """Format a function signature for display."""
        # Format parameters
        params_str = ", ".join([f"{name}: {param_type}" for name, param_type in function.parameters])
        
        # Format return type
        return_str = f" : {function.return_type}" if function.return_type else ""
        
        # Format access modifier
        access_symbol = self._get_access_symbol(function.access_modifier)
        
        # Format modifiers
        modifiers = []
        if function.is_static:
            modifiers.append("static")
        if function.is_abstract:
            modifiers.append("abstract")
        if function.is_final:
            modifiers.append("final")
        
        modifiers_str = " ".join(modifiers)
        if modifiers_str:
            modifiers_str = f"{modifiers_str} "
        
        return f"{access_symbol} {modifiers_str}{function.name}({params_str}){return_str}"
    
    def _format_variable_signature(self, variable: Variable) -> str:
        """Format a variable signature for display."""
        # Format access modifier
        access_symbol = self._get_access_symbol(variable.access_modifier)
        
        # Format type
        type_str = f" : {variable.var_type}" if variable.var_type else ""
        
        # Format initial value
        init_value_str = f" = {variable.initial_value}" if variable.initial_value is not None else ""
        
        # Format modifiers
        modifiers = []
        if variable.is_static:
            modifiers.append("static")
        if variable.is_final:
            modifiers.append("final")
        if variable.is_constant:
            modifiers.append("const")
        
        modifiers_str = " ".join(modifiers)
        if modifiers_str:
            modifiers_str = f"{modifiers_str} "
        
        return f"{access_symbol} {modifiers_str}{variable.name}{type_str}{init_value_str}"
    
    def _render_class(self, class_obj: Class):
        """Render a class as an HTML-like table."""
        class_id = class_obj.id
        
        # Start building the HTML-like label for the class
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Class name header (with stereotype for abstract classes)
        stereotype = ""
        if class_obj.is_abstract:
            stereotype = "\\n«abstract»"
        
        # Determine modifiers
        modifiers = []
        if class_obj.is_static:
            modifiers.append("static")
        if class_obj.is_final:
            modifiers.append("final")
        
        modifiers_str = ""
        if modifiers:
            modifiers_str = f"\\n«{' '.join(modifiers)}»"
        
        # Class name row (header)
        header_color = self.header_colors[CodeElementType.CLASS]
        label += f'<TR><TD BGCOLOR="{header_color}" COLSPAN="1"><B>{class_obj.name}{stereotype}{modifiers_str}</B></TD></TR>'
        
        # Add superclasses if any
        if class_obj.superclasses:
            superclasses_str = ", ".join(class_obj.superclasses)
            label += f'<TR><TD ALIGN="LEFT" PORT="superclasses">extends {superclasses_str}</TD></TR>'
        
        # Add interfaces if any
        if class_obj.interfaces:
            interfaces_str = ", ".join(class_obj.interfaces)
            label += f'<TR><TD ALIGN="LEFT" PORT="interfaces">implements {interfaces_str}</TD></TR>'
        
        # Attribute section
        has_attributes = False
        attribute_rows = ""
        
        # Find all variables that are children of this class
        for variable in self.diagram.variables:
            if variable in class_obj.children:
                has_attributes = True
                var_signature = self._format_variable_signature(variable)
                attribute_rows += f'<TR><TD ALIGN="LEFT" PORT="{variable.id}">{var_signature}</TD></TR>'
        
        if has_attributes:
            label += f'<TR><TD BGCOLOR="#E5E9F0" COLSPAN="1"><I>Attributes</I></TD></TR>'
            label += attribute_rows
        
        # Method section
        has_methods = False
        method_rows = ""
        
        # Find all functions that are children of this class
        for function in self.diagram.functions:
            if function in class_obj.children:
                has_methods = True
                method_signature = self._format_function_signature(function)
                method_rows += f'<TR><TD ALIGN="LEFT" PORT="{function.id}">{method_signature}</TD></TR>'
        
        if has_methods:
            label += f'<TR><TD BGCOLOR="#E5E9F0" COLSPAN="1"><I>Methods</I></TD></TR>'
            label += method_rows
        
        # Close the table
        label += '</TABLE>>'
        
        # Set node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': self.element_colors[CodeElementType.CLASS],
            'shape': 'plain'
        }
        
        # Add the class to the graph
        self.graph.node(class_id, **node_attrs)
    
    def _render_interface(self, interface: Interface):
        """Render an interface as an HTML-like table."""
        interface_id = interface.id
        
        # Start building the HTML-like label for the interface
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Interface name row (header)
        header_color = self.header_colors[CodeElementType.INTERFACE]
        label += f'<TR><TD BGCOLOR="{header_color}" COLSPAN="1"><B>{interface.name}\\n«interface»</B></TD></TR>'
        
        # Add superinterfaces if any
        if interface.superinterfaces:
            superinterfaces_str = ", ".join(interface.superinterfaces)
            label += f'<TR><TD ALIGN="LEFT" PORT="superinterfaces">extends {superinterfaces_str}</TD></TR>'
        
        # Method section
        has_methods = False
        method_rows = ""
        
        # Find all functions that are children of this interface
        for function in self.diagram.functions:
            if function in interface.children:
                has_methods = True
                method_signature = self._format_function_signature(function)
                method_rows += f'<TR><TD ALIGN="LEFT" PORT="{function.id}">{method_signature}</TD></TR>'
        
        if has_methods:
            label += f'<TR><TD BGCOLOR="#E5E9F0" COLSPAN="1"><I>Methods</I></TD></TR>'
            label += method_rows
        
        # Close the table
        label += '</TABLE>>'
        
        # Set node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': self.element_colors[CodeElementType.INTERFACE],
            'shape': 'plain'
        }
        
        # Add the interface to the graph
        self.graph.node(interface_id, **node_attrs)
    
    def _render_enum(self, enum: Enum):
        """Render an enum as an HTML-like table."""
        enum_id = enum.id
        
        # Start building the HTML-like label for the enum
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Enum name row (header)
        header_color = self.header_colors[CodeElementType.ENUM]
        label += f'<TR><TD BGCOLOR="{header_color}" COLSPAN="1"><B>{enum.name}\\n«enum»</B></TD></TR>'
        
        # Add enum values
        if enum.values:
            for value in enum.values:
                label += f'<TR><TD ALIGN="LEFT">{value}</TD></TR>'
        
        # Close the table
        label += '</TABLE>>'
        
        # Set node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': self.element_colors[CodeElementType.ENUM],
            'shape': 'plain'
        }
        
        # Add the enum to the graph
        self.graph.node(enum_id, **node_attrs)
    
    def _render_module(self, module: Module):
        """Render a module as a subgraph with contained elements."""
        module_id = module.id
        cluster_name = f"cluster_{module_id}"
        
        # Create a subgraph for the module
        with self.graph.subgraph(name=cluster_name) as subgraph:
            # Set subgraph attributes
            subgraph.attr(
                label=module.name,
                style="filled",
                fillcolor=self.element_colors[CodeElementType.MODULE],
                color=self.header_colors[CodeElementType.MODULE],
                fontname="Arial-Bold"
            )
            
            # Add all children elements to the subgraph
            for child in module.children:
                subgraph.node(child.id)
    
    def _render_function(self, function: Function):
        """Render a standalone function."""
        function_id = function.id
        
        # Format the function signature
        signature = self._format_function_signature(function)
        
        # Start building the HTML-like label for the function
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Function name row (header)
        header_color = self.header_colors[CodeElementType.FUNCTION]
        label += f'<TR><TD BGCOLOR="{header_color}" COLSPAN="1"><B>{function.name}</B></TD></TR>'
        
        # Function signature row
        label += f'<TR><TD ALIGN="LEFT">{signature}</TD></TR>'
        
        # Close the table
        label += '</TABLE>>'
        
        # Set node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': self.element_colors[CodeElementType.FUNCTION],
            'shape': 'plain'
        }
        
        # Add the function to the graph
        self.graph.node(function_id, **node_attrs)
    
    def _render_variable(self, variable: Variable):
        """Render a standalone variable."""
        variable_id = variable.id
        
        # Format the variable signature
        signature = self._format_variable_signature(variable)
        
        # Start building the HTML-like label for the variable
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Variable name row (header)
        header_color = self.header_colors[CodeElementType.VARIABLE]
        label += f'<TR><TD BGCOLOR="{header_color}" COLSPAN="1"><B>{variable.name}</B></TD></TR>'
        
        # Variable signature row
        label += f'<TR><TD ALIGN="LEFT">{signature}</TD></TR>'
        
        # Close the table
        label += '</TABLE>>'
        
        # Set node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': self.element_colors[CodeElementType.VARIABLE],
            'shape': 'plain'
        }
        
        # Add the variable to the graph
        self.graph.node(variable_id, **node_attrs)
    
    def _render_relationship(self, relationship: CodeRelationship):
        """Render a relationship as an edge between elements."""
        source_id = relationship.source_id
        target_id = relationship.target_id
        
        # Get the source and target elements
        source_element = self.diagram.find_element_by_id(source_id)
        target_element = self.diagram.find_element_by_id(target_id)
        
        if not source_element or not target_element:
            # Skip if either element is not found
            return
        
        # Get the relationship style based on type
        edge_attrs = self.relationship_styles.get(relationship.relationship_type, {}).copy()
        
        # Add relationship name as a label if provided
        if relationship.name:
            edge_attrs['label'] = relationship.name
        
        # Add the edge to the graph
        self.graph.edge(source_id, target_id, **edge_attrs)
    
    def render(self, output_path: str, format: str = "svg", view: bool = False) -> str:
        """
        Render the code diagram to a file.
        
        Args:
            output_path: Path where to save the rendered diagram
            format: Output format (svg, png, pdf, etc.)
            view: Whether to open the rendered diagram
            
        Returns:
            Path to the rendered file
        """
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Setup the graph
        self._setup_graph()
        
        # First pass: Render all modules as subgraphs
        for module in self.diagram.modules:
            self._render_module(module)
        
        # Second pass: Render all classes
        for class_obj in self.diagram.classes:
            self._render_class(class_obj)
        
        # Third pass: Render all interfaces
        for interface in self.diagram.interfaces:
            self._render_interface(interface)
        
        # Fourth pass: Render all enums
        for enum in self.diagram.enums:
            self._render_enum(enum)
        
        # Fifth pass: Render standalone functions (not part of classes or interfaces)
        for function in self.diagram.functions:
            if not any(function in element.children for element in self.diagram.classes + self.diagram.interfaces):
                self._render_function(function)
        
        # Sixth pass: Render standalone variables (not part of classes)
        for variable in self.diagram.variables:
            if not any(variable in element.children for element in self.diagram.classes):
                self._render_variable(variable)
        
        # Final pass: Render all relationships
        for relationship in self.diagram.relationships:
            self._render_relationship(relationship)
        
        # Render the graph to file
        file_path = self.graph.render(
            filename=os.path.splitext(output_path)[0],
            format=format,
            cleanup=True,
            view=view
        )
        
        return file_path


def render_code_diagram(diagram: CodeDiagram, output_path: str, format: str = "svg", view: bool = False) -> str:
    """
    Convenience function to render a Code Diagram.
    
    Args:
        diagram: The Code Diagram to render
        output_path: Path where to save the rendered diagram
        format: Output format (svg, png, pdf, etc.)
        view: Whether to open the rendered diagram
        
    Returns:
        Path to the rendered file
    """
    renderer = CodeRenderer(diagram)
    return renderer.render(output_path, format, view) 