"""
Sequence Diagram Renderer for PyDiagrams.

This module provides specialized rendering for UML Sequence Diagrams.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import svgwrite
import os

from pydiagrams.renderers.svg_renderer import SVGRenderer


class SequenceDiagramRenderer(SVGRenderer):
    """Specialized renderer for UML Sequence Diagrams."""
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px"):
        """
        Initialize the sequence diagram renderer.
        
        Args:
            width: Canvas width
            height: Canvas height
            unit: Unit for dimensions (px, mm, etc.)
        """
        super().__init__(width, height, unit)
        self.min_lifeline_spacing = 150  # Minimum space between lifelines
        self.lifeline_header_height = 40  # Height of lifeline headers
        self.activation_width = 16  # Width of activation rectangles
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render sequence diagram data to SVG file.
        
        Args:
            diagram_data: Dictionary with diagram data
            output_path: File path for output
            
        Returns:
            Path to the rendered file
        """
        # Pre-process diagram data to add sequence-specific layout
        self._preprocess_sequence_diagram(diagram_data)
        
        # Create SVG drawing with a compatible profile
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}"),
            profile="full"
        )
        
        # Add stylesheet for sequence diagram elements
        self._add_sequence_stylesheet(dwg)
        
        # Add sequence-specific definitions
        self._add_sequence_definitions(dwg)
        
        # Create a container group for the diagram
        diagram_group = dwg.g(id="diagram")
        
        # First render fragments (they go in the background)
        fragments_group = dwg.g(id="fragments")
        for element in diagram_data.get("elements", []):
            if element.get("type") == "fragment":
                fragment_svg = self._render_fragment(dwg, element, diagram_data)
                if fragment_svg:
                    fragments_group.add(fragment_svg)
        
        # Then render lifelines
        lifelines_group = dwg.g(id="lifelines")
        lifeline_positions = {}  # Store lifeline center positions for message routing
        
        for element in diagram_data.get("elements", []):
            if element.get("type") == "lifeline":
                lifeline_svg, center_x = self._render_lifeline(dwg, element, diagram_data)
                if lifeline_svg:
                    lifelines_group.add(lifeline_svg)
                    lifeline_positions[element.get("id")] = center_x
        
        # Render activations
        activations_group = dwg.g(id="activations")
        for element in diagram_data.get("elements", []):
            if element.get("type") == "lifeline" and "activations" in element:
                for activation in element.get("activations", []):
                    activation_svg = self._render_activation(
                        dwg, 
                        activation, 
                        element.get("id"), 
                        lifeline_positions,
                        diagram_data
                    )
                    if activation_svg:
                        activations_group.add(activation_svg)
        
        # Render messages
        messages_group = dwg.g(id="messages")
        for relationship in diagram_data.get("relationships", []):
            if relationship.get("type") == "message":
                message_svg = self._render_message(
                    dwg, 
                    relationship, 
                    lifeline_positions,
                    diagram_data
                )
                if message_svg:
                    messages_group.add(message_svg)
        
        # Add all groups to the diagram in the correct order
        diagram_group.add(fragments_group)
        diagram_group.add(lifelines_group)
        diagram_group.add(activations_group)
        diagram_group.add(messages_group)
        
        # Add the diagram group to the drawing
        dwg.add(diagram_group)
        
        # Save the SVG file
        dwg.save(pretty=True)
        
        return output_path
    
    def _add_sequence_stylesheet(self, dwg: svgwrite.Drawing) -> None:
        """
        Add sequence diagram specific styles to the SVG.
        
        Args:
            dwg: SVG drawing object
        """
        # Call the parent method to add base styles
        self._add_stylesheet(dwg)
        
        # Add sequence-specific styles
        style = """
            .lifeline { stroke: #000000; stroke-width: 1; }
            .lifeline-header { fill: #ffffff; stroke: #000000; stroke-width: 1; }
            .lifeline-line { stroke: #000000; stroke-width: 1; stroke-dasharray: 5,5; }
            .activation { fill: #E8E8E8; stroke: #000000; stroke-width: 1; }
            .fragment { fill: #F8F8F8; stroke: #000000; stroke-width: 1; }
            .fragment-label { font-weight: bold; font-size: 12px; }
            .message { stroke: #000000; stroke-width: 1; }
            .message-text { font-size: 11px; }
            .message-arrow-sync { marker-end: url(#arrowSync); }
            .message-arrow-async { marker-end: url(#arrowAsync); }
            .message-arrow-reply { marker-end: url(#arrowReply); stroke-dasharray: 5,5; }
            .message-arrow-create { marker-end: url(#arrowCreate); }
            .message-arrow-destroy { marker-end: url(#arrowDestroy); }
            .actor { fill: #ffffff; stroke: #000000; stroke-width: 1; }
        """
        # Add these styles to the SVG
        dwg.defs.add(dwg.style(style))
    
    def _add_sequence_definitions(self, dwg: svgwrite.Drawing) -> None:
        """
        Add sequence diagram specific definitions (markers, etc.)
        
        Args:
            dwg: SVG drawing object
        """
        # Call the parent method to add base definitions
        self._add_definitions(dwg)
        
        # Add sequence-specific arrow markers
        
        # Synchronous message arrow (filled triangle)
        marker = dwg.marker(
            id="arrowSync",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", fill="#000000"))
        dwg.defs.add(marker)
        
        # Asynchronous message arrow (open triangle)
        marker = dwg.marker(
            id="arrowAsync",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10", fill="none", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
        
        # Reply message arrow (dashed line with open triangle)
        marker = dwg.marker(
            id="arrowReply",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10", fill="none", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
        
        # Create message arrow
        marker = dwg.marker(
            id="arrowCreate",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,5 L0,10", fill="none", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
        
        # Destroy message marker (X)
        marker = dwg.marker(
            id="arrowDestroy",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L10,10 M0,10 L10,0", fill="none", stroke="#000000", stroke_width=1))
        dwg.defs.add(marker)
    
    def _preprocess_sequence_diagram(self, diagram_data: Dict[str, Any]) -> None:
        """
        Preprocess the sequence diagram data to calculate positions and sizes.
        
        Args:
            diagram_data: Dictionary with diagram data
        """
        # Get lifelines and calculate their horizontal spacing
        lifelines = [e for e in diagram_data.get("elements", []) if e.get("type") == "lifeline"]
        
        # Set up the initial positions if they're not set
        if lifelines:
            total_width = len(lifelines) * self.min_lifeline_spacing
            if total_width > self.width:
                self.width = total_width + 100  # Add margin
                
            # Position the lifelines horizontally
            x = 50  # Start at x=50
            max_time = 0
            
            for lifeline in lifelines:
                # Calculate lifeline width based on name length
                name_length = len(lifeline.get("name", ""))
                width = max(100, name_length * 8)  # Minimum 100px, otherwise 8px per character
                
                # Set the position if not set
                if "position" not in lifeline:
                    lifeline["position"] = {"x": x, "y": 50}
                
                # Calculate width if not set
                if "width" not in lifeline:
                    lifeline["width"] = width
                
                # Move x for the next lifeline
                x += width + 50  # Add 50px between lifelines
                
                # Find the max time point (for diagram height calculation)
                for activation in lifeline.get("activations", []):
                    max_time = max(max_time, activation.get("end_time", 0))
            
            # Set diagram dimensions
            diagram_data["width"] = max(self.width, x + 50)
            diagram_data["height"] = max(self.height, max_time + 100)
            
            # Find the longest message time point
            for relationship in diagram_data.get("relationships", []):
                if relationship.get("type") == "message":
                    max_time = max(max_time, relationship.get("time_point", 0))
            
            # Adjust height based on messages
            diagram_data["height"] = max(diagram_data["height"], max_time + 100)
    
    def _render_lifeline(self, dwg: svgwrite.Drawing, lifeline_data: Dict[str, Any], 
                        diagram_data: Dict[str, Any]) -> Tuple[svgwrite.container.Group, float]:
        """
        Render a sequence diagram lifeline.
        
        Args:
            dwg: SVG drawing object
            lifeline_data: Dictionary with lifeline data
            diagram_data: Complete diagram data for reference
            
        Returns:
            Tuple of (SVG group with the rendered lifeline, center x position)
        """
        lifeline_id = lifeline_data.get("id", "lifeline")
        lifeline_group = dwg.g(id=f"lifeline-{lifeline_id}", class_="lifeline")
        
        # Get position and style
        position = lifeline_data.get("position", {"x": 0, "y": 0})
        width = lifeline_data.get("width", 100)
        
        style_data = lifeline_data.get("style", {})
        fill = style_data.get("fill_color", "#ffffff")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Calculate center position for the lifeline
        center_x = position["x"] + width / 2
        
        # Draw the appropriate header based on whether it's an actor or object
        if lifeline_data.get("is_actor", False):
            # Actor drawing (stick figure)
            # Head
            lifeline_group.add(dwg.circle(
                center=(center_x, position["y"] + 15),
                r=10,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                class_="actor"
            ))
            
            # Body and limbs
            lifeline_group.add(dwg.line(
                start=(center_x, position["y"] + 25), 
                end=(center_x, position["y"] + 35),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Arms
            lifeline_group.add(dwg.line(
                start=(center_x - 10, position["y"] + 30), 
                end=(center_x + 10, position["y"] + 30),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Legs
            lifeline_group.add(dwg.line(
                start=(center_x, position["y"] + 35), 
                end=(center_x - 7, position["y"] + 45),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            lifeline_group.add(dwg.line(
                start=(center_x, position["y"] + 35), 
                end=(center_x + 7, position["y"] + 45),
                stroke=stroke,
                stroke_width=stroke_width
            ))
            
            # Add name text below the figure
            lifeline_group.add(dwg.text(
                lifeline_data.get("name", "Actor"),
                insert=(center_x, position["y"] + 60),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 12),
                text_anchor="middle",
                font_weight="bold"
            ))
            
            # The lifeline starts lower for an actor
            lifeline_start_y = position["y"] + 70
        else:
            # Regular object drawing (box)
            # Draw the header box
            lifeline_group.add(dwg.rect(
                insert=(position["x"], position["y"]),
                size=(width, self.lifeline_header_height),
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                rx=4, 
                ry=4,
                class_="lifeline-header"
            ))
            
            # Add stereotype if present
            if lifeline_data.get("stereotype"):
                lifeline_group.add(dwg.text(
                    lifeline_data.get("stereotype", ""),
                    insert=(center_x, position["y"] + 15),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 10),
                    text_anchor="middle",
                    font_style="italic"
                ))
                # Add name text below stereotype
                lifeline_group.add(dwg.text(
                    lifeline_data.get("name", "Object"),
                    insert=(center_x, position["y"] + 30),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 12),
                    text_anchor="middle",
                    font_weight="bold"
                ))
            else:
                # Add name text centered in the box
                lifeline_group.add(dwg.text(
                    lifeline_data.get("name", "Object"),
                    insert=(center_x, position["y"] + 25),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 12),
                    text_anchor="middle",
                    font_weight="bold"
                ))
            
            # The lifeline starts immediately below the header
            lifeline_start_y = position["y"] + self.lifeline_header_height
        
        # Calculate the height of the diagram
        diagram_height = diagram_data.get("height", self.height)
        
        # Draw the dashed lifeline
        lifeline_group.add(dwg.line(
            start=(center_x, lifeline_start_y),
            end=(center_x, diagram_height - 50),
            stroke=stroke,
            stroke_width=stroke_width,
            stroke_dasharray="5,5",
            class_="lifeline-line"
        ))
        
        return lifeline_group, center_x
    
    def _render_activation(self, dwg: svgwrite.Drawing, activation_data: Dict[str, Any], 
                          lifeline_id: str, lifeline_positions: Dict[str, float],
                          diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render an activation box on a lifeline.
        
        Args:
            dwg: SVG drawing object
            activation_data: Dictionary with activation data
            lifeline_id: ID of the lifeline this activation belongs to
            lifeline_positions: Dictionary of lifeline center x positions
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered activation
        """
        if lifeline_id not in lifeline_positions:
            return None
        
        activation_id = activation_data.get("id", "activation")
        activation_group = dwg.g(id=f"activation-{activation_id}", class_="activation")
        
        # Get the lifeline center x position
        center_x = lifeline_positions[lifeline_id]
        
        # Get activation times
        start_time = activation_data.get("start_time", 100)
        end_time = activation_data.get("end_time", 150)
        
        # Get style information
        style_data = activation_data.get("style", {})
        fill = style_data.get("fill_color", "#E8E8E8")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Draw the activation rectangle
        half_width = self.activation_width / 2
        activation_group.add(dwg.rect(
            insert=(center_x - half_width, start_time),
            size=(self.activation_width, end_time - start_time),
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            class_="activation"
        ))
        
        # Draw nested activations if any
        for nested in activation_data.get("nested_activations", []):
            nested_svg = self._render_activation(
                dwg, 
                nested, 
                lifeline_id, 
                lifeline_positions,
                diagram_data
            )
            if nested_svg:
                activation_group.add(nested_svg)
        
        return activation_group
    
    def _render_message(self, dwg: svgwrite.Drawing, message_data: Dict[str, Any],
                       lifeline_positions: Dict[str, float],
                       diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render a message between lifelines.
        
        Args:
            dwg: SVG drawing object
            message_data: Dictionary with message data
            lifeline_positions: Dictionary of lifeline center x positions
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered message
        """
        # Get source and target element IDs
        source_id = message_data.get("source_id")
        target_id = message_data.get("target_id")
        
        # Ensure we have positions for both source and target
        if source_id not in lifeline_positions or target_id not in lifeline_positions:
            return None
            
        message_id = message_data.get("id", "message")
        message_group = dwg.g(id=f"message-{message_id}", class_="message")
        
        # Get source and target x positions
        source_x = lifeline_positions[source_id]
        target_x = lifeline_positions[target_id]
        
        # Get message time point (y position)
        time_point = message_data.get("time_point", 100)
        
        # Get style information
        style_data = message_data.get("style", {})
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Get message type
        message_type = message_data.get("message_type", "synchronous")
        
        # Determine arrow class based on message type
        arrow_class = f"message-arrow-{message_type}"
        
        # Self-message needs a different path
        if source_id == target_id:
            # For self-messages, create a looping path
            # Create a path with two right angles
            path_data = f"M{source_x},{time_point} " + \
                       f"h20 v20 h-20"
            
            path = dwg.path(
                d=path_data,
                fill="none",
                stroke=stroke,
                stroke_width=stroke_width,
                class_=arrow_class
            )
            message_group.add(path)
            
            # Add message text
            message_text = message_data.get("name", "")
            if message_text:
                message_group.add(dwg.text(
                    message_text,
                    insert=(source_x + 25, time_point - 5),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 11),
                    text_anchor="start",
                    class_="message-text"
                ))
        else:
            # Regular message between two lifelines
            path = dwg.line(
                start=(source_x, time_point),
                end=(target_x, time_point),
                stroke=stroke,
                stroke_width=stroke_width,
                class_=arrow_class
            )
            
            # Set appropriate markers based on message type
            if message_type == "reply":
                path["stroke-dasharray"] = "5,5"
                
            message_group.add(path)
            
            # Add message text
            message_text = message_data.get("name", "")
            if message_text:
                # Determine text position and anchor based on direction
                if source_x < target_x:
                    # Left to right
                    text_x = source_x + (target_x - source_x) / 2
                    text_anchor = "middle"
                else:
                    # Right to left
                    text_x = target_x + (source_x - target_x) / 2
                    text_anchor = "middle"
                
                message_group.add(dwg.text(
                    message_text,
                    insert=(text_x, time_point - 5),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 11),
                    text_anchor=text_anchor,
                    class_="message-text"
                ))
        
        return message_group
    
    def _render_fragment(self, dwg: svgwrite.Drawing, fragment_data: Dict[str, Any],
                        diagram_data: Dict[str, Any]) -> Optional[svgwrite.container.Group]:
        """
        Render a combined fragment (loop, alt, etc.).
        
        Args:
            dwg: SVG drawing object
            fragment_data: Dictionary with fragment data
            diagram_data: Complete diagram data for reference
            
        Returns:
            SVG group with the rendered fragment
        """
        fragment_id = fragment_data.get("id", "fragment")
        fragment_group = dwg.g(id=f"fragment-{fragment_id}", class_="fragment")
        
        # Get fragment properties
        start_time = fragment_data.get("start_time", 100)
        end_time = fragment_data.get("end_time", 200)
        fragment_type = fragment_data.get("fragment_type", "loop")
        condition = fragment_data.get("condition", "")
        
        # Determine the width of the fragment based on all lifelines it spans
        # In a real implementation, this would be more sophisticated
        # For now, we'll just make it span the whole diagram
        left = 30
        right = diagram_data.get("width", self.width) - 30
        
        # Get style information
        style_data = fragment_data.get("style", {})
        fill = style_data.get("fill_color", "#F8F8F8")
        stroke = style_data.get("stroke_color", "#000000")
        stroke_width = style_data.get("stroke_width", 1)
        
        # Draw the outer rectangle
        fragment_group.add(dwg.rect(
            insert=(left, start_time),
            size=(right - left, end_time - start_time),
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            fill_opacity=0.3,
            class_="fragment"
        ))
        
        # Draw the fragment type label area
        label_width = len(fragment_type) * 8 + 16
        fragment_group.add(dwg.rect(
            insert=(left, start_time),
            size=(label_width, 20),
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            class_="fragment"
        ))
        
        # Add the fragment type label
        fragment_group.add(dwg.text(
            fragment_type.upper(),
            insert=(left + 8, start_time + 15),
            font_family=style_data.get("font_family", "Arial"),
            font_size=style_data.get("font_size", 12),
            font_weight="bold",
            class_="fragment-label"
        ))
        
        # Add the condition if present
        if condition:
            fragment_group.add(dwg.text(
                f"[{condition}]",
                insert=(left + label_width + 5, start_time + 15),
                font_family=style_data.get("font_family", "Arial"),
                font_size=style_data.get("font_size", 11),
                font_style="italic",
                class_="message-text"
            ))
        
        # Add separators for operands
        for condition, separator_time in fragment_data.get("operands", []):
            # Draw the separator line
            fragment_group.add(dwg.line(
                start=(left, separator_time),
                end=(right, separator_time),
                stroke=stroke,
                stroke_width=stroke_width,
                stroke_dasharray="3,3"
            ))
            
            # Add the condition label
            if condition:
                fragment_group.add(dwg.text(
                    f"[{condition}]",
                    insert=(left + 10, separator_time + 15),
                    font_family=style_data.get("font_family", "Arial"),
                    font_size=style_data.get("font_size", 11),
                    font_style="italic",
                    class_="message-text"
                ))
        
        return fragment_group 