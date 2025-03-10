#!/usr/bin/env python3
"""
Data Flow Diagram Renderer module for PyDiagrams.

This module provides a renderer for Data Flow Diagrams (DFD) using Graphviz.
"""

import os
from typing import Dict, List, Optional, Tuple, Any
import graphviz

from pydiagrams.diagrams.entity.dfd import (
    DataFlowDiagram, 
    Process, 
    DataStore, 
    ExternalEntity,
    TrustBoundary,
    DataFlow,
    ElementType,
    FlowType
)


class DFDRenderer:
    """Renderer for Data Flow Diagrams using Graphviz."""
    
    def __init__(self, diagram: DataFlowDiagram):
        """
        Initialize the DFD renderer.
        
        Args:
            diagram: The Data Flow Diagram to render
        """
        self.diagram = diagram
        self.graph = None
        
        # Default styles for diagram elements
        self.styles = {
            ElementType.PROCESS: {
                'shape': 'ellipse',
                'style': 'filled',
                'fillcolor': '#ECECFC',
                'color': '#9370DB',
                'fontname': 'Arial',
                'fontsize': '10'
            },
            ElementType.DATA_STORE: {
                'shape': 'box',
                'style': 'filled',
                'fillcolor': '#E3F2FD',
                'color': '#1E88E5',
                'fontname': 'Arial',
                'fontsize': '10'
            },
            ElementType.EXTERNAL_ENTITY: {
                'shape': 'box',
                'style': 'filled,rounded',
                'fillcolor': '#F1F8E9',
                'color': '#7CB342',
                'fontname': 'Arial',
                'fontsize': '10'
            },
            ElementType.TRUST_BOUNDARY: {
                'shape': 'box',
                'style': 'dashed',
                'color': '#FF5722',
                'fontname': 'Arial',
                'fontsize': '10'
            }
        }
        
        # Default styles for data flow arrows
        self.flow_styles = {
            FlowType.DATA: {
                'color': '#2196F3',
                'style': 'solid',
                'fontname': 'Arial',
                'fontsize': '8'
            },
            FlowType.CONTROL: {
                'color': '#FF5722',
                'style': 'dashed',
                'fontname': 'Arial',
                'fontsize': '8'
            },
            FlowType.EVENT: {
                'color': '#9C27B0',
                'style': 'dotted',
                'fontname': 'Arial',
                'fontsize': '8'
            },
            FlowType.RESPONSE: {
                'color': '#4CAF50',
                'style': 'solid',
                'fontname': 'Arial',
                'fontsize': '8'
            },
            FlowType.BIDIRECTIONAL: {
                'color': '#795548',
                'style': 'solid',
                'dir': 'both',
                'fontname': 'Arial',
                'fontsize': '8'
            }
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
            splines='polyline',
            nodesep='0.8',
            ranksep='1.0',
            fontname='Arial',
            fontsize='12',
            dpi='300',
            compound='true'  # For boundary boxes
        )
        
        # Set default node and edge attributes
        self.graph.attr('node', shape='box', style='filled', fillcolor='white',
                      fontname='Arial', fontsize='10')
        self.graph.attr('edge', color='gray', fontname='Arial', fontsize='8')

    def _format_label(self, element, include_number=True, include_description=False):
        """Format the label for a diagram element."""
        label = element.name
        
        # Add numbering if available
        if include_number:
            if hasattr(element, 'process_number') and element.process_number:
                label = f"{element.process_number}: {label}"
            elif hasattr(element, 'store_number') and element.store_number:
                label = f"{element.store_number}: {label}"
            elif hasattr(element, 'entity_number') and element.entity_number:
                label = f"{element.entity_number}: {label}"
        
        # Add description if requested
        if include_description and element.description:
            label = f"{label}\\n{element.description}"
        
        return label

    def _render_processes(self):
        """Render all processes in the diagram."""
        for process in self.diagram.processes:
            node_id = process.id
            label = self._format_label(process)
            
            # Apply process-specific styles
            attrs = self.styles[ElementType.PROCESS].copy()
            
            # Add the node to the graph
            self.graph.node(node_id, label, **attrs)

    def _render_data_stores(self):
        """Render all data stores in the diagram."""
        for data_store in self.diagram.data_stores:
            node_id = data_store.id
            # Format data store labels with "DS" prefix if no store number provided
            if not data_store.store_number:
                label = f"DS: {data_store.name}"
            else:
                label = self._format_label(data_store)
            
            # Apply data store-specific styles
            attrs = self.styles[ElementType.DATA_STORE].copy()
            
            # Add the node to the graph
            self.graph.node(node_id, label, **attrs)

    def _render_external_entities(self):
        """Render all external entities in the diagram."""
        for entity in self.diagram.external_entities:
            node_id = entity.id
            label = self._format_label(entity)
            
            # Apply external entity-specific styles
            attrs = self.styles[ElementType.EXTERNAL_ENTITY].copy()
            
            # Add the node to the graph
            self.graph.node(node_id, label, **attrs)

    def _render_trust_boundaries(self):
        """Render all trust boundaries in the diagram."""
        for boundary in self.diagram.trust_boundaries:
            # Create a subgraph for the trust boundary
            with self.graph.subgraph(name=f"cluster_{boundary.id}") as subgraph:
                # Set attributes for the boundary
                subgraph.attr(
                    label=boundary.name,
                    **self.styles[ElementType.TRUST_BOUNDARY]
                )
                
                # Add all elements within this boundary to the subgraph
                for element_id in boundary.element_ids:
                    # Just add the element ID to the subgraph
                    # The actual nodes are already created
                    subgraph.node(element_id)

    def _render_data_flows(self):
        """Render all data flows in the diagram."""
        for flow in self.diagram.data_flows:
            source_id = flow.source_id
            target_id = flow.target_id
            
            # Format the label with data items if present
            if flow.data_items:
                data_items_str = ", ".join(flow.data_items)
                label = f"{flow.name}\\n[{data_items_str}]" if flow.name else f"[{data_items_str}]"
            else:
                label = flow.name
            
            # Apply flow-specific styles
            attrs = self.flow_styles[flow.flow_type].copy()
            
            # Add the edge to the graph
            self.graph.edge(source_id, target_id, label=label, **attrs)

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
        
        # Render all diagram elements
        self._render_processes()
        self._render_data_stores()
        self._render_external_entities()
        self._render_trust_boundaries()
        self._render_data_flows()
        
        # Render the graph to file
        file_path = self.graph.render(
            filename=os.path.splitext(output_path)[0],
            format=format,
            cleanup=True,
            view=view
        )
        
        return file_path


def render_dfd(diagram: DataFlowDiagram, output_path: str, format: str = "svg", view: bool = False) -> str:
    """
    Convenience function to render a Data Flow Diagram.
    
    Args:
        diagram: The Data Flow Diagram to render
        output_path: Path where to save the rendered diagram
        format: Output format (svg, png, pdf, etc.)
        view: Whether to open the rendered diagram
        
    Returns:
        Path to the rendered file
    """
    renderer = DFDRenderer(diagram)
    return renderer.render(output_path, format, view) 