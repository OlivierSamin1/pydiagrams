#!/usr/bin/env python3
"""
Renderer for UML Component Diagrams.

This module provides specialized rendering for UML Component Diagrams
with support for components, interfaces, ports, and connectors.
"""

import math
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Any, Union

from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Line, Rect, Circle, Polygon
from svgwrite.text import Text
from svgwrite.path import Path

from pydiagrams.diagrams.uml.component_diagram import (
    ComponentDiagram, Component, Interface, Port, 
    Connector, Artifact, InterfaceType, ConnectorType, ComponentType
)
from pydiagrams.renderers.svg_renderer import SVGRenderer


@dataclass
class ComponentDiagramRenderer(SVGRenderer):
    """
    Specialized renderer for UML Component Diagrams.
    
    This renderer visualizes components, interfaces, ports, and connectors
    with their relationships in a UML Component Diagram.
    """
    # Default dimensions of the diagram
    width: int = 800
    height: int = 600
    unit: str = "px"
    
    # Styling properties
    component_width: int = 160
    component_height: int = 100
    component_spacing: int = 40
    interface_radius: int = 10
    port_size: int = 15
    text_margin: int = 5
    line_stroke_width: int = 2
    arrow_size: int = 10
    
    # Colors
    component_fill: str = "#E0E8FF"
    component_stroke: str = "#2F4F4F"
    interface_fill: str = "#FFFFFF"
    interface_stroke: str = "#000000"
    port_fill: str = "#D3D3D3"
    port_stroke: str = "#000000"
    artifact_fill: str = "#F8F8FF"
    artifact_stroke: str = "#696969"
    text_color: str = "#000000"
    connector_color: str = "#000000"
    
    # Component symbols
    component_symbol_width: int = 30
    component_symbol_height: int = 20
    component_symbol_offset: int = 10
    
    def render(self, 
               diagram: ComponentDiagram, 
               output_path: str, 
               **kwargs) -> str:
        """
        Render a UML Component Diagram to an SVG file.
        
        Args:
            diagram: The ComponentDiagram object to render
            output_path: The file path to save the rendered diagram
            **kwargs: Additional rendering options
            
        Returns:
            The path to the rendered SVG file
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create SVG Drawing
        self.drawing = Drawing(
            output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}")
        )
        
        # Add definitions
        self._add_defs()
        
        # Create groups for different element types for layering
        component_group = self.drawing.add(Group(id="components"))
        connector_group = self.drawing.add(Group(id="connectors"))
        interface_group = self.drawing.add(Group(id="interfaces"))
        port_group = self.drawing.add(Group(id="ports"))
        artifact_group = self.drawing.add(Group(id="artifacts"))
        
        # Calculate positions for components
        positions = self._calculate_positions(diagram)
        
        # Draw components
        component_positions = {}
        for component in diagram.components:
            pos = positions.get(component.id, (50, 50))
            component_positions[component.id] = pos
            self._render_component(component_group, component, pos)
        
        # Draw interfaces
        interface_positions = {}
        for component in diagram.components:
            for interface in component.provided_interfaces:
                pos = self._calculate_interface_position(
                    component_positions[component.id], 
                    component,
                    interface,
                    is_provided=True
                )
                interface_positions[interface.id] = pos
                self._render_interface(
                    interface_group, 
                    interface, 
                    pos,
                    is_provided=True
                )
            
            for interface in component.required_interfaces:
                pos = self._calculate_interface_position(
                    component_positions[component.id], 
                    component,
                    interface,
                    is_provided=False
                )
                interface_positions[interface.id] = pos
                self._render_interface(
                    interface_group, 
                    interface, 
                    pos,
                    is_provided=False
                )
        
        # Draw ports
        # (Simplified - in a full implementation, ports would be positioned
        # based on component boundaries)
        
        # Draw connectors
        for connector in diagram.connectors:
            source_pos = None
            target_pos = None
            
            # Find positions of source and target
            if connector.source_id in component_positions:
                source_pos = component_positions[connector.source_id]
            elif connector.source_id in interface_positions:
                source_pos = interface_positions[connector.source_id]
                
            if connector.target_id in component_positions:
                target_pos = component_positions[connector.target_id]
            elif connector.target_id in interface_positions:
                target_pos = interface_positions[connector.target_id]
            
            if source_pos and target_pos:
                self._render_connector(
                    connector_group, 
                    connector,
                    source_pos,
                    target_pos
                )
        
        # Draw artifacts
        y_offset = 50
        for artifact in diagram.artifacts:
            pos = (self.width - self.component_width - 50, y_offset)
            self._render_artifact(artifact_group, artifact, pos)
            y_offset += self.component_height + 20
        
        # Save the SVG
        self.drawing.save()
        return output_path
    
    def _add_defs(self) -> None:
        """Add definitions to the SVG (markers, patterns, etc.)."""
        # Add arrow marker for dependency
        marker = self.drawing.marker(
            insert=(10, 5), 
            size=(10, 10), 
            orient="auto", 
            id="arrow"
        )
        marker.add(self.drawing.path("M0,0 L10,5 L0,10 L3,5 Z", fill="#000000"))
        self.drawing.defs.add(marker)
        
        # Add hollow arrow marker for realization
        marker = self.drawing.marker(
            insert=(10, 5), 
            size=(10, 10), 
            orient="auto", 
            id="hollow-arrow"
        )
        marker.add(self.drawing.path(
            "M0,0 L10,5 L0,10 L3,5 Z", 
            fill="#FFFFFF", 
            stroke="#000000", 
            stroke_width=1
        ))
        self.drawing.defs.add(marker)
    
    def _calculate_positions(self, diagram: ComponentDiagram) -> Dict[str, Tuple[int, int]]:
        """
        Calculate positions for each component in the diagram.
        
        In a more advanced implementation, this would use a proper layout algorithm.
        For now, we'll use a simple grid layout.
        
        Args:
            diagram: The ComponentDiagram to calculate positions for
            
        Returns:
            A dictionary mapping component IDs to (x, y) positions
        """
        positions = {}
        rows = int(math.ceil(math.sqrt(len(diagram.components))))
        cols = int(math.ceil(len(diagram.components) / rows))
        
        for i, component in enumerate(diagram.components):
            row = i // cols
            col = i % cols
            
            x = 50 + col * (self.component_width + self.component_spacing)
            y = 50 + row * (self.component_height + self.component_spacing)
            
            positions[component.id] = (x, y)
        
        return positions
    
    def _render_component(self, 
                          group: Group, 
                          component: Component, 
                          position: Tuple[int, int]) -> None:
        """
        Render a component at the specified position.
        
        Args:
            group: The SVG group to add the component to
            component: The Component object to render
            position: The (x, y) position to place the component
        """
        x, y = position
        
        # Component rectangle
        rect = Rect(
            insert=(x, y),
            size=(self.component_width, self.component_height),
            rx=5, ry=5,
            fill=self.component_fill,
            stroke=self.component_stroke,
            stroke_width=2
        )
        group.add(rect)
        
        # Component symbol (small rectangles in top-right)
        symbol_x = x + self.component_width - self.component_symbol_width - self.component_symbol_offset
        symbol_y = y + self.component_symbol_offset
        
        # Draw two small rectangles for the component symbol
        rect1 = Rect(
            insert=(symbol_x, symbol_y),
            size=(self.component_symbol_width, self.component_symbol_height),
            rx=2, ry=2,
            fill=self.component_fill,
            stroke=self.component_stroke,
            stroke_width=1
        )
        group.add(rect1)
        
        rect2 = Rect(
            insert=(symbol_x - 5, symbol_y + 5),
            size=(10, 10),
            rx=1, ry=1,
            fill=self.component_fill,
            stroke=self.component_stroke,
            stroke_width=1
        )
        group.add(rect2)
        
        # Add stereotype if present
        text_y = y + 25
        if component.stereotype:
            stereotype_text = Text(
                f"«{component.stereotype}»",
                insert=(x + self.component_width / 2, text_y),
                fill="#696969",
                font_family="Arial, sans-serif",
                font_style="italic",
                text_anchor="middle"
            )
            group.add(stereotype_text)
            text_y += 20
        
        # Component name
        name_text = Text(
            component.name,
            insert=(x + self.component_width / 2, text_y),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Component type indicator (if not a regular component)
        if component.component_type != ComponentType.COMPONENT:
            type_text = Text(
                f"({component.component_type.name.lower()})",
                insert=(x + self.component_width / 2, text_y + 20),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(type_text)
    
    def _calculate_interface_position(self,
                                     component_pos: Tuple[int, int],
                                     component: Component,
                                     interface: Interface,
                                     is_provided: bool) -> Tuple[int, int]:
        """
        Calculate the position for an interface relative to its component.
        
        Args:
            component_pos: The (x, y) position of the component
            component: The Component object that owns the interface
            interface: The Interface object to position
            is_provided: Whether this is a provided interface
            
        Returns:
            The (x, y) position for the interface
        """
        # For simplicity, we'll position interfaces along the left or right
        # side of the component based on whether they're provided or required
        x, y = component_pos
        
        # Position provided interfaces on the right side
        if is_provided:
            interface_x = x + self.component_width
            # Distribute interfaces evenly along the right side
            idx = component.provided_interfaces.index(interface)
            total = len(component.provided_interfaces)
            interface_y = y + (self.component_height / (total + 1)) * (idx + 1)
        # Position required interfaces on the left side
        else:
            interface_x = x
            # Distribute interfaces evenly along the left side
            idx = component.required_interfaces.index(interface)
            total = len(component.required_interfaces)
            interface_y = y + (self.component_height / (total + 1)) * (idx + 1)
        
        return (interface_x, interface_y)
    
    def _render_interface(self, 
                          group: Group, 
                          interface: Interface, 
                          position: Tuple[int, int],
                          is_provided: bool) -> None:
        """
        Render an interface at the specified position.
        
        Args:
            group: The SVG group to add the interface to
            interface: The Interface object to render
            position: The (x, y) position to place the interface
            is_provided: Whether this is a provided interface
        """
        x, y = position
        
        # Provided interfaces use a "lollipop" notation (circle on a stick)
        if is_provided:
            # Line (stick)
            line = Line(
                start=(x, y),
                end=(x + 15, y),
                stroke=self.connector_color,
                stroke_width=1.5
            )
            group.add(line)
            
            # Circle (lollipop)
            circle = Circle(
                center=(x + 15 + self.interface_radius, y),
                r=self.interface_radius,
                fill=self.interface_fill,
                stroke=self.interface_stroke,
                stroke_width=1.5
            )
            group.add(circle)
            
            # Interface name
            text = Text(
                interface.name,
                insert=(x + 15 + self.interface_radius * 2 + 5, y + 5),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="12px"
            )
            group.add(text)
        
        # Required interfaces use a "socket" notation (half-circle)
        else:
            # Line (stick)
            line = Line(
                start=(x, y),
                end=(x - 15, y),
                stroke=self.connector_color,
                stroke_width=1.5
            )
            group.add(line)
            
            # Half-circle (socket) - using a path
            path_data = f"M {x - 15} {y - self.interface_radius} " \
                        f"A {self.interface_radius} {self.interface_radius} 0 0 0 " \
                        f"{x - 15} {y + self.interface_radius}"
            path = Path(
                d=path_data, 
                fill="none", 
                stroke=self.interface_stroke, 
                stroke_width=1.5
            )
            group.add(path)
            
            # Interface name
            text = Text(
                interface.name,
                insert=(x - 15 - self.interface_radius * 2 - 5, y + 5),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="end"
            )
            group.add(text)
    
    def _render_connector(self,
                         group: Group,
                         connector: Connector,
                         start_pos: Tuple[int, int],
                         end_pos: Tuple[int, int]) -> None:
        """
        Render a connector between two elements.
        
        Args:
            group: The SVG group to add the connector to
            connector: The Connector object to render
            start_pos: The (x, y) position of the source element
            end_pos: The (x, y) position of the target element
        """
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Determine connector style based on type
        stroke_dasharray = None
        if connector.connector_type in [
            ConnectorType.DELEGATION, 
            ConnectorType.DEPENDENCY, 
            ConnectorType.REALIZATION
        ]:
            stroke_dasharray = "5,3"
        
        # Add line with appropriate style
        line = Line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=self.connector_color,
            stroke_width=1.5,
            stroke_dasharray=stroke_dasharray
        )
        
        # Add arrow markers based on connector type
        if connector.connector_type == ConnectorType.DEPENDENCY:
            line["marker-end"] = "url(#arrow)"
        elif connector.connector_type == ConnectorType.REALIZATION:
            line["marker-end"] = "url(#hollow-arrow)"
        
        group.add(line)
        
        # Add connector name if present
        if connector.name:
            # Calculate midpoint for label placement
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Offset the label perpendicular to the line
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                offset = 15  # Offset distance
                nx = -dy / length * offset
                ny = dx / length * offset
                
                text = Text(
                    connector.name,
                    insert=(mid_x + nx, mid_y + ny),
                    fill=self.text_color,
                    font_family="Arial, sans-serif",
                    font_size="12px",
                    text_anchor="middle"
                )
                
                # Add stereotype if present
                if connector.stereotype:
                    stereotype_text = Text(
                        f"«{connector.stereotype}»",
                        insert=(mid_x + nx, mid_y + ny - 15),
                        fill="#696969",
                        font_family="Arial, sans-serif",
                        font_style="italic",
                        font_size="10px",
                        text_anchor="middle"
                    )
                    group.add(stereotype_text)
                
                group.add(text)
    
    def _render_artifact(self,
                        group: Group,
                        artifact: Artifact,
                        position: Tuple[int, int]) -> None:
        """
        Render an artifact at the specified position.
        
        Args:
            group: The SVG group to add the artifact to
            artifact: The Artifact object to render
            position: The (x, y) position to place the artifact
        """
        x, y = position
        width = self.component_width
        height = self.component_height - 20
        
        # Create the main rectangle
        rect = Rect(
            insert=(x, y),
            size=(width, height),
            fill=self.artifact_fill,
            stroke=self.artifact_stroke,
            stroke_width=1.5
        )
        group.add(rect)
        
        # Create the "dog-ear" effect in the top-right corner
        fold_size = 15
        path_data = f"M {x + width - fold_size} {y} " \
                    f"L {x + width} {y + fold_size} " \
                    f"L {x + width} {y} Z"
        fold = Path(
            d=path_data, 
            fill=self.artifact_fill, 
            stroke=self.artifact_stroke, 
            stroke_width=1.5
        )
        group.add(fold)
        
        # Add line for folded corner
        fold_line = Path(
            d=f"M {x + width - fold_size} {y} L {x + width - fold_size} {y + fold_size} L {x + width} {y + fold_size}",
            fill="none",
            stroke=self.artifact_stroke,
            stroke_width=1.5
        )
        group.add(fold_line)
        
        # Add stereotype if present
        text_y = y + 20
        if artifact.stereotype:
            stereotype_text = Text(
                f"«{artifact.stereotype}»",
                insert=(x + width / 2, text_y),
                fill="#696969",
                font_family="Arial, sans-serif",
                font_style="italic",
                text_anchor="middle"
            )
            group.add(stereotype_text)
            text_y += 20
        
        # Artifact name
        name_text = Text(
            artifact.name,
            insert=(x + width / 2, text_y),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text) 