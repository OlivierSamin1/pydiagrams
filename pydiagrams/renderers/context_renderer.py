#!/usr/bin/env python3
"""
Renderer for System Context Diagrams.

This module provides specialized rendering for System Context Diagrams,
visualizing systems, people, external systems, and their relationships.
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

from pydiagrams.diagrams.architectural.context_diagram import (
    SystemContextDiagram, ContextElement, ContextRelationship, 
    Boundary, ElementType, RelationshipType
)
from pydiagrams.renderers.svg_renderer import SVGRenderer


@dataclass
class SystemContextDiagramRenderer(SVGRenderer):
    """
    Specialized renderer for System Context Diagrams.
    
    This renderer visualizes system elements, people, external systems,
    and their relationships in a System Context Diagram.
    """
    # Default dimensions of the diagram
    width: int = 1200
    height: int = 900
    unit: str = "px"
    
    # Styling properties
    element_width: int = 180
    element_height: int = 120
    person_width: int = 100
    person_height: int = 140
    element_spacing: int = 80
    boundary_padding: int = 40
    text_margin: int = 10
    line_stroke_width: int = 2
    arrow_size: int = 10
    
    # Colors
    element_fill: Dict[ElementType, str] = field(default_factory=lambda: {
        ElementType.SYSTEM: "#1168BD",
        ElementType.PERSON: "#08427B",
        ElementType.EXTERNAL_SYSTEM: "#999999",
        ElementType.ENTERPRISE_BOUNDARY: "#444444",
        ElementType.CONTAINER: "#438DD5",
        ElementType.DATABASE: "#438DD5"
    })
    element_text_color: Dict[ElementType, str] = field(default_factory=lambda: {
        ElementType.SYSTEM: "#FFFFFF",
        ElementType.PERSON: "#FFFFFF",
        ElementType.EXTERNAL_SYSTEM: "#FFFFFF",
        ElementType.ENTERPRISE_BOUNDARY: "#FFFFFF",
        ElementType.CONTAINER: "#FFFFFF",
        ElementType.DATABASE: "#FFFFFF"
    })
    relationship_color: str = "#707070"
    boundary_fill: str = "#FFFFFF"
    boundary_stroke: str = "#444444"
    
    def render(self, 
               diagram: SystemContextDiagram, 
               output_path: str, 
               **kwargs) -> str:
        """
        Render a System Context Diagram to an SVG file.
        
        Args:
            diagram: The SystemContextDiagram object to render
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
        element_group = self.drawing.add(Group(id="elements"))
        relationship_group = self.drawing.add(Group(id="relationships"))
        label_group = self.drawing.add(Group(id="relationship-labels"))
        
        # Calculate positions for elements
        positions = self._calculate_positions(diagram)
        
        # Map boundaries to their contained elements
        boundary_elements = self._map_boundaries_to_elements(diagram)
        
        # Draw boundaries first (they'll be in the background)
        boundary_bounds = self._calculate_boundary_bounds(diagram, positions, boundary_elements)
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
        
        # Draw elements
        for element in diagram.elements:
            pos = positions.get(element.id, (self.width // 2, self.height // 2))
            self._render_element(element_group, element, pos)
        
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
    
    def _calculate_positions(self, diagram: SystemContextDiagram) -> Dict[str, Tuple[int, int]]:
        """
        Calculate positions for each element in the diagram.
        
        Args:
            diagram: The SystemContextDiagram to calculate positions for
            
        Returns:
            A dictionary mapping element IDs to (x, y) positions
        """
        # Use the layout manager to calculate positions
        elements = diagram.elements
        relationships = diagram.relationships
        
        positions = diagram.layout.apply(elements, relationships)
        
        # If the layout manager didn't provide positions for all elements,
        # use a simple grid layout as fallback
        if not positions or len(positions) < len(diagram.elements):
            positions = {}
            rows = int(math.ceil(math.sqrt(len(diagram.elements))))
            cols = int(math.ceil(len(diagram.elements) / rows))
            
            for i, element in enumerate(diagram.elements):
                row = i // cols
                col = i % cols
                
                x = 100 + col * (self.element_width + self.element_spacing)
                y = 100 + row * (self.element_height + self.element_spacing)
                
                positions[element.id] = (x, y)
        
        return positions
    
    def _map_boundaries_to_elements(self, diagram: SystemContextDiagram) -> Dict[str, List[str]]:
        """
        Create a mapping from boundary IDs to lists of element IDs.
        
        Args:
            diagram: The SystemContextDiagram to process
            
        Returns:
            Dictionary mapping boundary IDs to lists of element IDs
        """
        return {boundary.id: boundary.element_ids for boundary in diagram.boundaries}
    
    def _calculate_boundary_bounds(
        self,
        diagram: SystemContextDiagram,
        positions: Dict[str, Tuple[int, int]],
        boundary_elements: Dict[str, List[str]]
    ) -> Dict[str, Tuple[int, int, int, int]]:
        """
        Calculate the bounding box for each boundary based on contained elements.
        
        Args:
            diagram: The SystemContextDiagram to process
            positions: Dictionary mapping element IDs to (x, y) positions
            boundary_elements: Dictionary mapping boundary IDs to lists of element IDs
            
        Returns:
            Dictionary mapping boundary IDs to (x, y, width, height) bounds
        """
        boundary_bounds = {}
        
        for boundary_id, element_ids in boundary_elements.items():
            if not element_ids:
                continue
                
            # Get positions of all elements in this boundary
            element_positions = [positions[e_id] for e_id in element_ids if e_id in positions]
            
            if not element_positions:
                continue
                
            # Find elements by ID to determine their sizes
            element_dict = {elem.id: elem for elem in diagram.elements}
            element_sizes = []
            
            for e_id in element_ids:
                if e_id in element_dict:
                    element = element_dict[e_id]
                    if element.element_type == ElementType.PERSON:
                        element_sizes.append((self.person_width, self.person_height))
                    else:
                        element_sizes.append((self.element_width, self.element_height))
            
            # Calculate min/max coordinates with element sizes
            min_x = float('inf')
            min_y = float('inf')
            max_x = float('-inf')
            max_y = float('-inf')
            
            for pos, size in zip(element_positions, element_sizes):
                min_x = min(min_x, pos[0] - size[0] // 2)
                min_y = min(min_y, pos[1] - size[1] // 2)
                max_x = max(max_x, pos[0] + size[0] // 2)
                max_y = max(max_y, pos[1] + size[1] // 2)
            
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
    
    def _render_element(self,
                       group: Group,
                       element: ContextElement,
                       position: Tuple[int, int]) -> None:
        """
        Render an element at the specified position.
        
        Args:
            group: The SVG group to add the element to
            element: The ContextElement object to render
            position: The (x, y) position to place the element
        """
        x, y = position
        
        # Create element group
        element_group = group.add(Group(id=f"element-{element.id}"))
        
        # Get styling based on element type
        fill_color = self.element_fill.get(element.element_type, "#CCCCCC")
        text_color = self.element_text_color.get(element.element_type, "#000000")
        
        if element.element_type == ElementType.PERSON:
            # Person is a special case - render as a stick figure above a box
            self._render_person(element_group, element, (x, y), fill_color, text_color)
        else:
            # Other elements are rendered as rectangles
            self._render_box_element(element_group, element, (x, y), fill_color, text_color)
    
    def _render_person(self,
                      group: Group,
                      element: ContextElement,
                      position: Tuple[int, int],
                      fill_color: str,
                      text_color: str) -> None:
        """
        Render a person element (stick figure and box).
        
        Args:
            group: The SVG group to add the person to
            element: The ContextElement object to render
            position: The (x, y) position to place the person
            fill_color: Fill color for the person
            text_color: Text color for the person's name
        """
        x, y = position
        
        # Draw person icon (head and body)
        head_radius = 15
        head_center_y = y - self.person_height // 2 + head_radius + 10
        
        # Head (circle)
        head = Circle(
            center=(x, head_center_y),
            r=head_radius,
            fill=fill_color,
            stroke="none"
        )
        group.add(head)
        
        # Body (line)
        body = Line(
            start=(x, head_center_y + head_radius),
            end=(x, head_center_y + head_radius + 30),
            stroke=fill_color,
            stroke_width=4
        )
        group.add(body)
        
        # Arms (line)
        arms = Line(
            start=(x - 20, head_center_y + head_radius + 15),
            end=(x + 20, head_center_y + head_radius + 15),
            stroke=fill_color,
            stroke_width=4
        )
        group.add(arms)
        
        # Legs (lines)
        leg1 = Line(
            start=(x, head_center_y + head_radius + 30),
            end=(x - 15, head_center_y + head_radius + 50),
            stroke=fill_color,
            stroke_width=4
        )
        group.add(leg1)
        
        leg2 = Line(
            start=(x, head_center_y + head_radius + 30),
            end=(x + 15, head_center_y + head_radius + 50),
            stroke=fill_color,
            stroke_width=4
        )
        group.add(leg2)
        
        # Box for name and description
        box_y = y + self.person_height // 4
        box_height = self.person_height // 2
        
        rect = Rect(
            insert=(x - self.person_width // 2, box_y),
            size=(self.person_width, box_height),
            rx=3, ry=3,
            fill=fill_color,
            stroke="none"
        )
        group.add(rect)
        
        # Add name
        name_text = Text(
            element.name,
            insert=(x, box_y + 20),
            fill=text_color,
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add description (if it fits)
        if element.description:
            desc_text = Text(
                element.description,
                insert=(x, box_y + 40),
                fill=text_color,
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="middle"
            )
            group.add(desc_text)
    
    def _render_box_element(self,
                           group: Group,
                           element: ContextElement,
                           position: Tuple[int, int],
                           fill_color: str,
                           text_color: str) -> None:
        """
        Render a box-shaped element.
        
        Args:
            group: The SVG group to add the element to
            element: The ContextElement object to render
            position: The (x, y) position to place the element
            fill_color: Fill color for the element
            text_color: Text color for the element's name
        """
        x, y = position
        
        # Adjust position to center the element
        x_offset = self.element_width // 2
        y_offset = self.element_height // 2
        
        # Create the main rectangle
        rect = Rect(
            insert=(x - x_offset, y - y_offset),
            size=(self.element_width, self.element_height),
            rx=3, ry=3,
            fill=fill_color,
            stroke="none"
        )
        group.add(rect)
        
        # Special treatment for database elements
        if element.element_type == ElementType.DATABASE:
            # Add database-specific styling (rounded bottom, lines at top)
            top_arc = Path(
                d=f"M{x - x_offset} {y - y_offset + 20} A{self.element_width // 2} 10 0 0 1 {x + x_offset} {y - y_offset + 20}",
                fill="none",
                stroke="#FFFFFF",
                stroke_width=1.5
            )
            group.add(top_arc)
            
            bottom_arc = Path(
                d=f"M{x - x_offset} {y + y_offset - 1} A{self.element_width // 2} 10 0 0 0 {x + x_offset} {y + y_offset - 1}",
                fill="none",
                stroke="#FFFFFF",
                stroke_width=1.5
            )
            group.add(bottom_arc)
        
        # Add element type label at the top
        type_label = ""
        if element.element_type == ElementType.SYSTEM:
            type_label = "[System]"
        elif element.element_type == ElementType.EXTERNAL_SYSTEM:
            type_label = "[External System]"
        elif element.element_type == ElementType.CONTAINER:
            type_label = "[Container]"
        elif element.element_type == ElementType.DATABASE:
            type_label = "[Database]"
            
        if type_label:
            type_text = Text(
                type_label,
                insert=(x, y - y_offset + 20),
                fill=text_color,
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(type_text)
        
        # Add name
        name_text = Text(
            element.name,
            insert=(x, y),
            fill=text_color,
            font_family="Arial, sans-serif",
            font_size="14px",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add description (if it fits)
        if element.description:
            desc_text = Text(
                self._wrap_text(element.description, 25),
                insert=(x, y + 25),
                fill=text_color,
                font_family="Arial, sans-serif",
                font_size="12px",
                text_anchor="middle"
            )
            group.add(desc_text)
    
    def _render_relationship(self,
                            group: Group,
                            relationship: ContextRelationship,
                            start_pos: Tuple[int, int],
                            end_pos: Tuple[int, int]) -> Tuple[float, float]:
        """
        Render a relationship between two elements.
        
        Args:
            group: The SVG group to add the relationship to
            relationship: The ContextRelationship object to render
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
        offset = self.element_width // 2 + 10  # A bit more than half-width
        
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
        # For simplicity, just using different dash patterns for different types
        if relationship.relationship_type == RelationshipType.DEPENDS_ON:
            line["stroke-dasharray"] = "10,5"
        elif relationship.relationship_type == RelationshipType.SENDS_DATA_TO:
            line["stroke-dasharray"] = "5,3"
        elif relationship.relationship_type == RelationshipType.RECEIVES_DATA_FROM:
            line["stroke-dasharray"] = "5,3,1,3"
        
        group.add(line)
        
        return (mid_x, mid_y)
    
    def _render_relationship_label(self,
                                  group: Group,
                                  relationship: ContextRelationship,
                                  position: Tuple[float, float]) -> None:
        """
        Render a label for a relationship.
        
        Args:
            group: The SVG group to add the label to
            relationship: The ContextRelationship object
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
                        boundary: Boundary,
                        bounds: Tuple[int, int, int, int]) -> None:
        """
        Render a boundary.
        
        Args:
            group: The SVG group to add the boundary to
            boundary: The Boundary object to render
            bounds: The (x, y, width, height) bounds of the boundary
        """
        x, y, width, height = bounds
        
        # Create boundary rectangle
        rect = Rect(
            insert=(x, y),
            size=(width, height),
            rx=10, ry=10,
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