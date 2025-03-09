"""
SVG Renderer for PyDiagrams.

This module provides functionality to render diagrams as SVG.
"""

from typing import Dict, Any, Optional
import svgwrite
from abc import ABC, abstractmethod


class SVGRenderer:
    """Renderer for SVG output format."""
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px"):
        """
        Initialize the SVG renderer.
        
        Args:
            width: Canvas width
            height: Canvas height
            unit: Unit for dimensions (px, mm, etc.)
        """
        self.width = width
        self.height = height
        self.unit = unit
        self.padding = 20
        self.include_stylesheet = True
        self.include_defs = True
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render diagram data to SVG file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # Create SVG drawing with a compatible profile
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}"),
            profile="full"  # Use 'full' profile instead of 'tiny'
        )
        
        # Add stylesheet if needed
        if self.include_stylesheet:
            self._add_stylesheet(dwg)
            
        # Add definitions (markers, etc.) if needed
        if self.include_defs:
            self._add_definitions(dwg)
            
        # Create a container group for the diagram
        diagram_group = dwg.g(id="diagram")
        
        # Render elements
        elements_group = dwg.g(id="elements")
        for element_data in diagram_data.get("elements", []):
            element_svg = self._render_element(dwg, element_data)
            if element_svg:
                elements_group.add(element_svg)
                
        # Render relationships
        relationships_group = dwg.g(id="relationships")
        for relationship_data in diagram_data.get("relationships", []):
            relationship_svg = self._render_relationship(dwg, relationship_data, diagram_data)
            if relationship_svg:
                relationships_group.add(relationship_svg)
                
        # Add all groups to the diagram
        diagram_group.add(relationships_group)
        diagram_group.add(elements_group)
        
        # Add the diagram group to the drawing
        dwg.add(diagram_group)
        
        # Save the SVG file
        dwg.save(pretty=True)
        
        return output_path
        
    def _add_stylesheet(self, dwg: svgwrite.Drawing) -> None:
        """
        Add CSS stylesheet to the SVG.
        
        Args:
            dwg: SVG drawing object
        """
        style = """
            .element { fill: #ffffff; stroke: #000000; stroke-width: 1; }
            .relationship { stroke: #000000; stroke-width: 1; }
            .text { font-family: Arial, sans-serif; font-size: 12px; }
            .element-name { font-weight: bold; }
            .element-attribute { font-style: normal; }
            .element-method { font-style: normal; }
            .relationship-label { font-size: 10px; }
        """
        dwg.defs.add(dwg.style(style))
        
    def _add_definitions(self, dwg: svgwrite.Drawing) -> None:
        """
        Add definitions like markers for arrows.
        
        Args:
            dwg: SVG drawing object
        """
        # Define arrow marker for relationships
        marker = dwg.marker(
            id="arrow",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10 L2,5 z", fill="#000000"))
        dwg.defs.add(marker)
        
        # Define inheritance marker (hollow triangle)
        marker = dwg.marker(
            id="inheritance",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10 z", fill="#ffffff", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
        
        # Define aggregation marker (hollow diamond)
        marker = dwg.marker(
            id="aggregation",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,5 L5,0 L10,5 L5,10 z", fill="#ffffff", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
        
        # Define composition marker (filled diamond)
        marker = dwg.marker(
            id="composition",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,5 L5,0 L10,5 L5,10 z", fill="#000000"))
        dwg.defs.add(marker)
        
    def _render_element(self, dwg: svgwrite.Drawing, element_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render a diagram element to SVG.
        
        Args:
            dwg: SVG drawing object
            element_data: Dictionary with element data
            
        Returns:
            SVG group with the rendered element, or None if not supported
        """
        # Get element type and position
        element_type = element_data.get("type", "unknown")
        position = element_data.get("position", {"x": 0, "y": 0})
        element_id = element_data.get("id", "element")
        
        # Create a group for the element
        element_group = dwg.g(id=f"element-{element_id}", class_="element")
        
        # Extract style information
        style_data = element_data.get("style", {})
        fill = style_data.get("fill_color", "#ffffff")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Create a basic rectangle for the element
        # In a real implementation, this would be more sophisticated
        # based on the element type
        width = element_data.get("width", 100)
        height = element_data.get("height", 80)
        
        # Add the main shape based on element type
        if element_type == "class":
            # Draw class box
            element_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, height),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                rx=style_data.get("corner_radius", 0),
                ry=style_data.get("corner_radius", 0)
            ))
            
            # Draw name section
            element_group.add(dwg.line(
                start=(position["x"], position["y"] + 30),
                end=(position["x"] + width, position["y"] + 30),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Add name text
            element_group.add(dwg.text(
                element_data.get("name", "Class"),
                insert=(position["x"] + width/2, position["y"] + 20),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                font_weight="bold",
                text_anchor="middle",
                class_="element-name"
            ))
            
            # Check for attributes section
            if "attributes" in element_data:
                # Draw attributes separator line
                element_group.add(dwg.line(
                    start=(position["x"], position["y"] + 60),
                    end=(position["x"] + width, position["y"] + 60),
                    stroke=stroke,
                    stroke_width=stroke_width
                ))
                
                # Add attributes
                y_pos = position["y"] + 45
                for attr in element_data.get("attributes", []):
                    element_group.add(dwg.text(
                        attr,
                        insert=(position["x"] + 10, y_pos),
                        font_family=style_data.get("font_family", "Arial"),
                        font_size=style_data.get("font_size", 10),
                        class_="element-attribute"
                    ))
                    y_pos += 15
                    
            # Add methods
            if "methods" in element_data:
                y_pos = position["y"] + 75
                for method in element_data.get("methods", []):
                    element_group.add(dwg.text(
                        method,
                        insert=(position["x"] + 10, y_pos),
                        font_family=style_data.get("font_family", "Arial"),
                        font_size=style_data.get("font_size", 10),
                        class_="element-method"
                    ))
                    y_pos += 15
                    
        elif element_type == "usecase":
            # Draw use case ellipse
            element_group.add(dwg.ellipse(
                center=(position["x"] + width/2, position["y"] + height/2),
                r=(width/2, height/2),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Add name text
            element_group.add(dwg.text(
                element_data.get("name", "Use Case"),
                insert=(position["x"] + width/2, position["y"] + height/2),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="element-name"
            ))
            
        elif element_type == "actor":
            # Draw actor symbol (stick figure)
            center_x = position["x"] + width/2
            center_y = position["y"] + 15
            
            # Head
            element_group.add(dwg.circle(
                center=(center_x, center_y),
                r=10,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Body
            element_group.add(dwg.line(
                start=(center_x, center_y + 10),
                end=(center_x, center_y + 35),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Arms
            element_group.add(dwg.line(
                start=(center_x - 15, center_y + 20),
                end=(center_x + 15, center_y + 20),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Legs
            element_group.add(dwg.line(
                start=(center_x, center_y + 35),
                end=(center_x - 10, center_y + 55),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            element_group.add(dwg.line(
                start=(center_x, center_y + 35),
                end=(center_x + 10, center_y + 55),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Add name text
            element_group.add(dwg.text(
                element_data.get("name", "Actor"),
                insert=(center_x, position["y"] + 70),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                class_="element-name"
            ))
            
        else:
            # Generic rectangle for other element types
            element_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, height),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                rx=style_data.get("corner_radius", 0),
                ry=style_data.get("corner_radius", 0)
            ))
            
            # Add name text
            element_group.add(dwg.text(
                element_data.get("name", "Element"),
                insert=(position["x"] + width/2, position["y"] + height/2),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="element-name"
            ))
            
        return element_group
        
    def _render_relationship(self, dwg: svgwrite.Drawing, relationship_data: Dict[str, Any], diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render a relationship to SVG.
        
        Args:
            dwg: SVG drawing object
            relationship_data: Dictionary with relationship data
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered relationship, or None if not supported
        """
        # Create a group for the relationship
        relationship_id = relationship_data.get("id", "relationship")
        relationship_group = dwg.g(id=f"relationship-{relationship_id}", class_="relationship")
        
        # Get source and target elements
        source_id = relationship_data.get("source_id")
        target_id = relationship_data.get("target_id")
        
        # Find source and target positions
        source_position = {"x": 0, "y": 0}
        target_position = {"x": 100, "y": 100}
        
        # In a real implementation, this would look up the actual positions
        # from the elements based on their IDs
        for element in diagram_data.get("elements", []):
            if element.get("id") == source_id:
                source_position = element.get("position", source_position)
                source_width = element.get("width", 100)
                source_height = element.get("height", 80)
            elif element.get("id") == target_id:
                target_position = element.get("position", target_position)
                target_width = element.get("width", 100)
                target_height = element.get("height", 80)
                
        # Calculate connection points
        # In a real implementation, this would be more sophisticated
        source_x = source_position["x"] + 50  # center of element
        source_y = source_position["y"] + 40
        target_x = target_position["x"] + 50
        target_y = target_position["y"] + 40
        
        # Extract style information
        style_data = relationship_data.get("style", {})
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        dash_array = style_data.get("dash_array", None)
        
        # Get relationship type
        relationship_type = relationship_data.get("relationship_type", "default")
        
        # Set marker based on relationship type
        marker_end = None
        if relationship_type == "inheritance":
            marker_end = "url(#inheritance)"
        elif relationship_type == "aggregation":
            marker_end = "url(#aggregation)"
        elif relationship_type == "composition":
            marker_end = "url(#composition)"
        else:
            marker_end = "url(#arrow)"
            
        # Create the path
        path = dwg.path(
            d=f"M{source_x},{source_y} L{target_x},{target_y}",
            fill="none",
            stroke=stroke,
            stroke_width=stroke_width,
            marker_end=marker_end
        )
        
        # Add dash array if specified
        if dash_array:
            path["stroke-dasharray"] = dash_array
            
        relationship_group.add(path)
        
        # Add relationship label if present
        label = relationship_data.get("name")
        if label:
            # Calculate middle point
            mid_x = (source_x + target_x) / 2
            mid_y = (source_y + target_y) / 2
            
            # Add text
            relationship_group.add(dwg.text(
                label,
                insert=(mid_x, mid_y - 5),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 10),
                text_anchor="middle",
                class_="relationship-label",
                fill=style_data.get("text_color", "#000000")
            ))
            
        # Add source label if present
        source_label = relationship_data.get("source_label")
        if source_label:
            # Calculate position near source
            label_x = source_x + (target_x - source_x) * 0.15
            label_y = source_y + (target_y - source_y) * 0.15
            
            # Add text
            relationship_group.add(dwg.text(
                source_label,
                insert=(label_x, label_y - 5),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 10),
                text_anchor="middle",
                class_="relationship-label",
                fill=style_data.get("text_color", "#000000")
            ))
            
        # Add target label if present
        target_label = relationship_data.get("target_label")
        if target_label:
            # Calculate position near target
            label_x = source_x + (target_x - source_x) * 0.85
            label_y = source_y + (target_y - source_y) * 0.85
            
            # Add text
            relationship_group.add(dwg.text(
                target_label,
                insert=(label_x, label_y - 5),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 10),
                text_anchor="middle",
                class_="relationship-label",
                fill=style_data.get("text_color", "#000000")
            ))
            
        return relationship_group 