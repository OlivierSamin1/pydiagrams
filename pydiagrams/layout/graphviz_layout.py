"""
Layout management using Graphviz.

This module provides layout algorithms based on Graphviz.
"""

import os
import tempfile
from typing import Dict, Any, Tuple, List, Optional, Union
import networkx as nx
import pygraphviz as pgv
from enum import Enum


class LayoutEngine(Enum):
    """Available layout engines from Graphviz."""
    DOT = "dot"       # Hierarchical layout (default)
    NEATO = "neato"   # Spring model layout
    FDP = "fdp"       # Spring model layout with force-directed placement
    SFDP = "sfdp"     # Multiscale version of fdp for large graphs
    TWOPI = "twopi"   # Radial layout
    CIRCO = "circo"   # Circular layout


class NodeShape(Enum):
    """Common node shapes for different diagram elements."""
    BOX = "box"
    ELLIPSE = "ellipse"
    CIRCLE = "circle"
    DIAMOND = "diamond"
    RECTANGLE = "rectangle"
    ROUNDED_BOX = "box,style=rounded"
    DOUBLE_CIRCLE = "doublecircle"
    POINT = "point"
    NONE = "none"


class GraphvizLayoutManager:
    """
    Layout manager using Graphviz algorithms.
    
    This class handles the conversion between PyDiagrams data structures and Graphviz
    graphs, applies layout algorithms, and returns the calculated positions.
    """
    
    def __init__(self, engine: LayoutEngine = LayoutEngine.DOT):
        """
        Initialize the Graphviz layout manager.
        
        Args:
            engine: The Graphviz layout engine to use.
        """
        self.engine = engine
        self.node_positions = {}
        self.edge_points = {}
        
    def _create_graphviz_graph(self, diagram_data: Dict[str, Any]) -> pgv.AGraph:
        """
        Convert diagram data to a Pygraphviz graph.
        
        Args:
            diagram_data: The diagram data as a dictionary.
            
        Returns:
            A Pygraphviz graph.
        """
        # Create a new graph
        graph = pgv.AGraph(directed=True, strict=True)
        graph.graph_attr.update(
            splines='true',  # Use splines for edges
            overlap='false',  # Avoid node overlap
            rankdir='TB',    # Top to bottom layout by default
            concentrate='true',  # Concentrate edges
            nodesep='0.5',   # Minimum space between nodes
            ranksep='0.75',  # Minimum space between ranks
        )
        
        # Process elements based on diagram type
        diagram_type = diagram_data.get("type", "unknown")
        
        if diagram_type == "state_diagram":
            self._process_state_diagram(graph, diagram_data)
        elif diagram_type == "class_diagram":
            self._process_class_diagram(graph, diagram_data)
        elif diagram_type == "sequence_diagram":
            self._process_sequence_diagram(graph, diagram_data)
        elif diagram_type == "activity_diagram":
            self._process_activity_diagram(graph, diagram_data)
        elif diagram_type == "usecase_diagram":
            self._process_usecase_diagram(graph, diagram_data)
        else:
            # Generic processing
            self._process_generic_diagram(graph, diagram_data)
        
        return graph
    
    def _process_generic_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process a generic diagram into a Graphviz graph.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Add all elements as nodes
        for element in diagram_data.get("elements", []):
            element_id = element.get("id")
            element_name = element.get("name", "")
            element_type = element.get("type", "unknown")
            
            # Create a node
            graph.add_node(element_id, 
                          label=element_name, 
                          shape="box")
        
        # Add all relationships as edges
        for relationship in diagram_data.get("relationships", []):
            source_id = relationship.get("source_id")
            target_id = relationship.get("target_id")
            rel_type = relationship.get("type", "unknown")
            label = relationship.get("label", "")
            
            # Create an edge
            graph.add_edge(source_id, target_id, label=label)
    
    def _process_state_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process a state diagram into a Graphviz graph.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Configure graph for state diagrams
        graph.graph_attr.update(
            rankdir='TB',    # Top to bottom layout
            ranksep='0.75',  # Minimum space between ranks
            margin='0.2',    # Margin around the graph
        )
        
        # Add all states as nodes
        for element in diagram_data.get("elements", []):
            if element.get("type") == "state":
                element_id = element.get("id")
                element_name = element.get("name", "")
                state_type = element.get("state_type", "simple")
                
                # Determine shape based on state type
                shape = "box"
                style = "rounded"
                width = 1.5
                height = 1.0
                
                if state_type == "initial":
                    shape = "circle"
                    style = "filled"
                    width = 0.3
                    height = 0.3
                    element_name = ""  # No label for initial state
                elif state_type == "final":
                    shape = "doublecircle"
                    width = 0.4
                    height = 0.4
                    element_name = ""  # No label for final state
                elif state_type == "choice":
                    shape = "diamond"
                    width = 0.4
                    height = 0.4
                    element_name = ""  # No label for choice state
                elif state_type == "junction":
                    shape = "circle"
                    style = "filled"
                    width = 0.2
                    height = 0.2
                    element_name = ""  # No label for junction state
                elif state_type in ["shallow_history", "deep_history"]:
                    shape = "circle"
                    element_name = "H" if state_type == "shallow_history" else "H*"
                    width = 0.3
                    height = 0.3
                elif state_type == "terminate":
                    shape = "circle"
                    style = "filled,dashed"
                    width = 0.3
                    height = 0.3
                    element_name = "X"
                elif state_type == "composite":
                    shape = "box"
                    style = "rounded"
                    width = 2.0
                    height = 2.0
                
                # Add node with appropriate shape and style
                graph.add_node(element_id, 
                              label=element_name,
                              shape=shape,
                              style=style,
                              width=width,
                              height=height)
                
                # Handle composite states - add invisible edges to ensure
                # substates are contained within the composite state
                if state_type == "composite":
                    substates = element.get("substates", [])
                    for substate in substates:
                        substate_id = substate.get("id")
                        # Add an invisible edge to the substate
                        graph.add_edge(element_id, substate_id, style="invis")
        
        # Add all transitions as edges
        for relationship in diagram_data.get("relationships", []):
            if relationship.get("type") == "transition":
                source_id = relationship.get("source_id")
                target_id = relationship.get("target_id")
                label = relationship.get("label", "")
                
                # Create an edge
                graph.add_edge(source_id, target_id, label=label)
    
    def _process_class_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process a class diagram into a Graphviz graph.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Configure graph for class diagrams
        graph.graph_attr.update(
            rankdir='TB',    # Top to bottom layout
            ranksep='1.0',   # More space between ranks for class diagrams
            margin='0.2',    # Margin around the graph
        )
        
        # Add all classes as nodes
        for element in diagram_data.get("elements", []):
            element_id = element.get("id")
            element_name = element.get("name", "")
            element_type = element.get("type", "unknown")
            
            if element_type == "class":
                # Create a label that includes attributes and methods
                attrs = element.get("attributes", [])
                methods = element.get("methods", [])
                
                # Format label with HTML-like label
                label = f"<{{<B>{element_name}</B>}}|"
                
                # Add attributes section
                label += "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
                for attr in attrs:
                    attr_name = attr.get("name", "")
                    attr_type = attr.get("type", "")
                    attr_visibility = attr.get("visibility", "")
                    vis_symbol = {"public": "+", "private": "-", "protected": "#", "package": "~"}.get(attr_visibility, "")
                    label += f"<TR><TD ALIGN=\"LEFT\">{vis_symbol} {attr_name}: {attr_type}</TD></TR>"
                label += "</TABLE>|"
                
                # Add methods section
                label += "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
                for method in methods:
                    method_name = method.get("name", "")
                    method_return_type = method.get("return_type", "")
                    method_visibility = method.get("visibility", "")
                    vis_symbol = {"public": "+", "private": "-", "protected": "#", "package": "~"}.get(method_visibility, "")
                    label += f"<TR><TD ALIGN=\"LEFT\">{vis_symbol} {method_name}(): {method_return_type}</TD></TR>"
                label += "</TABLE>}>"
                
                # Add class node with the HTML label
                graph.add_node(element_id, 
                              label=label,
                              shape="record",
                              style="filled",
                              fillcolor="white",
                              fontname="Helvetica")
            
            elif element_type == "interface":
                # Similar to class, but with stereotype and only methods
                methods = element.get("methods", [])
                
                # Format label with HTML-like label
                label = f"<{{<B>&lt;&lt;interface&gt;&gt;</B><BR/><B>{element_name}</B>}}|"
                
                # Add methods section
                label += "<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">"
                for method in methods:
                    method_name = method.get("name", "")
                    method_return_type = method.get("return_type", "")
                    label += f"<TR><TD ALIGN=\"LEFT\">+ {method_name}(): {method_return_type}</TD></TR>"
                label += "</TABLE>}>"
                
                # Add interface node with the HTML label
                graph.add_node(element_id, 
                              label=label,
                              shape="record",
                              style="filled",
                              fillcolor="white",
                              fontname="Helvetica")
        
        # Add all relationships as edges
        for relationship in diagram_data.get("relationships", []):
            source_id = relationship.get("source_id")
            target_id = relationship.get("target_id")
            rel_type = relationship.get("type", "unknown")
            
            # Set edge attributes based on relationship type
            edge_attrs = {
                "label": relationship.get("label", ""),
                "fontsize": 10
            }
            
            if rel_type == "inheritance":
                edge_attrs["arrowhead"] = "empty"
                edge_attrs["style"] = "solid"
            elif rel_type == "implementation":
                edge_attrs["arrowhead"] = "empty"
                edge_attrs["style"] = "dashed"
            elif rel_type == "association":
                edge_attrs["arrowhead"] = "vee"
                edge_attrs["style"] = "solid"
            elif rel_type == "aggregation":
                edge_attrs["arrowhead"] = "odiamond"
                edge_attrs["style"] = "solid"
            elif rel_type == "composition":
                edge_attrs["arrowhead"] = "diamond"
                edge_attrs["style"] = "solid"
            elif rel_type == "dependency":
                edge_attrs["arrowhead"] = "vee"
                edge_attrs["style"] = "dashed"
            
            # Create an edge with appropriate attributes
            graph.add_edge(source_id, target_id, **edge_attrs)
    
    def _process_activity_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process an activity diagram into a Graphviz graph.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Configure graph for activity diagrams
        graph.graph_attr.update(
            rankdir='TB',    # Top to bottom layout
            ranksep='0.75',  # Minimum space between ranks
            margin='0.2',    # Margin around the graph
        )
        
        # Add all nodes
        for element in diagram_data.get("elements", []):
            if element.get("type") == "activity_node":
                node_id = element.get("id")
                node_name = element.get("name", "")
                node_type = element.get("node_type", "action")
                
                # Determine shape based on node type
                shape = "box"
                style = "rounded"
                width = 1.5
                height = 1.0
                
                if node_type == "initial":
                    shape = "circle"
                    style = "filled"
                    width = 0.3
                    height = 0.3
                    node_name = ""  # No label for initial node
                elif node_type == "activity_final":
                    shape = "doublecircle"
                    width = 0.4
                    height = 0.4
                    node_name = ""  # No label for final node
                elif node_type == "flow_final":
                    shape = "circle"
                    style = "filled,dashed"
                    width = 0.3
                    height = 0.3
                    node_name = "X"
                elif node_type == "decision":
                    shape = "diamond"
                    width = 0.7
                    height = 0.7
                elif node_type == "merge":
                    shape = "diamond"
                    width = 0.7
                    height = 0.7
                elif node_type == "fork":
                    shape = "rect"
                    width = 1.0
                    height = 0.1
                    node_name = ""  # No label for fork node
                elif node_type == "join":
                    shape = "rect"
                    width = 1.0
                    height = 0.1
                    node_name = ""  # No label for join node
                elif node_type == "object":
                    shape = "box"
                    style = "rounded,dashed"
                
                # Add node with appropriate shape and style
                graph.add_node(node_id, 
                              label=node_name,
                              shape=shape,
                              style=style,
                              width=width,
                              height=height)
        
        # Add all edges
        for relationship in diagram_data.get("relationships", []):
            if relationship.get("type") == "activity_edge":
                source_id = relationship.get("source_id")
                target_id = relationship.get("target_id")
                guard = relationship.get("guard", "")
                
                # Create an edge
                graph.add_edge(source_id, target_id, label=guard)
    
    def _process_usecase_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process a use case diagram into a Graphviz graph.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Configure graph for use case diagrams
        graph.graph_attr.update(
            rankdir='LR',    # Left to right layout
            ranksep='1.0',   # More space between ranks
            margin='0.2',    # Margin around the graph
        )
        
        # Create invisible nodes to group elements
        graph.add_node("actors_group", shape="point", style="invis")
        graph.add_node("system_group", shape="point", style="invis")
        
        # Process all elements
        for element in diagram_data.get("elements", []):
            element_id = element.get("id")
            element_name = element.get("name", "")
            element_type = element.get("type", "unknown")
            
            if element_type == "actor":
                # Add actor node
                graph.add_node(element_id, 
                              label=element_name,
                              shape="custom",
                              style="bold",
                              fixedsize="true",
                              width=0.5,
                              height=1.0)
                
                # Add edge to actor group for layout control
                graph.add_edge("actors_group", element_id, style="invis")
                
            elif element_type == "usecase":
                # Add use case node
                graph.add_node(element_id, 
                              label=element_name,
                              shape="ellipse",
                              style="filled",
                              fillcolor="white",
                              fontname="Helvetica")
                
                # Add edge to system group for layout control
                graph.add_edge("system_group", element_id, style="invis")
                
            elif element_type == "system":
                # System boundary is handled as a subgraph
                system_id = element.get("id")
                system_name = element.get("name", "")
                use_cases = element.get("use_cases", [])
                
                # Create a subgraph for the system
                subgraph = graph.add_subgraph(
                    nbunch=use_cases,
                    name=f"cluster_{system_id}",
                    label=system_name,
                    style="dashed",
                    color="gray60"
                )
        
        # Add all relationships
        for relationship in diagram_data.get("relationships", []):
            source_id = relationship.get("source_id")
            target_id = relationship.get("target_id")
            rel_type = relationship.get("relationship_type", "association")
            label = relationship.get("label", "")
            
            # Set edge attributes based on relationship type
            edge_attrs = {
                "label": label,
                "fontsize": 10
            }
            
            if rel_type == "association":
                edge_attrs["style"] = "solid"
            elif rel_type == "include":
                edge_attrs["style"] = "dashed"
                if not label:
                    edge_attrs["label"] = "<<include>>"
            elif rel_type == "extend":
                edge_attrs["style"] = "dashed"
                if not label:
                    edge_attrs["label"] = "<<extend>>"
            elif rel_type == "generalization":
                edge_attrs["arrowhead"] = "empty"
                edge_attrs["style"] = "solid"
            
            # Create an edge with appropriate attributes
            graph.add_edge(source_id, target_id, **edge_attrs)
    
    def _process_sequence_diagram(self, graph: pgv.AGraph, diagram_data: Dict[str, Any]) -> None:
        """
        Process a sequence diagram into a Graphviz graph.
        
        Note: Sequence diagrams have a very specific layout not well-suited for
        standard graph layout algorithms. This method provides a simplified representation.
        
        Args:
            graph: The Pygraphviz graph to populate.
            diagram_data: The diagram data as a dictionary.
        """
        # Configure graph for sequence diagrams
        graph.graph_attr.update(
            rankdir='LR',    # Left to right for lifelines
            ranksep='1.0',   # More space between ranks
            margin='0.2',    # Margin around the graph
        )
        
        # Process all elements
        lifelines = []
        for element in diagram_data.get("elements", []):
            if element.get("type") == "lifeline":
                lifeline_id = element.get("id")
                lifeline_name = element.get("name", "")
                
                # Add lifeline node
                graph.add_node(lifeline_id, 
                              label=lifeline_name,
                              shape="box",
                              style="filled",
                              fillcolor="white",
                              fontname="Helvetica")
                
                lifelines.append(lifeline_id)
        
        # Add edges between lifelines to ensure proper horizontal alignment
        for i in range(len(lifelines) - 1):
            graph.add_edge(lifelines[i], lifelines[i+1], style="invis")
        
        # Note: Messages would be processed here, but they don't map well to the
        # standard graph layout model. The sequence diagram renderer needs to handle
        # these specially.
    
    def apply_layout(self, diagram_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply layout algorithms to a diagram.
        
        Args:
            diagram_data: The diagram data as a dictionary.
            
        Returns:
            The diagram data with added layout information.
        """
        # Create a Graphviz graph from the diagram data
        graph = self._create_graphviz_graph(diagram_data)
        
        # Apply the layout
        graph.layout(prog=self.engine.value)
        
        # Extract positions
        self.node_positions = {}
        self.edge_points = {}
        
        # Store node positions
        for node in graph.nodes():
            node_id = node.get_name()
            pos = node.attr.get('pos', '0,0').split(',')
            try:
                x = float(pos[0])
                y = float(pos[1].split('!')[0])  # Handle special position indicators
                self.node_positions[node_id] = (x, y)
            except (ValueError, IndexError):
                self.node_positions[node_id] = (0, 0)
        
        # Store edge control points
        for edge in graph.edges():
            source_id = edge[0]
            target_id = edge[1]
            edge_key = (source_id, target_id)
            
            # Get the pos attribute which contains the spline points
            pos = edge.attr.get('pos', None)
            if pos:
                # Parse the spline points
                points = []
                segments = pos.split(' ')
                for segment in segments:
                    if segment.startswith('e,') or segment.startswith('s,'):
                        # These are control point indicators
                        continue
                    
                    try:
                        coords = segment.split(',')
                        x = float(coords[0])
                        y = float(coords[1])
                        points.append((x, y))
                    except (ValueError, IndexError):
                        continue
                
                if points:
                    self.edge_points[edge_key] = points
        
        # Update diagram data with layout information
        for element in diagram_data.get("elements", []):
            element_id = element.get("id")
            if element_id in self.node_positions:
                element["position"] = {
                    "x": self.node_positions[element_id][0],
                    "y": self.node_positions[element_id][1]
                }
        
        for relationship in diagram_data.get("relationships", []):
            source_id = relationship.get("source_id")
            target_id = relationship.get("target_id")
            edge_key = (source_id, target_id)
            if edge_key in self.edge_points:
                relationship["control_points"] = [
                    {"x": p[0], "y": p[1]} for p in self.edge_points[edge_key]
                ]
        
        return diagram_data
    
    def get_node_position(self, node_id: str) -> Tuple[float, float]:
        """
        Get the position of a node.
        
        Args:
            node_id: The ID of the node.
            
        Returns:
            The (x, y) position of the node.
        """
        return self.node_positions.get(node_id, (0, 0))
    
    def get_edge_points(self, source_id: str, target_id: str) -> List[Tuple[float, float]]:
        """
        Get the control points of an edge.
        
        Args:
            source_id: The ID of the source node.
            target_id: The ID of the target node.
            
        Returns:
            A list of (x, y) control points for the edge.
        """
        return self.edge_points.get((source_id, target_id), []) 