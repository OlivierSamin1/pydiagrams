"""
Renderer for UML State Diagrams using Graphviz layout.

This module provides a specialized renderer for UML State Diagrams
with improved layout using Graphviz algorithms.
"""

import os
import math
from typing import Dict, List, Tuple, Any, Optional
import svgwrite
from svgwrite.container import Group

from pydiagrams.renderers.state_renderer import StateDiagramRenderer
from pydiagrams.layout.graphviz_layout import GraphvizLayoutManager, LayoutEngine


class GraphvizStateDiagramRenderer(StateDiagramRenderer):
    """
    Specialized renderer for UML State Diagrams using Graphviz layout.
    
    This renderer extends the standard state diagram renderer but uses
    Graphviz algorithms for improved layout.
    """
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px",
                 layout_engine: LayoutEngine = LayoutEngine.DOT):
        """
        Initialize the Graphviz-enhanced state diagram renderer.
        
        Args:
            width: The width of the diagram.
            height: The height of the diagram.
            unit: The unit of measurement (e.g., 'px', 'mm', 'cm').
            layout_engine: The Graphviz layout engine to use.
        """
        super().__init__(width, height, unit)
        
        # Create a layout manager
        self.layout_manager = GraphvizLayoutManager(engine=layout_engine)
        
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render a state diagram to an SVG file with improved layout.
        
        Args:
            diagram_data: The diagram data as a dictionary.
            output_path: The path where the rendered diagram will be saved.
            
        Returns:
            The path to the rendered file.
        """
        # Add diagram type for the layout manager
        diagram_data["type"] = "state_diagram"
        
        # Apply Graphviz layout
        diagram_data = self.layout_manager.apply_layout(diagram_data)
        
        # Create the SVG drawing
        dwg = svgwrite.Drawing(
            filename=output_path,
            size=(f"{self.width}{self.unit}", f"{self.height}{self.unit}"),
        )
        
        # Add stylesheet
        self._add_state_stylesheet(dwg)
        
        # Add symbol definitions for reusable elements
        self._add_state_definitions(dwg)
        
        # Create a main group for the diagram
        main_group = dwg.g(id="main")
        
        # Render regions if any (for composite states)
        regions = diagram_data.get("regions", [])
        for region in regions:
            region_group = self._render_region(dwg, region, diagram_data)
            if region_group:
                main_group.add(region_group)
        
        # Render all states
        for state in diagram_data.get("elements", []):
            if state.get("type") == "state":
                state_group = self._render_state_with_position(dwg, state, diagram_data)
                if state_group:
                    main_group.add(state_group)
        
        # Render all transitions
        for transition in diagram_data.get("relationships", []):
            if transition.get("type") == "transition":
                transition_group = self._render_transition_with_points(dwg, transition, diagram_data)
                if transition_group:
                    main_group.add(transition_group)
        
        # Add the main group to the drawing
        dwg.add(main_group)
        
        # Save the drawing
        dwg.save()
        
        return output_path
    
    def _render_state_with_position(self, dwg: svgwrite.Drawing, state_data: Dict[str, Any],
                          diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a state using position information from the layout manager.
        
        Args:
            dwg: The SVG drawing.
            state_data: The state data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the state, or None if the state can't be rendered.
        """
        state_id = state_data.get("id")
        
        # Use position from Graphviz layout
        position = state_data.get("position")
        if not position:
            return None
        
        x = position.get("x", 0)
        y = position.get("y", 0)
        
        # Adjust position to account for state dimensions
        state_type = state_data.get("state_type")
        if state_type in ["initial", "final", "choice", "junction", "shallow_history", 
                          "deep_history", "terminate", "entry_point", "exit_point"]:
            # These are centered on their position
            pass
        else:
            # Regular states need to be adjusted to use the top-left
            # as reference point instead of center
            x -= self.state_width / 2
            y -= self.state_height / 2
        
        # Update the position in the temporary data
        temp_state_data = state_data.copy()
        self.positions[state_id] = (x, y)
        
        # Use the standard rendering method with the updated position
        return self._render_state(dwg, temp_state_data, diagram_data)
    
    def _render_transition_with_points(self, dwg: svgwrite.Drawing, transition_data: Dict[str, Any],
                            diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a transition using control points from the layout manager.
        
        Args:
            dwg: The SVG drawing.
            transition_data: The transition data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the transition, or None if the transition can't be rendered.
        """
        source_id = transition_data.get("source_id")
        target_id = transition_data.get("target_id")
        
        # Check if we have control points from Graphviz
        control_points = transition_data.get("control_points")
        
        if control_points and len(control_points) >= 2:
            # Create a new group for the transition
            transition_group = dwg.g(id=f"transition-{source_id}-{target_id}")
            
            # Convert control points to SVG path
            points = [(p.get("x", 0), p.get("y", 0)) for p in control_points]
            
            # Create a path using the control points
            path_data = f"M{points[0][0]},{points[0][1]}"
            for i in range(1, len(points)):
                path_data += f" L{points[i][0]},{points[i][1]}"
            
            # Create the path
            path = dwg.path(d=path_data, class_="transition")
            transition_group.add(path)
            
            # Add arrowhead at the end
            end_x, end_y = points[-1]
            prev_x, prev_y = points[-2] if len(points) > 1 else points[0]
            
            # Calculate arrowhead angle
            angle = math.atan2(end_y - prev_y, end_x - prev_x)
            
            # Draw arrowhead
            arrow_size = 10
            arrow1_x = end_x - arrow_size * math.cos(angle - math.pi/6)
            arrow1_y = end_y - arrow_size * math.sin(angle - math.pi/6)
            arrow2_x = end_x - arrow_size * math.cos(angle + math.pi/6)
            arrow2_y = end_y - arrow_size * math.sin(angle + math.pi/6)
            
            arrowhead = dwg.polygon(
                points=[(end_x, end_y), (arrow1_x, arrow1_y), (arrow2_x, arrow2_y)],
                class_="transition-arrow"
            )
            transition_group.add(arrowhead)
            
            # Add label if present
            label = transition_data.get("label", "")
            if label:
                # Calculate midpoint of the path for label placement
                mid_idx = len(points) // 2
                mid_x = points[mid_idx][0]
                mid_y = points[mid_idx][1]
                
                # Add a slight offset perpendicular to the path
                if mid_idx > 0:
                    angle = math.atan2(points[mid_idx][1] - points[mid_idx-1][1],
                                      points[mid_idx][0] - points[mid_idx-1][0])
                    offset_x = -15 * math.sin(angle)
                    offset_y = 15 * math.cos(angle)
                else:
                    offset_x = 0
                    offset_y = -15
                
                # Create a small white background for better readability
                text_bg = dwg.rect(
                    insert=(mid_x + offset_x - 5, mid_y + offset_y - 12),
                    size=(len(label) * 6 + 10, 16),
                    fill="white",
                    stroke="none"
                )
                
                text = dwg.text(
                    label,
                    insert=(mid_x + offset_x, mid_y + offset_y),
                    class_="transition-label"
                )
                
                transition_group.add(text_bg)
                transition_group.add(text)
            
            return transition_group
            
        else:
            # Fall back to standard rendering if no control points
            return self._render_transition(dwg, transition_data, diagram_data) 