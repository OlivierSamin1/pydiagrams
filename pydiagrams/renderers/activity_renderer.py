"""
Activity Diagram Renderer for PyDiagrams.

This module provides specialized rendering for UML Activity Diagrams.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import svgwrite
import os
import math

from pydiagrams.renderers.svg_renderer import SVGRenderer


class ActivityDiagramRenderer(SVGRenderer):
    """Specialized renderer for UML Activity Diagrams."""
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px"):
        """
        Initialize the activity diagram renderer.
        
        Args:
            width: Canvas width
            height: Canvas height
            unit: Unit for dimensions (px, mm, etc.)
        """
        super().__init__(width, height, unit)
        self.node_spacing = 80  # Spacing between nodes
        self.swimlane_padding = 20  # Padding inside swimlanes
        self.node_sizes = {
            "action": (120, 60),
            "initial": (20, 20),
            "final": (30, 30),
            "activity_final": (30, 30),
            "decision": (40, 40),
            "merge": (40, 40),
            "fork": (10, 80),
            "join": (10, 80),
            "object": (120, 60),
            "send_signal": (120, 60),
            "receive_signal": (120, 60),
            "time_event": (60, 40),
            "accept_event": (60, 40)
        }
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render activity diagram data to SVG file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # Pre-process diagram data to add activity-specific layout
        self._preprocess_activity_diagram(diagram_data)
        
        # Create SVG drawing with a compatible profile
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}"),
            profile="full"
        )
        
        # Add stylesheet for activity diagram elements
        self._add_activity_stylesheet(dwg)
        
        # Add activity-specific definitions
        self._add_activity_definitions(dwg)
        
        # Create a container group for the diagram
        diagram_group = dwg.g(id="diagram")
        
        # First render swimlanes (they go in the background)
        swimlanes_group = dwg.g(id="swimlanes")
        for element in diagram_data.get("elements", []):
            if element.get("type") == "swimlane":
                swimlane_svg = self._render_swimlane(dwg, element, diagram_data)
                if swimlane_svg:
                    swimlanes_group.add(swimlane_svg)
        
        # Then render edges (they go below nodes)
        edges_group = dwg.g(id="edges")
        for relationship in diagram_data.get("relationships", []):
            if relationship.get("type") == "activity_edge":
                edge_svg = self._render_edge(dwg, relationship, diagram_data)
                if edge_svg:
                    edges_group.add(edge_svg)
        
        # Finally render nodes
        nodes_group = dwg.g(id="nodes")
        for element in diagram_data.get("elements", []):
            if element.get("type") == "activity_node":
                node_svg = self._render_node(dwg, element, diagram_data)
                if node_svg:
                    nodes_group.add(node_svg)
        
        # Add all groups to the diagram in the correct order
        diagram_group.add(swimlanes_group)
        diagram_group.add(edges_group)
        diagram_group.add(nodes_group)
        
        # Add the diagram group to the drawing
        dwg.add(diagram_group)
        
        # Save the SVG file
        dwg.save(pretty=True)
        
        return output_path
    
    def _add_activity_stylesheet(self, dwg: svgwrite.Drawing) -> None:
        """
        Add activity diagram specific styles to the SVG.
        
        Args:
            dwg: SVG drawing object
        """
        # Call the parent method to add base styles
        self._add_stylesheet(dwg)
        
        # Add activity-specific styles
        style = """
            .activity-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .action-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; rx: 8; ry: 8; }
            .initial-node { fill: #000000; stroke: #000000; stroke-width: 1; }
            .final-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .activity-final-inner { fill: #000000; stroke: none; }
            .decision-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .merge-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .fork-node { fill: #000000; stroke: #000000; stroke-width: 1; }
            .join-node { fill: #000000; stroke: #000000; stroke-width: 1; }
            .object-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .signal-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .time-event-node { fill: #FFFFFF; stroke: #000000; stroke-width: 1.5; }
            .swimlane { fill: #F8F8F8; stroke: #000000; stroke-width: 1; fill-opacity: 0.3; }
            .swimlane-label { font-weight: bold; font-size: 14px; }
            .node-label { font-size: 12px; text-anchor: middle; }
            .edge { stroke: #000000; stroke-width: 1.5; fill: none; marker-end: url(#arrow); }
            .edge-label { font-size: 12px; text-anchor: middle; }
            .guard { font-size: 11px; font-style: italic; }
        """
        # Add these styles to the SVG
        dwg.defs.add(dwg.style(style))
    
    def _add_activity_definitions(self, dwg: svgwrite.Drawing) -> None:
        """
        Add activity diagram specific definitions (markers, etc.)
        
        Args:
            dwg: SVG drawing object
        """
        # Call the parent method to add base definitions
        self._add_definitions(dwg)
        
        # Create a special marker for activity flow arrows
        marker = dwg.marker(
            id="activityArrow",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10 L3,5 z", fill="#000000"))
        dwg.defs.add(marker)
        
    def _preprocess_activity_diagram(self, diagram_data: Dict[str, Any]) -> None:
        """
        Preprocess the activity diagram data to calculate positions and sizes.
        
        Args:
            diagram_data: Dictionary with diagram data
        """
        # For now, we assume the layout algorithm has already assigned positions
        # to each node. If not, we could implement a simple layout algorithm here.
        
        # Set diagram dimensions based on nodes
        max_x = 0
        max_y = 0
        min_x = float('inf')
        min_y = float('inf')
        
        # Find the extents of the diagram
        for element in diagram_data.get("elements", []):
            if "position" in element:
                position = element.get("position", {"x": 0, "y": 0})
                x, y = position.get("x", 0), position.get("y", 0)
                
                # Get size based on node type
                if element.get("type") == "activity_node":
                    node_type = element.get("node_type", "action")
                    width, height = self.node_sizes.get(node_type, (100, 50))
                else:
                    width, height = 120, 60  # Default size
                
                max_x = max(max_x, x + width + 50)  # Add margin
                max_y = max(max_y, y + height + 50)  # Add margin
                min_x = min(min_x, x - 50)  # Add margin
                min_y = min(min_y, y - 50)  # Add margin
        
        # Set diagram dimensions
        if min_x != float('inf'):
            self.width = max(self.width, max_x - min_x)
            self.height = max(self.height, max_y - min_y)
            
        diagram_data["width"] = self.width
        diagram_data["height"] = self.height
    
    def _render_node(self, dwg: svgwrite.Drawing, node_data: Dict[str, Any], 
                    diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render an activity node to SVG.
        
        Args:
            dwg: SVG drawing object
            node_data: Dictionary with node data
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered node
        """
        node_id = node_data.get("id", "node")
        node_group = dwg.g(id=f"node-{node_id}", class_="activity-node")
        
        # Get node properties
        node_type = node_data.get("node_type", "action")
        position = node_data.get("position", {"x": 0, "y": 0})
        name = node_data.get("name", "")
        
        # Get style information
        style_data = node_data.get("style", {})
        fill = style_data.get("fill_color", "#FFFFFF")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1.5)
        
        # Get size based on node type
        width, height = self.node_sizes.get(node_type, (120, 60))
        
        # Render based on node type
        if node_type == "action":
            # Action nodes are rounded rectangles
            node_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, height),
                rx=8, ry=8,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="action-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(position["x"] + width/2, position["y"] + height/2),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="node-label"
            ))
            
        elif node_type == "initial":
            # Initial nodes are solid circles
            node_group.add(dwg.circle(
                center=(position["x"] + width/2, position["y"] + height/2),
                r=width/2,
                fill="#000000",
                class_="initial-node"
            ))
            
        elif node_type == "final" or node_type == "activity_final":
            # Activity final nodes are a circle with a solid circle inside
            # Outer circle
            node_group.add(dwg.circle(
                center=(position["x"] + width/2, position["y"] + height/2),
                r=width/2,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="final-node"
            ))
            
            # Inner circle for activity final
            if node_type == "activity_final":
                node_group.add(dwg.circle(
                    center=(position["x"] + width/2, position["y"] + height/2),
                    r=width/3,
                    fill="#000000",
                    class_="activity-final-inner"
                ))
            
        elif node_type == "decision" or node_type == "merge":
            # Decision/merge nodes are diamonds
            center_x = position["x"] + width/2
            center_y = position["y"] + height/2
            
            diamond_points = [
                (center_x, center_y - height/2),  # Top
                (center_x + width/2, center_y),   # Right
                (center_x, center_y + height/2),  # Bottom
                (center_x - width/2, center_y)    # Left
            ]
            
            node_group.add(dwg.polygon(
                points=diamond_points,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_=f"{node_type}-node"
            ))
            
            # Add the node name if not empty
            if name and name != "Decision" and name != "Merge":
                node_group.add(dwg.text(
                    name,
                    insert=(center_x, center_y - height/2 - 10),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 12),
                    text_anchor="middle",
                    class_="node-label"
                ))
            
        elif node_type == "fork" or node_type == "join":
            # Fork/join nodes are solid bars
            # For horizontal bars (default)
            if width < height:  # This is the vertical bar case
                node_group.add(dwg.rect(
                    insert=(position["x"], position["y"]),
                    size=(width, height),
                    fill="#000000",
                    class_=f"{node_type}-node"
                ))
            else:  # This is the horizontal bar case
                node_group.add(dwg.rect(
                    insert=(position["x"], position["y"]),
                    size=(width, height),
                    fill="#000000",
                    class_=f"{node_type}-node"
                ))
            
        elif node_type == "object":
            # Object nodes are rectangles with the state in brackets
            node_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, height),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="object-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(position["x"] + width/2, position["y"] + height/2 - 10),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                class_="node-label"
            ))
            
            # Add the state if present
            state = node_data.get("state", "")
            if state:
                node_group.add(dwg.text(
                    f"[{state}]",
                    insert=(position["x"] + width/2, position["y"] + height/2 + 10),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 10),
                    font_style="italic",
                    text_anchor="middle",
                    class_="node-label"
                ))
            
        elif node_type == "send_signal":
            # Send signal nodes are convex polygons
            center_x = position["x"] + width/2
            center_y = position["y"] + height/2
            
            # Create a polygon with a point on the right side
            signal_points = [
                (position["x"], position["y"]),                   # Top-left
                (position["x"] + width - 20, position["y"]),      # Top-right before point
                (position["x"] + width, center_y),                # Right point
                (position["x"] + width - 20, position["y"] + height),  # Bottom-right after point
                (position["x"], position["y"] + height)           # Bottom-left
            ]
            
            node_group.add(dwg.polygon(
                points=signal_points,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="signal-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(center_x - 10, center_y),  # Offset to account for the point
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="node-label"
            ))
            
        elif node_type == "receive_signal":
            # Receive signal nodes are concave polygons
            center_x = position["x"] + width/2
            center_y = position["y"] + height/2
            
            # Create a polygon with a point on the left side
            signal_points = [
                (position["x"] + 20, position["y"]),           # Top-left after point
                (position["x"] + width, position["y"]),        # Top-right
                (position["x"] + width, position["y"] + height),  # Bottom-right
                (position["x"] + 20, position["y"] + height),  # Bottom-left after point
                (position["x"], center_y)                      # Left point
            ]
            
            node_group.add(dwg.polygon(
                points=signal_points,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="signal-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(center_x + 10, center_y),  # Offset to account for the point
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="node-label"
            ))
            
        elif node_type == "time_event":
            # Time event nodes are hourglasses
            center_x = position["x"] + width/2
            center_y = position["y"] + height/2
            
            # Create an hourglass shape
            hourglass_points = [
                (center_x - width/3, center_y - height/3),  # Top-left
                (center_x + width/3, center_y - height/3),  # Top-right
                (center_x - width/3, center_y + height/3),  # Bottom-left
                (center_x + width/3, center_y + height/3)   # Bottom-right
            ]
            
            # Draw the hourglass as two triangles
            node_group.add(dwg.polygon(
                points=[hourglass_points[0], hourglass_points[1], hourglass_points[3]],
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="time-event-node"
            ))
            
            node_group.add(dwg.polygon(
                points=[hourglass_points[0], hourglass_points[2], hourglass_points[3]],
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="time-event-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(center_x, position["y"] + height + 15),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                class_="node-label"
            ))
            
        else:
            # For any other node type, use a generic rectangle
            node_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, height),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="activity-node"
            ))
            
            # Add the node name
            node_group.add(dwg.text(
                name,
                insert=(position["x"] + width/2, position["y"] + height/2),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                alignment_baseline="middle",
                class_="node-label"
            ))
            
        return node_group
    
    def _render_edge(self, dwg: svgwrite.Drawing, edge_data: Dict[str, Any],
                    diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render an activity edge to SVG.
        
        Args:
            dwg: SVG drawing object
            edge_data: Dictionary with edge data
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered edge
        """
        edge_id = edge_data.get("id", "edge")
        edge_group = dwg.g(id=f"edge-{edge_id}", class_="edge")
        
        # Get source and target element IDs
        source_id = edge_data.get("source_id")
        target_id = edge_data.get("target_id")
        
        # Find source and target elements
        source_element = None
        target_element = None
        for element in diagram_data.get("elements", []):
            if element.get("id") == source_id:
                source_element = element
            elif element.get("id") == target_id:
                target_element = element
                
        if not source_element or not target_element:
            return None
            
        # Get source and target positions
        source_position = source_element.get("position", {"x": 0, "y": 0})
        target_position = target_element.get("position", {"x": 0, "y": 0})
        
        # Get node types and sizes
        source_type = source_element.get("node_type", "action")
        target_type = target_element.get("node_type", "action")
        source_width, source_height = self.node_sizes.get(source_type, (120, 60))
        target_width, target_height = self.node_sizes.get(target_type, (120, 60))
        
        # Calculate center points
        source_center_x = source_position["x"] + source_width / 2
        source_center_y = source_position["y"] + source_height / 2
        target_center_x = target_position["x"] + target_width / 2
        target_center_y = target_position["y"] + target_height / 2
        
        # Calculate edge start and end points based on node shapes
        start_x, start_y = self._calculate_edge_point(
            source_center_x, source_center_y, 
            target_center_x, target_center_y,
            source_type, source_width, source_height
        )
        
        end_x, end_y = self._calculate_edge_point(
            target_center_x, target_center_y,
            source_center_x, source_center_y,
            target_type, target_width, target_height
        )
        
        # Get style information
        style_data = edge_data.get("style", {})
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1.5)
        
        # Create the path with an arrow at the end
        path = dwg.path(
            d=f"M{start_x},{start_y} L{end_x},{end_y}",
            fill="none",
            stroke=stroke,
            stroke_width=stroke_width,
            marker_end="url(#arrow)",
            class_="edge"
        )
        edge_group.add(path)
        
        # Add guard condition if present
        guard = edge_data.get("guard", "")
        if guard:
            # Calculate a position near the middle of the edge
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Offset the guard text from the edge
            offset_x, offset_y = self._calculate_offset(start_x, start_y, end_x, end_y, 15)
            
            edge_group.add(dwg.text(
                f"[{guard}]",
                insert=(mid_x + offset_x, mid_y + offset_y),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 11),
                font_style="italic",
                text_anchor="middle",
                class_="guard"
            ))
            
        return edge_group
    
    def _render_swimlane(self, dwg: svgwrite.Drawing, swimlane_data: Dict[str, Any],
                        diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render a swimlane to SVG.
        
        Args:
            dwg: SVG drawing object
            swimlane_data: Dictionary with swimlane data
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered swimlane
        """
        swimlane_id = swimlane_data.get("id", "swimlane")
        swimlane_group = dwg.g(id=f"swimlane-{swimlane_id}", class_="swimlane")
        
        # Get swimlane properties
        name = swimlane_data.get("name", "")
        is_horizontal = swimlane_data.get("is_horizontal", True)
        node_ids = swimlane_data.get("node_ids", [])
        
        # Get style information
        style_data = swimlane_data.get("style", {})
        fill = style_data.get("fill_color", "#F8F8F8")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Find the bounding box for all nodes in this swimlane
        left = float('inf')
        top = float('inf')
        right = 0
        bottom = 0
        
        for element in diagram_data.get("elements", []):
            if element.get("id") in node_ids:
                position = element.get("position", {"x": 0, "y": 0})
                x, y = position.get("x", 0), position.get("y", 0)
                
                # Get size based on node type
                if element.get("type") == "activity_node":
                    node_type = element.get("node_type", "action")
                    width, height = self.node_sizes.get(node_type, (120, 60))
                else:
                    width, height = 120, 60  # Default size
                
                left = min(left, x)
                top = min(top, y)
                right = max(right, x + width)
                bottom = max(bottom, y + height)
        
        # Add padding
        left -= self.swimlane_padding
        top -= self.swimlane_padding
        right += self.swimlane_padding
        bottom += self.swimlane_padding
        
        # If no nodes in swimlane, use default size
        if left == float('inf'):
            left, top = 50, 50
            right, bottom = 200, 500 if is_horizontal else 500, 200
        
        # Calculate swimlane dimensions
        width = right - left
        height = bottom - top
        
        # Add more space for the label
        if is_horizontal:
            left -= 20
            width += 40
            top -= 30
            height += 30
        else:
            left -= 80
            width += 80
            top -= 20
            height += 40
        
        # Draw the swimlane rectangle
        swimlane_group.add(dwg.rect(
            insert=(left, top),
            size=(width, height),
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            fill_opacity=0.3,
            class_="swimlane"
        ))
        
        # Add the swimlane label
        if is_horizontal:
            # For horizontal swimlanes, label goes at the top
            swimlane_group.add(dwg.text(
                name,
                insert=(left + width/2, top + 20),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 14),
                font_weight="bold",
                text_anchor="middle",
                class_="swimlane-label"
            ))
        else:
            # For vertical swimlanes, label goes on the left side
            # Create rotated text
            text = dwg.text(
                name,
                insert=(left + 30, top + height/2),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 14),
                font_weight="bold",
                text_anchor="middle",
                class_="swimlane-label"
            )
            text.rotate(-90, (left + 30, top + height/2))
            swimlane_group.add(text)
        
        return swimlane_group
    
    def _calculate_edge_point(self, center_x: float, center_y: float, 
                           other_x: float, other_y: float,
                           node_type: str, width: float, height: float) -> Tuple[float, float]:
        """
        Calculate the point where an edge connects to a node.
        
        Args:
            center_x: Center x coordinate of the node
            center_y: Center y coordinate of the node
            other_x: Center x coordinate of the other node
            other_y: Center y coordinate of the other node
            node_type: Type of the node
            width: Width of the node
            height: Height of the node
            
        Returns:
            Tuple of (x, y) coordinates for the edge connection point
        """
        # Calculate angle between centers
        dx = other_x - center_x
        dy = other_y - center_y
        angle = math.atan2(dy, dx)
        
        # Initialize point at center
        point_x, point_y = center_x, center_y
        
        # Calculate intersection with node shape based on type
        if node_type in ["initial", "final", "activity_final"]:
            # For circular nodes, intersection is at radius in direction of angle
            radius = width / 2
            point_x = center_x + radius * math.cos(angle)
            point_y = center_y + radius * math.sin(angle)
            
        elif node_type in ["decision", "merge"]:
            # For diamond nodes, use simplified intersection
            # This is an approximation, more complex for exact diamond intersection
            half_width = width / 2
            half_height = height / 2
            
            # Different calculation based on the angle
            tan_abs = abs(math.tan(angle)) if math.cos(angle) != 0 else float('inf')
            
            if tan_abs < half_height / half_width:
                # Intersection with left/right side
                point_x = center_x + (half_width if dx > 0 else -half_width)
                point_y = center_y + (half_width * math.tan(angle) if dx > 0 else half_width * -math.tan(angle))
            else:
                # Intersection with top/bottom side
                point_y = center_y + (half_height if dy > 0 else -half_height)
                point_x = center_x + (half_height / math.tan(angle) if dy > 0 else half_height / -math.tan(angle))
            
        elif node_type in ["fork", "join"]:
            # For fork/join nodes (bars), simplified as thin rectangles
            half_width = width / 2
            half_height = height / 2
            
            if width < height:  # Vertical bar
                point_x = center_x
                point_y = center_y + (half_height if dy > 0 else -half_height)
            else:  # Horizontal bar
                point_x = center_x + (half_width if dx > 0 else -half_width)
                point_y = center_y
            
        elif node_type in ["send_signal", "receive_signal"]:
            # For signal nodes, simplified as rectangles
            # In a real implementation, the exact polygon intersection would be calculated
            half_width = width / 2
            half_height = height / 2
            
            if abs(dx) * half_height > abs(dy) * half_width:
                # Intersection with left/right side
                point_x = center_x + (half_width if dx > 0 else -half_width)
                point_y = center_y + tan_abs * (point_x - center_x)
            else:
                # Intersection with top/bottom side
                point_y = center_y + (half_height if dy > 0 else -half_height)
                point_x = center_x + (point_y - center_y) / tan_abs if tan_abs > 0 else center_x
            
        else:
            # For rectangular nodes (action, object, etc.)
            half_width = width / 2
            half_height = height / 2
            
            # Different calculation based on angle
            tan_abs = abs(math.tan(angle)) if math.cos(angle) != 0 else float('inf')
            
            if tan_abs < half_height / half_width:
                # Intersection with left/right side
                point_x = center_x + (half_width if dx > 0 else -half_width)
                point_y = center_y + (tan_abs * half_width * (1 if dy > 0 else -1))
            else:
                # Intersection with top/bottom side
                point_y = center_y + (half_height if dy > 0 else -half_height)
                point_x = center_x + ((half_height / tan_abs) * (1 if dx > 0 else -1))
        
        return point_x, point_y
    
    def _calculate_offset(self, x1: float, y1: float, x2: float, y2: float, distance: float) -> Tuple[float, float]:
        """
        Calculate an offset perpendicular to a line.
        
        Args:
            x1: Start x coordinate
            y1: Start y coordinate
            x2: End x coordinate
            y2: End y coordinate
            distance: Distance to offset
            
        Returns:
            Tuple of (dx, dy) offset values
        """
        # Calculate direction vector
        dx = x2 - x1
        dy = y2 - y1
        
        # Calculate perpendicular vector (rotate 90 degrees)
        length = math.sqrt(dx*dx + dy*dy)
        if length < 0.0001:
            return 0, 0
            
        nx = -dy / length
        ny = dx / length
        
        # Return scaled offset
        return nx * distance, ny * distance 