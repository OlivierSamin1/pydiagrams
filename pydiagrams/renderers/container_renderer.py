#!/usr/bin/env python3
"""
Renderer for Container Diagrams.

This module provides specialized rendering for Container Diagrams,
visualizing the containers within a system, people, external systems,
and their relationships.
"""

import math
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any, Union

from svgwrite import Drawing
from svgwrite.container import Group
from svgwrite.shapes import Line, Rect, Circle, Polygon, Ellipse
from svgwrite.text import Text
from svgwrite.path import Path

from pydiagrams.diagrams.architectural.container_diagram import (
    ContainerDiagram, Person, Container, ExternalSystem, 
    ContainerRelationship, SystemBoundary, ContainerType, 
    ContainerRelationshipType
)
from pydiagrams.renderers.svg_renderer import SVGRenderer


@dataclass
class ContainerDiagramRenderer(SVGRenderer):
    """
    Specialized renderer for Container Diagrams.
    
    This renderer visualizes containers, people, external systems,
    and their relationships in a Container Diagram.
    """
    # Default dimensions of the diagram
    width: int = 1200
    height: int = 900
    unit: str = "px"
    
    # Styling properties
    container_width: int = 200
    container_height: int = 130
    person_width: int = 100
    person_height: int = 140
    external_system_width: int = 180
    external_system_height: int = 120
    element_spacing: int = 80
    boundary_padding: int = 40
    text_margin: int = 10
    line_stroke_width: int = 2
    arrow_size: int = 10
    
    # Colors
    container_fill: Dict[ContainerType, str] = field(default_factory=lambda: {
        ContainerType.WEB_APPLICATION: "#438DD5",  # Blue
        ContainerType.MOBILE_APP: "#438DD5",       # Blue
        ContainerType.DESKTOP_APP: "#438DD5",      # Blue
        ContainerType.API: "#438DD5",              # Blue
        ContainerType.DATABASE: "#438DD5",         # Blue
        ContainerType.FILE_SYSTEM: "#438DD5",      # Blue
        ContainerType.MICROSERVICE: "#438DD5",     # Blue
        ContainerType.QUEUE: "#438DD5",            # Blue
        ContainerType.SERVER_SIDE: "#438DD5",      # Blue
        ContainerType.CACHE: "#438DD5",            # Blue
        ContainerType.CUSTOM: "#438DD5"            # Blue
    })
    person_fill: str = "#08427B"  # Dark blue
    external_system_fill: str = "#999999"  # Gray
    text_color: Dict[str, str] = field(default_factory=lambda: {
        "container": "#FFFFFF",  # White
        "person": "#FFFFFF",     # White
        "external": "#FFFFFF"    # White
    })
    relationship_color: str = "#707070"  # Dark gray
    boundary_fill: str = "#FFFFFF"       # White
    boundary_stroke: str = "#444444"     # Dark gray
    
    def render(self, 
               diagram: ContainerDiagram, 
               output_path: str, 
               **kwargs) -> str:
        """
        Render a Container Diagram to an SVG file.
        
        Args:
            diagram: The ContainerDiagram object to render
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
        boundary_group = self.drawing.add(Group(id="boundaries"))
        container_group = self.drawing.add(Group(id="containers"))
        person_group = self.drawing.add(Group(id="people"))
        external_system_group = self.drawing.add(Group(id="external-systems"))
        relationship_group = self.drawing.add(Group(id="relationships"))
        label_group = self.drawing.add(Group(id="relationship-labels"))
        
        # Calculate positions for all elements
        positions = self._calculate_positions(diagram)
        
        # Map boundaries to their contained containers
        boundary_containers = self._map_boundaries_to_containers(diagram)
        
        # Draw boundaries first (they'll be in the background)
        boundary_bounds = self._calculate_boundary_bounds(diagram, positions, boundary_containers)
        for boundary in diagram.boundaries:
            if boundary.id in boundary_bounds:
                self._render_boundary(boundary_group, boundary, boundary_bounds[boundary.id])
        
        # Draw relationships
        relationship_midpoints = {}
        for relationship in diagram.relationships:
            source_pos = positions.get(relationship.source_id)
            target_pos = positions.get(relationship.target_id)
            
            if source_pos and target_pos:
                midpoint = self._render_relationship(
                    relationship_group,
                    relationship,
                    source_pos,
                    target_pos
                )
                relationship_midpoints[relationship.id] = midpoint
        
        # Draw containers
        for container in diagram.containers:
            pos = positions.get(container.id, (self.width // 2, self.height // 2))
            self._render_container(container_group, container, pos)
        
        # Draw people
        for person in diagram.people:
            pos = positions.get(person.id, (self.width // 2, self.height // 2))
            self._render_person(person_group, person, pos)
        
        # Draw external systems
        for ext_system in diagram.external_systems:
            pos = positions.get(ext_system.id, (self.width // 2, self.height // 2))
            self._render_external_system(external_system_group, ext_system, pos)
        
        # Draw relationship labels
        for relationship in diagram.relationships:
            if relationship.id in relationship_midpoints:
                self._render_relationship_label(
                    label_group,
                    relationship,
                    relationship_midpoints[relationship.id]
                )
        
        # Save the SVG
        self.drawing.save()
        return output_path
    
    def _add_defs(self) -> None:
        """Add definitions to the SVG (markers, patterns, etc.)."""
        # Add arrow marker for relationships
        marker = self.drawing.marker(
            insert=(10, 5),
            size=(10, 10),
            orient="auto",
            id="arrow"
        )
        marker.add(self.drawing.path(
            "M0,0 L10,5 L0,10 L3,5 Z",
            fill=self.relationship_color
        ))
        self.drawing.defs.add(marker)
    
    def _calculate_positions(self, diagram: ContainerDiagram) -> Dict[str, Tuple[int, int]]:
        """
        Calculate positions for all elements in the diagram.
        
        Args:
            diagram: The ContainerDiagram to calculate positions for
            
        Returns:
            A dictionary mapping element IDs to (x, y) positions
        """
        # Collect all elements across types
        elements = []
        elements.extend(diagram.containers)
        elements.extend(diagram.people)
        elements.extend(diagram.external_systems)
        
        # Map for layout engine
        element_map = {elem.id: elem for elem in elements}
        
        # Use the layout manager to calculate positions
        relationships = diagram.relationships
        
        positions = diagram.layout.apply(elements, relationships)
        
        # If the layout manager didn't provide positions for all elements,
        # use a simple grid layout as fallback
        if not positions or len(positions) < len(elements):
            positions = {}
            rows = int(math.ceil(math.sqrt(len(elements))))
            cols = int(math.ceil(len(elements) / rows))
            
            # Sort elements for more predictable layout (people first, then containers, then externals)
            sorted_elements = []
            sorted_elements.extend(diagram.people)
            sorted_elements.extend(diagram.containers)
            sorted_elements.extend(diagram.external_systems)
            
            for i, element in enumerate(sorted_elements):
                row = i // cols
                col = i % cols
                
                x = 100 + col * (self.container_width + self.element_spacing)
                y = 100 + row * (self.container_height + self.element_spacing)
                
                positions[element.id] = (x, y)
        
        return positions
    
    def _map_boundaries_to_containers(self, diagram: ContainerDiagram) -> Dict[str, List[str]]:
        """
        Create a mapping from boundary IDs to lists of container IDs.
        
        Args:
            diagram: The ContainerDiagram to process
            
        Returns:
            Dictionary mapping boundary IDs to lists of container IDs
        """
        return {boundary.id: boundary.container_ids for boundary in diagram.boundaries}
    
    def _calculate_boundary_bounds(
        self,
        diagram: ContainerDiagram,
        positions: Dict[str, Tuple[int, int]],
        boundary_containers: Dict[str, List[str]]
    ) -> Dict[str, Tuple[int, int, int, int]]:
        """
        Calculate the bounding box for each boundary based on contained containers.
        
        Args:
            diagram: The ContainerDiagram to process
            positions: Dictionary mapping element IDs to (x, y) positions
            boundary_containers: Dictionary mapping boundary IDs to lists of container IDs
            
        Returns:
            Dictionary mapping boundary IDs to (x, y, width, height) bounds
        """
        boundary_bounds = {}
        
        for boundary_id, container_ids in boundary_containers.items():
            if not container_ids:
                continue
                
            # Get positions of all containers in this boundary
            container_positions = [positions[c_id] for c_id in container_ids if c_id in positions]
            
            if not container_positions:
                continue
                
            # Calculate min/max coordinates with standard container size
            min_x = float('inf')
            min_y = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')
            
            for pos in container_positions:
                min_x = min(min_x, pos[0] - self.container_width // 2)
                min_y = min(min_y, pos[1] - self.container_height // 2)
                max_x = max(max_x, pos[0] + self.container_width // 2)
                max_y = max(max_y, pos[1] + self.container_height // 2)
            
            # Add padding
            min_x -= self.boundary_padding
            min_y -= self.boundary_padding
            max_x += self.boundary_padding
            max_y += self.boundary_padding
            
            # Calculate width and height
            width = max_x - min_x
            height = max_y - min_y
            
            boundary_bounds[boundary_id] = (min_x, min_y, width, height)
        
        return boundary_bounds
    
    def _render_person(self,
                       group: Group,
                       person: Person,
                       position: Tuple[int, int]) -> None:
        """
        Render a person at the specified position.
        
        Args:
            group: The SVG group to add the person to
            person: The Person object to render
            position: The (x, y) position to place the person
        """
        x, y = position
        
        # Create person group
        person_group = group.add(Group(id=f"person-{person.id}"))
        
        # Draw person icon (head and body)
        head_radius = 15
        head_center_y = y - self.person_height // 2 + head_radius + 10
        
        # Head (circle)
        head = Circle(
            center=(x, head_center_y),
            r=head_radius,
            fill=self.person_fill,
            stroke="none"
        )
        person_group.add(head)
        
        # Body (line)
        body = Line(
            start=(x, head_center_y + head_radius),
            end=(x, head_center_y + head_radius + 30),
            stroke=self.person_fill,
            stroke_width=4
        )
        person_group.add(body)
        
        # Arms (line)
        arms = Line(
            start=(x - 20, head_center_y + head_radius + 15),
            end=(x + 20, head_center_y + head_radius + 15),
            stroke=self.person_fill,
            stroke_width=4
        )
        person_group.add(arms)
        
        # Legs (lines)
        leg1 = Line(
            start=(x, head_center_y + head_radius + 30),
            end=(x - 15, head_center_y + head_radius + 50),
            stroke=self.person_fill,
            stroke_width=4
        )
        person_group.add(leg1)
        
        leg2 = Line(
            start=(x, head_center_y + head_radius + 30),
            end=(x + 15, head_center_y + head_radius + 50),
            stroke=self.person_fill,
            stroke_width=4
        )
        person_group.add(leg2)
        
        # Box for name and description
        box_y = y + self.person_height // 4
        box_height = self.person_height // 2
        
        rect = Rect(
            insert=(x - self.person_width // 2, box_y),
            size=(self.person_width, box_height),
            rx=3, ry=3,
            fill=self.person_fill,
            stroke="none"
        )
        person_group.add(rect)
        
        # Add person type
        person_type = "External Person" if person.external else "Person"
        type_text = Text(
            f"[{person_type}]",
            insert=(x, box_y + 15),
            fill=self.text_color["person"],
            font_family="Arial, sans-serif",
            font_size="10px",
            text_anchor="middle",
            font_style="italic"
        )
        person_group.add(type_text)
        
        # Add name
        name_text = Text(
            person.name,
            insert=(x, box_y + 35),
            fill=self.text_color["person"],
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        person_group.add(name_text)
        
        # Add description (if it fits)
        if person.description:
            desc_text = Text(
                self._wrap_text(person.description, 15),
                insert=(x, box_y + 55),
                fill=self.text_color["person"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            person_group.add(desc_text)
    
    def _render_container(self,
                         group: Group,
                         container: Container,
                         position: Tuple[int, int]) -> None:
        """
        Render a container at the specified position.
        
        Args:
            group: The SVG group to add the container to
            container: The Container object to render
            position: The (x, y) position to place the container
        """
        x, y = position
        
        # Create container group
        container_group = group.add(Group(id=f"container-{container.id}"))
        
        # Adjust position to center the container
        x_offset = self.container_width // 2
        y_offset = self.container_height // 2
        
        # Get fill color based on container type
        fill_color = self.container_fill.get(container.container_type, "#438DD5")
        
        # Create different shapes based on container type
        if container.container_type == ContainerType.DATABASE:
            # Database shape (cylinder)
            self._render_database(
                container_group, 
                container, 
                (x, y), 
                fill_color
            )
        elif container.container_type == ContainerType.QUEUE:
            # Queue shape (rectangle with pipes)
            self._render_queue(
                container_group, 
                container, 
                (x, y), 
                fill_color
            )
        else:
            # Standard container (rectangle)
            rect = Rect(
                insert=(x - x_offset, y - y_offset),
                size=(self.container_width, self.container_height),
                rx=3, ry=3,
                fill=fill_color,
                stroke="none"
            )
            container_group.add(rect)
            
            # Add container type
            container_type = self._get_container_type_label(container.container_type)
            type_text = Text(
                f"[{container_type}]",
                insert=(x, y - y_offset + 20),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="middle",
                font_style="italic"
            )
            container_group.add(type_text)
            
            # Add name
            name_text = Text(
                container.name,
                insert=(x, y),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="14px",
                text_anchor="middle",
                font_weight="bold"
            )
            container_group.add(name_text)
            
            # Add technology if present
            if container.technology:
                tech_text = Text(
                    f"[{container.technology}]",
                    insert=(x, y + 20),
                    fill=self.text_color["container"],
                    font_family="Arial, sans-serif",
                    font_size="10px",
                    text_anchor="middle",
                    font_style="italic"
                )
                container_group.add(tech_text)
            
            # Add description (if it fits)
            desc_y_pos = y + (30 if container.technology else 20)
            if container.description:
                desc_text = Text(
                    self._wrap_text(container.description, 25),
                    insert=(x, desc_y_pos),
                    fill=self.text_color["container"],
                    font_family="Arial, sans-serif",
                    font_size="10px",
                    text_anchor="middle"
                )
                container_group.add(desc_text)
    
    def _render_database(self,
                        group: Group,
                        container: Container,
                        position: Tuple[int, int],
                        fill_color: str) -> None:
        """
        Render a database container as a cylinder.
        
        Args:
            group: The SVG group to add the database to
            container: The Container object to render
            position: The (x, y) position to place the database
            fill_color: Fill color for the database
        """
        x, y = position
        x_offset = self.container_width // 2
        y_offset = self.container_height // 2
        
        # Main body rectangle
        rect = Rect(
            insert=(x - x_offset, y - y_offset + 10),
            size=(self.container_width, self.container_height - 20),
            fill=fill_color,
            stroke="none"
        )
        group.add(rect)
        
        # Top ellipse
        top_ellipse = Ellipse(
            center=(x, y - y_offset + 10),
            r=(self.container_width // 2, 10),
            fill=fill_color,
            stroke="none"
        )
        group.add(top_ellipse)
        
        # Bottom ellipse
        bottom_ellipse = Ellipse(
            center=(x, y + y_offset - 10),
            r=(self.container_width // 2, 10),
            fill=fill_color,
            stroke="none"
        )
        group.add(bottom_ellipse)
        
        # Add container type
        type_text = Text(
            "[Database]",
            insert=(x, y - y_offset + 25),
            fill=self.text_color["container"],
            font_family="Arial, sans-serif",
            font_size="12px",
            text_anchor="middle",
            font_style="italic"
        )
        group.add(type_text)
        
        # Add name
        name_text = Text(
            container.name,
            insert=(x, y),
            fill=self.text_color["container"],
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add technology if present
        if container.technology:
            tech_text = Text(
                f"[{container.technology}]",
                insert=(x, y + 20),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(tech_text)
        
        # Add description (if it fits)
        desc_y_pos = y + (30 if container.technology else 20)
        if container.description:
            desc_text = Text(
                self._wrap_text(container.description, 25),
                insert=(x, desc_y_pos),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            group.add(desc_text)
    
    def _render_queue(self,
                     group: Group,
                     container: Container,
                     position: Tuple[int, int],
                     fill_color: str) -> None:
        """
        Render a queue container with pipe-like indicators.
        
        Args:
            group: The SVG group to add the queue to
            container: The Container object to render
            position: The (x, y) position to place the queue
            fill_color: Fill color for the queue
        """
        x, y = position
        x_offset = self.container_width // 2
        y_offset = self.container_height // 2
        
        # Main rectangle
        rect = Rect(
            insert=(x - x_offset, y - y_offset),
            size=(self.container_width, self.container_height),
            rx=3, ry=3,
            fill=fill_color,
            stroke="none"
        )
        group.add(rect)
        
        # Add pipe indicators on left and right
        pipe_width = 8
        pipe_height = 20
        pipe_spacing = 15
        
        # Left pipes
        for i in range(3):
            pipe_y = y - pipe_height + i * pipe_spacing
            pipe_rect = Rect(
                insert=(x - x_offset - pipe_width, pipe_y),
                size=(pipe_width, pipe_height),
                fill=fill_color,
                stroke="none"
            )
            group.add(pipe_rect)
        
        # Right pipes
        for i in range(3):
            pipe_y = y - pipe_height + i * pipe_spacing
            pipe_rect = Rect(
                insert=(x + x_offset, pipe_y),
                size=(pipe_width, pipe_height),
                fill=fill_color,
                stroke="none"
            )
            group.add(pipe_rect)
        
        # Add container type
        type_text = Text(
            "[Queue]",
            insert=(x, y - y_offset + 20),
            fill=self.text_color["container"],
            font_family="Arial, sans-serif",
            font_size="12px",
            text_anchor="middle",
            font_style="italic"
        )
        group.add(type_text)
        
        # Add name
        name_text = Text(
            container.name,
            insert=(x, y),
            fill=self.text_color["container"],
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add technology if present
        if container.technology:
            tech_text = Text(
                f"[{container.technology}]",
                insert=(x, y + 20),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(tech_text)
        
        # Add description (if it fits)
        desc_y_pos = y + (30 if container.technology else 20)
        if container.description:
            desc_text = Text(
                self._wrap_text(container.description, 25),
                insert=(x, desc_y_pos),
                fill=self.text_color["container"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            group.add(desc_text)
    
    def _render_external_system(self,
                              group: Group,
                              external_system: ExternalSystem,
                              position: Tuple[int, int]) -> None:
        """
        Render an external system at the specified position.
        
        Args:
            group: The SVG group to add the external system to
            external_system: The ExternalSystem object to render
            position: The (x, y) position to place the external system
        """
        x, y = position
        
        # Create external system group
        ext_system_group = group.add(Group(id=f"ext-system-{external_system.id}"))
        
        # Adjust position to center the external system
        x_offset = self.external_system_width // 2
        y_offset = self.external_system_height // 2
        
        # Create the main rectangle
        rect = Rect(
            insert=(x - x_offset, y - y_offset),
            size=(self.external_system_width, self.external_system_height),
            rx=3, ry=3,
            fill=self.external_system_fill,
            stroke="none"
        )
        ext_system_group.add(rect)
        
        # Add external system type
        type_text = Text(
            "[External System]",
            insert=(x, y - y_offset + 20),
            fill=self.text_color["external"],
            font_family="Arial, sans-serif",
            font_size="12px",
            text_anchor="middle",
            font_style="italic"
        )
        ext_system_group.add(type_text)
        
        # Add name
        name_text = Text(
            external_system.name,
            insert=(x, y),
            fill=self.text_color["external"],
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        ext_system_group.add(name_text)
        
        # Add technology if present
        if external_system.technology:
            tech_text = Text(
                f"[{external_system.technology}]",
                insert=(x, y + 20),
                fill=self.text_color["external"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle",
                font_style="italic"
            )
            ext_system_group.add(tech_text)
        
        # Add description (if it fits)
        desc_y_pos = y + (30 if external_system.technology else 20)
        if external_system.description:
            desc_text = Text(
                self._wrap_text(external_system.description, 25),
                insert=(x, desc_y_pos),
                fill=self.text_color["external"],
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            ext_system_group.add(desc_text)
    
    def _render_relationship(self,
                           group: Group,
                           relationship: ContainerRelationship,
                           start_pos: Tuple[int, int],
                           end_pos: Tuple[int, int]) -> Tuple[float, float]:
        """
        Render a relationship between elements.
        
        Args:
            group: The SVG group to add the relationship to
            relationship: The ContainerRelationship object to render
            start_pos: The (x, y) position of the source element
            end_pos: The (x, y) position of the target element
            
        Returns:
            The (x, y) midpoint of the relationship for label placement
        """
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Calculate direction vector
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        if length < 1:  # Avoid division by zero
            return (x1, y1)
        
        # Normalize direction vector
        dx /= length
        dy /= length
        
        # Calculate offset from center to edge of element
        offset = self.container_width // 2 + 10  # A bit more than half-width
        
        # Adjust start and end points to be on the edge of elements
        x1 += dx * offset
        y1 += dy * offset
        x2 -= dx * offset
        y2 -= dy * offset
        
        # Calculate the midpoint for label placement
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Create the relationship line
        line = Line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=self.relationship_color,
            stroke_width=self.line_stroke_width,
            marker_end="url(#arrow)"
        )
        
        # Styling based on relationship type
        if relationship.relationship_type == ContainerRelationshipType.DEPENDS_ON:
            line["stroke-dasharray"] = "10,5"
        elif relationship.relationship_type == ContainerRelationshipType.READS_FROM:
            line["stroke-dasharray"] = "5,3"
        elif relationship.relationship_type == ContainerRelationshipType.WRITES_TO:
            line["stroke-dasharray"] = "5,3,1,3"
        elif relationship.relationship_type == ContainerRelationshipType.NOTIFIES:
            line["stroke-dasharray"] = "1,3"
        
        group.add(line)
        
        return (mid_x, mid_y)
    
    def _render_relationship_label(self,
                                 group: Group,
                                 relationship: ContainerRelationship,
                                 position: Tuple[float, float]) -> None:
        """
        Render a label for a relationship.
        
        Args:
            group: The SVG group to add the label to
            relationship: The ContainerRelationship object
            position: The (x, y) position for the label
        """
        x, y = position
        
        # Don't render if there's no label text
        if not relationship.name and not relationship.technology:
            return
        
        # Create background for the label
        label_bg = Rect(
            insert=(x - 70, y - 15),
            size=(140, 30),
            rx=5, ry=5,
            fill="white",
            fill_opacity=0.8,
            stroke="none"
        )
        group.add(label_bg)
        
        # Add relationship name
        if relationship.name:
            name_text = Text(
                relationship.name,
                insert=(x, y),
                fill="#000000",
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="middle"
            )
            group.add(name_text)
        
        # Add technology if present
        if relationship.technology:
            tech_text = Text(
                f"[{relationship.technology}]",
                insert=(x, y + (0 if not relationship.name else 15)),
                fill="#666666",
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(tech_text)
    
    def _render_boundary(self,
                       group: Group,
                       boundary: SystemBoundary,
                       bounds: Tuple[int, int, int, int]) -> None:
        """
        Render a system boundary.
        
        Args:
            group: The SVG group to add the boundary to
            boundary: The SystemBoundary object to render
            bounds: The (x, y, width, height) bounds of the boundary
        """
        x, y, width, height = bounds
        
        # Create boundary rectangle
        rect = Rect(
            insert=(x, y),
            size=(width, height),
            rx=15, ry=15,
            fill=self.boundary_fill,
            fill_opacity=0.1,
            stroke=self.boundary_stroke,
            stroke_width=1.5,
            stroke_dasharray="5,5"
        )
        group.add(rect)
        
        # Add boundary name in the top-left corner
        name_text = Text(
            boundary.name,
            insert=(x + 15, y + 25),
            fill="#000000",
            font_family="Arial, sans-serif",
            font_size="16px",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add description if present
        if boundary.description:
            desc_text = Text(
                boundary.description,
                insert=(x + 15, y + 45),
                fill="#666666",
                font_family="Arial, sans-serif",
                font_size="12px",
                font_style="italic"
            )
            group.add(desc_text)
    
    def _get_container_type_label(self, container_type: ContainerType) -> str:
        """
        Get a display label for a container type.
        
        Args:
            container_type: The ContainerType enum value
            
        Returns:
            A string representation of the container type
        """
        label_map = {
            ContainerType.WEB_APPLICATION: "Web Application",
            ContainerType.MOBILE_APP: "Mobile App",
            ContainerType.DESKTOP_APP: "Desktop App",
            ContainerType.API: "API",
            ContainerType.DATABASE: "Database",
            ContainerType.FILE_SYSTEM: "File System",
            ContainerType.MICROSERVICE: "Microservice",
            ContainerType.QUEUE: "Queue",
            ContainerType.SERVER_SIDE: "Server",
            ContainerType.CACHE: "Cache",
            ContainerType.CUSTOM: "Container"
        }
        return label_map.get(container_type, "Container")
    
    def _wrap_text(self, text: str, max_chars_per_line: int) -> str:
        """
        Wrap text to fit within a certain width.
        
        Args:
            text: The text to wrap
            max_chars_per_line: Maximum characters per line
            
        Returns:
            Text with line breaks inserted
        """
        if len(text) <= max_chars_per_line:
            return text
            
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + len(current_line) <= max_chars_per_line:
                current_line.append(word)
                current_length += len(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(" ".join(current_line))
            
        return "\n".join(lines) 