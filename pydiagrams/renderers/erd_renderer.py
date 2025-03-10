#!/usr/bin/env python3
"""
Entity Relationship Diagram Renderer module for PyDiagrams.

This module provides a renderer for Entity Relationship Diagrams (ERD) using Graphviz.
"""

import os
from typing import Dict, List, Optional, Tuple, Any
import graphviz

from pydiagrams.diagrams.entity.erd import (
    EntityRelationshipDiagram,
    Entity,
    Attribute,
    EntityRelationship,
    AttributeType,
    RelationshipType,
    Cardinality
)


class ERDRenderer:
    """Renderer for Entity Relationship Diagrams using Graphviz."""
    
    def __init__(self, diagram: EntityRelationshipDiagram):
        """
        Initialize the ERD renderer.
        
        Args:
            diagram: The Entity Relationship Diagram to render
        """
        self.diagram = diagram
        self.graph = None
        
        # Mapping from RelationshipType to edge style
        self.relationship_styles = {
            RelationshipType.ONE_TO_ONE: {
                'dir': 'both',
                'arrowtail': 'tee',
                'arrowhead': 'tee',
                'style': 'solid',
                'color': '#1E88E5'
            },
            RelationshipType.ONE_TO_MANY: {
                'dir': 'both',
                'arrowtail': 'tee',
                'arrowhead': 'crow',
                'style': 'solid',
                'color': '#43A047'
            },
            RelationshipType.MANY_TO_ONE: {
                'dir': 'both',
                'arrowtail': 'crow',
                'arrowhead': 'tee',
                'style': 'solid',
                'color': '#FB8C00'
            },
            RelationshipType.MANY_TO_MANY: {
                'dir': 'both',
                'arrowtail': 'crow',
                'arrowhead': 'crow',
                'style': 'solid',
                'color': '#F44336'
            },
            RelationshipType.INHERITANCE: {
                'dir': 'back',
                'arrowtail': 'empty',
                'style': 'solid',
                'color': '#9C27B0'
            },
            RelationshipType.AGGREGATION: {
                'dir': 'back',
                'arrowtail': 'odiamond',
                'style': 'solid',
                'color': '#795548'
            },
            RelationshipType.COMPOSITION: {
                'dir': 'back',
                'arrowtail': 'diamond',
                'style': 'solid',
                'color': '#607D8B'
            }
        }
        
        # Mapping from Cardinality to label text
        self.cardinality_labels = {
            Cardinality.ZERO_OR_ONE: '0..1',
            Cardinality.EXACTLY_ONE: '1',
            Cardinality.ZERO_OR_MANY: '0..*',
            Cardinality.ONE_OR_MANY: '1..*',
            Cardinality.CUSTOM: 'custom'  # This will be replaced with custom text
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
            rankdir='LR',
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

    def _format_attribute_label(self, attr: Attribute) -> str:
        """Format an attribute for display in the entity table."""
        # Start with icons for primary/foreign keys
        prefix = ""
        if attr.is_primary_key and attr.is_foreign_key:
            prefix = "🔑🔗 "
        elif attr.is_primary_key:
            prefix = "🔑 "
        elif attr.is_foreign_key:
            prefix = "🔗 "
        
        # Add attribute name
        label = f"{prefix}{attr.name}"
        
        # Add data type if provided
        if attr.data_type:
            data_type = attr.data_type
            
            # Add length/precision/scale if applicable
            if attr.length is not None:
                data_type = f"{data_type}({attr.length})"
            elif attr.precision is not None:
                if attr.scale is not None:
                    data_type = f"{data_type}({attr.precision},{attr.scale})"
                else:
                    data_type = f"{data_type}({attr.precision})"
            
            label = f"{label} : {data_type}"
        
        # Add nullability indicator
        if not attr.is_nullable:
            label = f"{label} NOT NULL"
        
        # Add unique constraint
        if attr.is_unique and not attr.is_primary_key:  # Primary keys are already unique
            label = f"{label} UNIQUE"
        
        return label

    def _render_entity(self, entity: Entity):
        """Render an entity as an HTML-like table."""
        entity_id = entity.id
        
        # Start building the HTML-like label for the entity
        label = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Entity name header (with different background for weak entities)
        bg_color = "#ECECFC" if not entity.is_weak else "#FFF9C4"
        
        # Entity name row (header)
        label += f'<TR><TD BGCOLOR="{bg_color}" COLSPAN="1"><B>{entity.name}</B></TD></TR>'
        
        # Attribute rows
        for attr in entity.attributes:
            attr_label = self._format_attribute_label(attr)
            label += f'<TR><TD ALIGN="LEFT" PORT="{attr.id}">{attr_label}</TD></TR>'
        
        # Close the table
        label += '</TABLE>>'
        
        # Set additional node attributes
        node_attrs = {
            'label': label,
            'style': 'filled',
            'fillcolor': 'white',
            'color': '#333333' if not entity.is_weak else '#FFB300'
        }
        
        # Add dashed border for weak entities
        if entity.is_weak:
            node_attrs['style'] = 'filled,dashed'
        
        # Add the entity to the graph
        self.graph.node(entity_id, **node_attrs)

    def _get_cardinality_label(self, rel: EntityRelationship, end: str) -> str:
        """Get the cardinality label for a relationship end."""
        if end == 'source':
            cardinality = rel.source_cardinality
            custom_cardinality = rel.custom_source_cardinality
        else:  # target
            cardinality = rel.target_cardinality
            custom_cardinality = rel.custom_target_cardinality
        
        if cardinality == Cardinality.CUSTOM and custom_cardinality:
            return custom_cardinality
        else:
            return self.cardinality_labels.get(cardinality, '')

    def _render_relationship(self, rel: EntityRelationship):
        """Render a relationship as an edge between entities."""
        source_id = rel.source_entity_id
        target_id = rel.target_entity_id
        
        # Get the source and target entities
        source_entity = self.diagram.find_entity_by_id(source_id)
        target_entity = self.diagram.find_entity_by_id(target_id)
        
        if not source_entity or not target_entity:
            # Skip if either entity is not found
            return
        
        # Get the relationship style based on type
        edge_attrs = self.relationship_styles.get(rel.relationship_type, {}).copy()
        
        # Add relationship name as a label if provided
        if rel.name:
            edge_attrs['label'] = rel.name
        
        # Add cardinality labels
        source_cardinality = self._get_cardinality_label(rel, 'source')
        target_cardinality = self._get_cardinality_label(rel, 'target')
        
        if source_cardinality:
            edge_attrs['taillabel'] = source_cardinality
        
        if target_cardinality:
            edge_attrs['headlabel'] = target_cardinality
        
        # Add role names if provided
        if rel.source_role:
            edge_attrs['taillabel'] = f"{edge_attrs.get('taillabel', '')} ({rel.source_role})"
        
        if rel.target_role:
            edge_attrs['headlabel'] = f"{edge_attrs.get('headlabel', '')} ({rel.target_role})"
        
        # Add identifying relationship style
        if rel.identifying:
            edge_attrs['style'] = f"{edge_attrs.get('style', 'solid')},bold"
        
        # Add the edge to the graph
        self.graph.edge(source_id, target_id, **edge_attrs)

    def render(self, output_path: str, format: str = "svg", view: bool = False) -> str:
        """
        Render the diagram to a file.
        
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
        
        # Render all entities
        for entity in self.diagram.entities:
            self._render_entity(entity)
        
        # Render all relationships
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


def render_erd(diagram: EntityRelationshipDiagram, output_path: str, format: str = "svg", view: bool = False) -> str:
    """
    Convenience function to render an Entity Relationship Diagram.
    
    Args:
        diagram: The Entity Relationship Diagram to render
        output_path: Path where to save the rendered diagram
        format: Output format (svg, png, pdf, etc.)
        view: Whether to open the rendered diagram
        
    Returns:
        Path to the rendered file
    """
    renderer = ERDRenderer(diagram)
    return renderer.render(output_path, format, view) 