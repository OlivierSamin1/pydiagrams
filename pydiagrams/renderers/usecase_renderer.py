"""
Renderer for UML Use Case Diagrams.

This module provides a specialized renderer for UML Use Case Diagrams.
"""

import os
import math
from typing import Dict, List, Tuple, Any, Optional
import svgwrite
from svgwrite.container import Group

from pydiagrams.renderers.svg_renderer import SVGRenderer


class UseCaseDiagramRenderer(SVGRenderer):
    """Specialized renderer for UML Use Case Diagrams."""
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px"):
        """
        Initialize the use case diagram renderer.
        
        Args:
            width: The width of the diagram.
            height: The height of the diagram.
            unit: The unit of measurement (e.g., 'px', 'mm', 'cm').
        """
        super().__init__(width, height, unit)
        
        # Define default sizes and spacing
        self.actor_width = 50
        self.actor_height = 100
        self.usecase_width = 150
        self.usecase_height = 80
        self.system_padding = 30
        self.element_spacing = 50
        
        # Default positions for layout algorithm
        self.positions = {}
        self.system_dimensions = {}
        
        # Element colors
        self.actor_color = "#FFFFFF"
        self.actor_stroke = "#000000"
        self.usecase_fill = "#FFFFFF"
        self.usecase_stroke = "#000000"
        self.system_fill = "#FAFAFA"
        self.system_stroke = "#666666"
        self.relationship_color = "#000000"
        self.text_color = "#000000"
    
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render a use case diagram to an SVG file.
        
        Args:
            diagram_data: The diagram data as a dictionary.
            output_path: The path where the rendered diagram will be saved.
            
        Returns:
            The path to the rendered file.
        """
        # Create the SVG drawing
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}"),
        )
        
        # Add stylesheet
        self._add_usecase_stylesheet(dwg)
        
        # Add symbol definitions for reusable elements
        self._add_usecase_definitions(dwg)
        
        # Preprocess diagram data for layout
        self._preprocess_usecase_diagram(diagram_data)
        
        # Create a main group for the diagram
        main_group = dwg.g(id="main")
        
        # Render all systems first (as boundaries)
        for element in diagram_data.get("elements", []):
            if element.get("type") == "system":
                system_group = self._render_system(dwg, element, diagram_data)
                if system_group:
                    main_group.add(system_group)
        
        # Render all use cases
        for element in diagram_data.get("elements", []):
            if element.get("type") == "usecase":
                usecase_group = self._render_usecase(dwg, element, diagram_data)
                if usecase_group:
                    main_group.add(usecase_group)
        
        # Render all actors
        for element in diagram_data.get("elements", []):
            if element.get("type") == "actor":
                actor_group = self._render_actor(dwg, element, diagram_data)
                if actor_group:
                    main_group.add(actor_group)
        
        # Render all relationships
        for relationship in diagram_data.get("relationships", []):
            relationship_group = self._render_relationship(dwg, relationship, diagram_data)
            if relationship_group:
                main_group.add(relationship_group)
        
        # Add the main group to the drawing
        dwg.add(main_group)
        
        # Save the drawing
        dwg.save()
        
        return output_path
    
    def _add_usecase_stylesheet(self, dwg: svgwrite.Drawing) -> None:
        """
        Add a CSS stylesheet to the drawing for styling use case diagram elements.
        
        Args:
            dwg: The SVG drawing to add styles to.
        """
        style = dwg.style(content="""
            .actor {
                stroke: #000000;
                stroke-width: 1px;
                fill: #FFFFFF;
            }
            .actor-name {
                font-family: Arial, sans-serif;
                font-size: 14px;
                text-anchor: middle;
            }
            .usecase {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
            .usecase-name {
                font-family: Arial, sans-serif;
                font-size: 14px;
                text-anchor: middle;
            }
            .system {
                fill: #FAFAFA;
                stroke: #666666;
                stroke-width: 1px;
                stroke-dasharray: 4 2;
            }
            .system-name {
                font-family: Arial, sans-serif;
                font-size: 16px;
                text-anchor: middle;
                font-weight: bold;
            }
            .relationship {
                stroke: #000000;
                stroke-width: 1px;
                fill: none;
            }
            .relationship-arrow {
                fill: #000000;
            }
            .relationship-label {
                font-family: Arial, sans-serif;
                font-size: 12px;
                text-anchor: middle;
                fill: #000000;
            }
            .include-extend-label {
                font-family: Arial, sans-serif;
                font-size: 11px;
                text-anchor: middle;
                fill: #000000;
                font-style: italic;
            }
            .generalization-arrow {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
        """)
        dwg.defs.add(style)
    
    def _add_usecase_definitions(self, dwg: svgwrite.Drawing) -> None:
        """
        Add symbol definitions to the drawing for reusable elements.
        
        Args:
            dwg: The SVG drawing to add definitions to.
        """
        # Define arrowhead marker for association relationships
        assoc_marker = dwg.marker(
            id="association-arrow",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        assoc_marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", class_="relationship-arrow"))
        dwg.defs.add(assoc_marker)
        
        # Define arrowhead marker for include/extend relationships (dashed)
        inc_ext_marker = dwg.marker(
            id="include-extend-arrow",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        inc_ext_marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", class_="relationship-arrow"))
        dwg.defs.add(inc_ext_marker)
        
        # Define arrowhead marker for generalization relationships (empty triangle)
        gen_marker = dwg.marker(
            id="generalization-arrow",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        gen_marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", class_="generalization-arrow"))
        dwg.defs.add(gen_marker)
        
        # Define actor symbol (stick figure)
        actor_symbol = dwg.symbol(id="actor-symbol")
        # Head
        actor_symbol.add(dwg.circle(center=(25, 15), r=10, class_="actor"))
        # Body
        actor_symbol.add(dwg.line(start=(25, 25), end=(25, 50), class_="actor"))
        # Arms
        actor_symbol.add(dwg.line(start=(10, 35), end=(40, 35), class_="actor"))
        # Legs
        actor_symbol.add(dwg.line(start=(25, 50), end=(10, 75), class_="actor"))
        actor_symbol.add(dwg.line(start=(25, 50), end=(40, 75), class_="actor"))
        
        dwg.defs.add(actor_symbol)
    
    def _preprocess_usecase_diagram(self, diagram_data: Dict[str, Any]) -> None:
        """
        Preprocess the diagram data to compute positions and dimensions.
        
        Args:
            diagram_data: The diagram data as a dictionary.
        """
        # Extract elements by type
        systems = [e for e in diagram_data.get("elements", []) if e.get("type") == "system"]
        usecases = [e for e in diagram_data.get("elements", []) if e.get("type") == "usecase"]
        actors = [e for e in diagram_data.get("elements", []) if e.get("type") == "actor"]
        
        # Create mappings for easier lookup
        system_map = {s.get("id"): s for s in systems}
        usecase_map = {uc.get("id"): uc for uc in usecases}
        actor_map = {a.get("id"): a for a in actors}
        
        # First, place actors on the left side
        actor_x = 50
        actor_y = 100
        
        for actor in actors:
            actor_id = actor.get("id")
            
            self.positions[actor_id] = (actor_x, actor_y)
            
            # Move down for the next actor
            actor_y += self.actor_height + self.element_spacing
            
            # If we're off the bottom of the page, wrap to the right
            if actor_y > self.height - 100:
                actor_y = 100
                actor_x += self.actor_width + self.element_spacing
        
        # Place systems in the center
        system_x = 200
        system_y = 50
        
        for system in systems:
            system_id = system.get("id")
            system_name = system.get("name", "")
            
            # Find all use cases in this system
            system_usecase_ids = system.get("use_cases", [])
            system_usecases = [usecase_map.get(uc_id) for uc_id in system_usecase_ids if uc_id in usecase_map]
            
            # Calculate system dimensions based on the number of use cases
            num_usecases = len(system_usecases)
            
            # Basic sizing calculation
            rows = max(1, int(math.sqrt(num_usecases)))
            cols = math.ceil(num_usecases / rows)
            
            system_width = max(300, cols * (self.usecase_width + self.element_spacing) + self.system_padding * 2)
            system_height = max(200, rows * (self.usecase_height + self.element_spacing) + self.system_padding * 2 + 30)  # Extra for title
            
            self.system_dimensions[system_id] = (system_width, system_height)
            
            # Place the system
            self.positions[system_id] = (system_x, system_y)
            
            # Place use cases within the system
            usecase_x = system_x + self.system_padding
            usecase_y = system_y + self.system_padding + 30  # Allow space for system name
            
            for i, usecase in enumerate(system_usecases):
                usecase_id = usecase.get("id")
                
                # Calculate row and column for grid layout
                row = i // cols
                col = i % cols
                
                # Calculate position
                x = usecase_x + col * (self.usecase_width + self.element_spacing)
                y = usecase_y + row * (self.usecase_height + self.element_spacing)
                
                self.positions[usecase_id] = (x, y)
            
            # Move right for the next system
            system_x += system_width + self.element_spacing
            
            # If we're off the right of the page, wrap down
            if system_x + 300 > self.width:
                system_x = 200
                system_y += system_height + self.element_spacing
        
        # Place any use cases not in a system on the right
        usecase_x = system_x
        usecase_y = 100
        
        for usecase in usecases:
            usecase_id = usecase.get("id")
            
            # Skip if already positioned
            if usecase_id in self.positions:
                continue
            
            self.positions[usecase_id] = (usecase_x, usecase_y)
            
            # Move down for the next use case
            usecase_y += self.usecase_height + self.element_spacing
            
            # If we're off the bottom of the page, wrap to the right
            if usecase_y > self.height - 100:
                usecase_y = 100
                usecase_x += self.usecase_width + self.element_spacing
    
    def _render_actor(self, dwg: svgwrite.Drawing, actor_data: Dict[str, Any],
                     diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render an actor as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            actor_data: The actor data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the actor, or None if the actor can't be rendered.
        """
        actor_id = actor_data.get("id")
        name = actor_data.get("name", "")
        
        # Get position from preprocessed data
        if actor_id not in self.positions:
            return None
        
        x, y = self.positions[actor_id]
        
        # Create a group for the actor
        actor_group = dwg.g(id=f"actor-{actor_id}")
        
        # Use the actor symbol
        actor_fig = dwg.use(href="#actor-symbol", insert=(x, y))
        actor_group.add(actor_fig)
        
        # Add actor name below the figure
        name_text = dwg.text(
            name,
            insert=(x + self.actor_width / 2, y + self.actor_height + 20),
            class_="actor-name"
        )
        actor_group.add(name_text)
        
        return actor_group
    
    def _render_usecase(self, dwg: svgwrite.Drawing, usecase_data: Dict[str, Any],
                      diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a use case as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            usecase_data: The use case data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the use case, or None if the use case can't be rendered.
        """
        usecase_id = usecase_data.get("id")
        name = usecase_data.get("name", "")
        
        # Get position from preprocessed data
        if usecase_id not in self.positions:
            return None
        
        x, y = self.positions[usecase_id]
        
        # Create a group for the use case
        usecase_group = dwg.g(id=f"usecase-{usecase_id}")
        
        # Render the use case as an ellipse
        ellipse = dwg.ellipse(
            center=(x + self.usecase_width / 2, y + self.usecase_height / 2),
            r=(self.usecase_width / 2, self.usecase_height / 2),
            class_="usecase"
        )
        usecase_group.add(ellipse)
        
        # Add use case name in the center
        # Handle multi-line text by splitting on spaces and limiting line length
        words = name.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 20:  # Limit line length
                if len(current_line) > 1:  # Ensure at least one word per line
                    current_line.pop()  # Remove the last word that would make it too long
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(" ".join(current_line))
                    current_line = []
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Render each line of text
        center_x = x + self.usecase_width / 2
        center_y = y + self.usecase_height / 2
        line_height = 18
        start_y = center_y - (len(lines) - 1) * line_height / 2
        
        for i, line in enumerate(lines):
            text = dwg.text(
                line,
                insert=(center_x, start_y + i * line_height),
                class_="usecase-name"
            )
            usecase_group.add(text)
        
        return usecase_group
    
    def _render_system(self, dwg: svgwrite.Drawing, system_data: Dict[str, Any],
                     diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a system boundary as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            system_data: The system data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the system boundary, or None if the system can't be rendered.
        """
        system_id = system_data.get("id")
        name = system_data.get("name", "")
        
        # Get position and dimensions from preprocessed data
        if system_id not in self.positions or system_id not in self.system_dimensions:
            return None
        
        x, y = self.positions[system_id]
        width, height = self.system_dimensions[system_id]
        
        # Create a group for the system
        system_group = dwg.g(id=f"system-{system_id}")
        
        # Render the system as a rectangle
        rect = dwg.rect(
            insert=(x, y),
            size=(width, height),
            rx=10, ry=10,
            class_="system"
        )
        system_group.add(rect)
        
        # Add system name at the top
        name_text = dwg.text(
            name,
            insert=(x + width / 2, y + 20),
            class_="system-name"
        )
        system_group.add(name_text)
        
        return system_group
    
    def _render_relationship(self, dwg: svgwrite.Drawing, relationship_data: Dict[str, Any],
                           diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a relationship as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            relationship_data: The relationship data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the relationship, or None if the relationship can't be rendered.
        """
        source_id = relationship_data.get("source_id")
        target_id = relationship_data.get("target_id")
        relationship_type = relationship_data.get("relationship_type", "association")
        label = relationship_data.get("label", "")
        
        # Get source and target positions
        if source_id not in self.positions or target_id not in self.positions:
            return None
        
        # Create mapping for elements
        elements = {e.get("id"): e for e in diagram_data.get("elements", [])}
        
        source = elements.get(source_id)
        target = elements.get(target_id)
        
        if not source or not target:
            return None
        
        source_type = source.get("type")
        target_type = target.get("type")
        
        # Get element centers and calculate connection points
        source_x, source_y = self.positions[source_id]
        target_x, target_y = self.positions[target_id]
        
        # Adjust centers based on element type
        if source_type == "actor":
            source_center_x = source_x + self.actor_width / 2
            source_center_y = source_y + self.actor_height / 2
        elif source_type == "usecase":
            source_center_x = source_x + self.usecase_width / 2
            source_center_y = source_y + self.usecase_height / 2
        else:  # system or other
            source_center_x = source_x
            source_center_y = source_y
        
        if target_type == "actor":
            target_center_x = target_x + self.actor_width / 2
            target_center_y = target_y + self.actor_height / 2
        elif target_type == "usecase":
            target_center_x = target_x + self.usecase_width / 2
            target_center_y = target_y + self.usecase_height / 2
        else:  # system or other
            target_center_x = target_x
            target_center_y = target_y
        
        # Calculate connection points based on element types
        source_point = self._calculate_connection_point(
            source_center_x, source_center_y, 
            target_center_x, target_center_y,
            source_type, source_id
        )
        
        target_point = self._calculate_connection_point(
            target_center_x, target_center_y, 
            source_center_x, source_center_y,
            target_type, target_id
        )
        
        if not source_point or not target_point:
            return None
        
        # Create a group for the relationship
        relationship_group = dwg.g(id=f"relationship-{source_id}-{target_id}")
        
        # Draw the line based on relationship type
        if relationship_type == "association":
            # Simple straight line for association
            line = dwg.line(
                start=source_point,
                end=target_point,
                class_="relationship",
                marker_end="url(#association-arrow)"
            )
            relationship_group.add(line)
            
        elif relationship_type in ["include", "extend"]:
            # Dashed line for include/extend relationships
            line = dwg.line(
                start=source_point,
                end=target_point,
                class_="relationship",
                stroke_dasharray="4,2",
                marker_end="url(#include-extend-arrow)"
            )
            relationship_group.add(line)
            
            # Add stereotype label
            mid_x = (source_point[0] + target_point[0]) / 2
            mid_y = (source_point[1] + target_point[1]) / 2
            
            # Add a slight offset perpendicular to the line
            angle = math.atan2(target_point[1] - source_point[1], target_point[0] - source_point[0])
            offset_x = -10 * math.sin(angle)
            offset_y = 10 * math.cos(angle)
            
            # Create a small white background for better readability
            text_bg = dwg.rect(
                insert=(mid_x + offset_x - 35, mid_y + offset_y - 12),
                size=(70, 16),
                fill="white",
                stroke="none"
            )
            
            stereotype = "<<include>>" if relationship_type == "include" else "<<extend>>"
            text = dwg.text(
                stereotype,
                insert=(mid_x + offset_x, mid_y + offset_y),
                class_="include-extend-label"
            )
            
            relationship_group.add(text_bg)
            relationship_group.add(text)
            
        elif relationship_type == "generalization":
            # Solid line with empty triangle for generalization
            line = dwg.line(
                start=source_point,
                end=target_point,
                class_="relationship",
                marker_end="url(#generalization-arrow)"
            )
            relationship_group.add(line)
            
        # Add label if present
        if label and relationship_type == "association":
            # Calculate a position for the label (midpoint with slight offset)
            mid_x = (source_point[0] + target_point[0]) / 2
            mid_y = (source_point[1] + target_point[1]) / 2
            
            # Add a slight offset perpendicular to the line
            angle = math.atan2(target_point[1] - source_point[1], target_point[0] - source_point[0])
            offset_x = -10 * math.sin(angle)
            offset_y = 10 * math.cos(angle)
            
            # Create a small white background for better readability
            text_bg = dwg.rect(
                insert=(mid_x + offset_x - 3, mid_y + offset_y - 12),
                size=(len(label) * 6 + 6, 16),
                fill="white",
                stroke="none"
            )
            
            text = dwg.text(
                label,
                insert=(mid_x + offset_x, mid_y + offset_y),
                class_="relationship-label"
            )
            
            relationship_group.add(text_bg)
            relationship_group.add(text)
        
        return relationship_group
    
    def _calculate_connection_point(self, center_x: float, center_y: float,
                                  other_x: float, other_y: float,
                                  element_type: str, element_id: str) -> Tuple[float, float]:
        """
        Calculate the connection point for a relationship.
        
        Args:
            center_x: The x-coordinate of the element's center.
            center_y: The y-coordinate of the element's center.
            other_x: The x-coordinate of the other element's center.
            other_y: The y-coordinate of the other element's center.
            element_type: The type of the element.
            element_id: The ID of the element.
            
        Returns:
            The (x, y) coordinates of the connection point.
        """
        # Calculate the angle between the centers
        angle = math.atan2(other_y - center_y, other_x - center_x)
        
        # Calculate the connection point based on element type
        if element_type == "actor":
            # For actor, use a simple circle approximation
            radius = 40  # Approximate radius to cover the stick figure
            return (
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle)
            )
        
        elif element_type == "usecase":
            # For use case, use the ellipse formula to find the intersection
            a = self.usecase_width / 2  # Semi-major axis (horizontal)
            b = self.usecase_height / 2  # Semi-minor axis (vertical)
            
            # Parametric equation for an ellipse
            # We need to find t such that (x,y) = (center_x + a*cos(t), center_y + b*sin(t))
            # lies on the ray from center to other_point
            
            # Approximate t value based on the angle
            # For an ellipse, this is not exactly the same as the angle, but close enough
            t = angle
            
            # Point on the ellipse
            x = center_x + a * math.cos(t)
            y = center_y + b * math.sin(t)
            
            return (x, y)
        
        elif element_type == "system":
            # For system boundary, use the rectangle formula
            width, height = self.system_dimensions.get(element_id, (300, 200))
            half_width = width / 2
            half_height = height / 2
            
            # Find the intersection of the ray with the rectangle
            if abs(math.cos(angle)) * half_height > abs(math.sin(angle)) * half_width:
                # Intersect with left or right edge
                dx = half_width * (1 if math.cos(angle) > 0 else -1)
                dy = dx * math.tan(angle)
            else:
                # Intersect with top or bottom edge
                dy = half_height * (1 if math.sin(angle) > 0 else -1)
                dx = dy / math.tan(angle) if math.tan(angle) != 0 else 0
            
            return (center_x + dx, center_y + dy)
        
        # Default fallback
        return (center_x, center_y) 