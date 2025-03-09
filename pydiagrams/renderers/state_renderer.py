"""
Renderer for UML State Diagrams.

This module provides a specialized renderer for UML State Diagrams.
"""

import os
import math
from typing import Dict, List, Tuple, Any, Optional
import svgwrite
from svgwrite.container import Group

from pydiagrams.renderers.svg_renderer import SVGRenderer


class StateDiagramRenderer(SVGRenderer):
    """Specialized renderer for UML State Diagrams."""
    
    def __init__(self, width: int = 800, height: int = 600, unit: str = "px"):
        """
        Initialize the state diagram renderer.
        
        Args:
            width: The width of the diagram.
            height: The height of the diagram.
            unit: The unit of measurement (e.g., 'px', 'mm', 'cm').
        """
        super().__init__(width, height, unit)
        
        # Define default sizes and spacing
        self.state_width = 120
        self.state_height = 80
        self.composite_state_padding = 20
        self.state_spacing = 50
        self.text_padding = 10
        
        # Sizes for pseudostates
        self.initial_state_radius = 10
        self.final_state_outer_radius = 16
        self.final_state_inner_radius = 10
        self.choice_size = 20  # Diamond size
        self.junction_radius = 10
        self.entry_exit_point_radius = 12
        self.terminate_size = 20  # X size
        self.history_radius = 10
        
        # Default positions for layout algorithm
        self.positions = {}
        self.level_counts = {}
        self.composite_dimensions = {}
        
        # Element colors
        self.state_fill = "#FFFFFF"
        self.state_stroke = "#000000"
        self.transition_color = "#000000"
        self.text_color = "#000000"
        self.region_stroke = "#999999"
        self.region_fill = "#FAFAFA"
    
    def render(self, diagram_data: Dict[str, Any], output_path: str) -> str:
        """
        Render a state diagram to an SVG file.
        
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
        self._add_state_stylesheet(dwg)
        
        # Add symbol definitions for reusable elements
        self._add_state_definitions(dwg)
        
        # Preprocess diagram data for layout
        self._preprocess_state_diagram(diagram_data)
        
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
                state_group = self._render_state(dwg, state, diagram_data)
                if state_group:
                    main_group.add(state_group)
        
        # Render all transitions
        for transition in diagram_data.get("relationships", []):
            if transition.get("type") == "transition":
                transition_group = self._render_transition(dwg, transition, diagram_data)
                if transition_group:
                    main_group.add(transition_group)
        
        # Add the main group to the drawing
        dwg.add(main_group)
        
        # Save the drawing
        dwg.save()
        
        return output_path
    
    def _add_state_stylesheet(self, dwg: svgwrite.Drawing) -> None:
        """
        Add a CSS stylesheet to the drawing for styling state diagram elements.
        
        Args:
            dwg: The SVG drawing to add styles to.
        """
        style = dwg.style(content="""
            .state {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
            .composite-state {
                fill: #FAFAFA;
                stroke: #000000;
                stroke-width: 1px;
            }
            .state-name {
                font-family: Arial, sans-serif;
                font-size: 14px;
                text-anchor: middle;
            }
            .state-divider {
                stroke: #000000;
                stroke-width: 1px;
            }
            .activity-label {
                font-family: Arial, sans-serif;
                font-size: 12px;
                text-anchor: start;
            }
            .transition {
                stroke: #000000;
                stroke-width: 1px;
                fill: none;
            }
            .transition-arrow {
                fill: #000000;
            }
            .transition-label {
                font-family: Arial, sans-serif;
                font-size: 12px;
                text-anchor: middle;
                fill: #000000;
            }
            .initial-state {
                fill: #000000;
            }
            .final-state-outer {
                fill: none;
                stroke: #000000;
                stroke-width: 1px;
            }
            .final-state-inner {
                fill: #000000;
            }
            .choice-pseudostate {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
            .junction-pseudostate {
                fill: #000000;
                stroke: none;
            }
            .history-pseudostate {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
            .terminate-pseudostate {
                stroke: #000000;
                stroke-width: 2px;
            }
            .entry-exit-point {
                fill: #FFFFFF;
                stroke: #000000;
                stroke-width: 1px;
            }
            .region {
                fill: #FAFAFA;
                stroke: #999999;
                stroke-width: 1px;
                stroke-dasharray: 4 2;
            }
            .region-name {
                font-family: Arial, sans-serif;
                font-size: 12px;
                font-style: italic;
                text-anchor: start;
            }
        """)
        dwg.defs.add(style)
    
    def _add_state_definitions(self, dwg: svgwrite.Drawing) -> None:
        """
        Add symbol definitions to the drawing for reusable elements.
        
        Args:
            dwg: The SVG drawing to add definitions to.
        """
        # Define arrowhead marker for transitions
        marker = dwg.marker(
            id="arrowhead",
            insert=(10, 5),
            size=(10, 10),
            orient="auto"
        )
        marker.add(dwg.path(d="M0,0 L0,10 L10,5 z", class_="transition-arrow"))
        dwg.defs.add(marker)
    
    def _preprocess_state_diagram(self, diagram_data: Dict[str, Any]) -> None:
        """
        Preprocess the diagram data to compute positions and dimensions.
        
        Args:
            diagram_data: The diagram data as a dictionary.
        """
        # Extract states and transitions
        states = [s for s in diagram_data.get("elements", []) if s.get("type") == "state"]
        transitions = [t for t in diagram_data.get("relationships", []) if t.get("type") == "transition"]
        
        # Create a tree structure for composite states
        root_states = []
        state_map = {}
        
        # First pass: map states by ID and find root states
        for state in states:
            state_id = state.get("id")
            state_map[state_id] = state
            
            # Consider a state as root if it has no parent or parent is not defined
            parent_id = state.get("parent_id")
            if not parent_id:
                root_states.append(state)
        
        # Compute diagram dimensions and positions
        # This is a simple layout where states are positioned horizontally
        # For a real implementation, a more sophisticated layout algorithm would be needed
        x = 50
        y = 50
        
        for i, state in enumerate(states):
            state_type = state.get("state_type")
            state_id = state.get("id")
            
            # Calculate position based on state type
            if state_type == "initial":
                self.positions[state_id] = (x, y)
                x += self.initial_state_radius * 2 + self.state_spacing
            elif state_type == "final":
                self.positions[state_id] = (x, y)
                x += self.final_state_outer_radius * 2 + self.state_spacing
            elif state_type == "choice":
                self.positions[state_id] = (x, y)
                x += self.choice_size + self.state_spacing
            elif state_type == "junction":
                self.positions[state_id] = (x, y)
                x += self.junction_radius * 2 + self.state_spacing
            elif state_type in ["shallow_history", "deep_history"]:
                self.positions[state_id] = (x, y)
                x += self.history_radius * 2 + self.state_spacing
            elif state_type in ["entry_point", "exit_point"]:
                self.positions[state_id] = (x, y)
                x += self.entry_exit_point_radius * 2 + self.state_spacing
            elif state_type == "terminate":
                self.positions[state_id] = (x, y)
                x += self.terminate_size + self.state_spacing
            else:  # Simple or composite state
                # Check if we need to wrap to next line
                if x + self.state_width > self.width - 50:
                    x = 50
                    y += self.state_height + self.state_spacing
                
                self.positions[state_id] = (x, y)
                
                # Advance position
                if state_type == "composite":
                    # Composite states take more space
                    substates = state.get("substates", [])
                    composite_width = max(self.state_width + self.composite_state_padding * 2,
                                        len(substates) * (self.state_width + self.state_spacing))
                    composite_height = self.state_height + self.composite_state_padding * 2
                    
                    if substates:
                        composite_height += self.state_height + self.state_spacing
                    
                    self.composite_dimensions[state_id] = (composite_width, composite_height)
                    x += composite_width + self.state_spacing
                else:
                    x += self.state_width + self.state_spacing
            
            # If we're at the edge, wrap to next line
            if x > self.width - 100:
                x = 50
                y += self.state_height + self.state_spacing
    
    def _render_state(self, dwg: svgwrite.Drawing, state_data: Dict[str, Any],
                     diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a state as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            state_data: The state data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the state, or None if the state can't be rendered.
        """
        state_id = state_data.get("id")
        state_type = state_data.get("state_type")
        name = state_data.get("name", "")
        
        # Get position from preprocessed data
        if state_id not in self.positions:
            return None
        
        x, y = self.positions[state_id]
        
        # Create a group for the state
        state_group = dwg.g(id=f"state-{state_id}")
        
        # Render the state based on its type
        if state_type == "initial":
            # Initial state is a filled circle
            circle = dwg.circle(
                center=(x, y),
                r=self.initial_state_radius,
                class_="initial-state"
            )
            state_group.add(circle)
        
        elif state_type == "final":
            # Final state is a double circle (outer empty, inner filled)
            outer_circle = dwg.circle(
                center=(x, y),
                r=self.final_state_outer_radius,
                class_="final-state-outer"
            )
            inner_circle = dwg.circle(
                center=(x, y),
                r=self.final_state_inner_radius,
                class_="final-state-inner"
            )
            state_group.add(outer_circle)
            state_group.add(inner_circle)
        
        elif state_type == "choice":
            # Choice pseudostate is a diamond
            half_size = self.choice_size / 2
            points = [
                (x, y - half_size),  # top
                (x + half_size, y),  # right
                (x, y + half_size),  # bottom
                (x - half_size, y),  # left
            ]
            diamond = dwg.polygon(points=points, class_="choice-pseudostate")
            state_group.add(diamond)
        
        elif state_type == "junction":
            # Junction pseudostate is a filled circle
            circle = dwg.circle(
                center=(x, y),
                r=self.junction_radius,
                class_="junction-pseudostate"
            )
            state_group.add(circle)
        
        elif state_type in ["shallow_history", "deep_history"]:
            # History pseudostate is a circle with an 'H' or 'H*' inside
            circle = dwg.circle(
                center=(x, y),
                r=self.history_radius,
                class_="history-pseudostate"
            )
            text = dwg.text(
                "H*" if state_type == "deep_history" else "H",
                insert=(x, y + 4),
                class_="state-name"
            )
            state_group.add(circle)
            state_group.add(text)
        
        elif state_type in ["entry_point", "exit_point"]:
            # Entry/exit points are circles on the border of a composite state
            circle = dwg.circle(
                center=(x, y),
                r=self.entry_exit_point_radius,
                class_="entry-exit-point"
            )
            
            if name:
                text = dwg.text(
                    name,
                    insert=(x, y - self.entry_exit_point_radius - 5),
                    class_="state-name"
                )
                state_group.add(text)
            
            state_group.add(circle)
        
        elif state_type == "terminate":
            # Terminate pseudostate is an X
            half_size = self.terminate_size / 2
            line1 = dwg.line(
                start=(x - half_size, y - half_size),
                end=(x + half_size, y + half_size),
                class_="terminate-pseudostate"
            )
            line2 = dwg.line(
                start=(x - half_size, y + half_size),
                end=(x + half_size, y - half_size),
                class_="terminate-pseudostate"
            )
            state_group.add(line1)
            state_group.add(line2)
        
        elif state_type == "composite":
            # Composite state is a rounded rectangle with potentially nested states
            width, height = self.composite_dimensions.get(state_id, (self.state_width + self.composite_state_padding * 2,
                                                                  self.state_height + self.composite_state_padding * 2))
            
            rect = dwg.rect(
                insert=(x, y),
                size=(width, height),
                rx=10, ry=10,
                class_="composite-state"
            )
            
            # State name
            name_text = dwg.text(
                name,
                insert=(x + width / 2, y + 20),
                class_="state-name"
            )
            
            # Divider line below the name
            divider = dwg.line(
                start=(x + 10, y + 30),
                end=(x + width - 10, y + 30),
                class_="state-divider"
            )
            
            state_group.add(rect)
            state_group.add(name_text)
            state_group.add(divider)
            
            # Render internal elements (entry/exit/do activities)
            y_offset = y + 40
            
            entry_activities = state_data.get("entry_activities", [])
            for activity in entry_activities:
                activity_text = dwg.text(
                    f"entry / {activity}",
                    insert=(x + 15, y_offset),
                    class_="activity-label"
                )
                state_group.add(activity_text)
                y_offset += 20
            
            do_activities = state_data.get("do_activities", [])
            for activity in do_activities:
                activity_text = dwg.text(
                    f"do / {activity}",
                    insert=(x + 15, y_offset),
                    class_="activity-label"
                )
                state_group.add(activity_text)
                y_offset += 20
            
            exit_activities = state_data.get("exit_activities", [])
            for activity in exit_activities:
                activity_text = dwg.text(
                    f"exit / {activity}",
                    insert=(x + 15, y_offset),
                    class_="activity-label"
                )
                state_group.add(activity_text)
                y_offset += 20
            
            # Render internal transitions
            internal_transitions = state_data.get("internal_transitions", {})
            for event, action in internal_transitions.items():
                transition_text = dwg.text(
                    f"{event} / {action}",
                    insert=(x + 15, y_offset),
                    class_="activity-label"
                )
                state_group.add(transition_text)
                y_offset += 20
            
            # Render substates
            substates = state_data.get("substates", [])
            if substates:
                # Position substates within the composite state
                substate_x = x + self.composite_state_padding
                substate_y = y_offset + 10
                
                for i, substate in enumerate(substates):
                    # Update the position for this substate
                    self.positions[substate.get("id")] = (substate_x, substate_y)
                    
                    # Render the substate
                    substate_group = self._render_state(dwg, substate, diagram_data)
                    if substate_group:
                        state_group.add(substate_group)
                    
                    # Move to the next position
                    substate_x += self.state_width + self.state_spacing
                    if substate_x + self.state_width > x + width - self.composite_state_padding:
                        substate_x = x + self.composite_state_padding
                        substate_y += self.state_height + self.state_spacing
        
        else:  # Simple state
            # Simple state is a rounded rectangle
            rect = dwg.rect(
                insert=(x, y),
                size=(self.state_width, self.state_height),
                rx=10, ry=10,
                class_="state"
            )
            
            # State name
            name_text = dwg.text(
                name,
                insert=(x + self.state_width / 2, y + 20),
                class_="state-name"
            )
            
            state_group.add(rect)
            state_group.add(name_text)
            
            # If the state has activities or internal transitions, add a divider and list them
            entry_activities = state_data.get("entry_activities", [])
            do_activities = state_data.get("do_activities", [])
            exit_activities = state_data.get("exit_activities", [])
            internal_transitions = state_data.get("internal_transitions", {})
            
            if entry_activities or do_activities or exit_activities or internal_transitions:
                divider = dwg.line(
                    start=(x + 10, y + 30),
                    end=(x + self.state_width - 10, y + 30),
                    class_="state-divider"
                )
                state_group.add(divider)
                
                y_offset = y + 40
                
                # Entry activities
                for activity in entry_activities:
                    activity_text = dwg.text(
                        f"entry / {activity}",
                        insert=(x + 15, y_offset),
                        class_="activity-label"
                    )
                    state_group.add(activity_text)
                    y_offset += 15
                
                # Do activities
                for activity in do_activities:
                    activity_text = dwg.text(
                        f"do / {activity}",
                        insert=(x + 15, y_offset),
                        class_="activity-label"
                    )
                    state_group.add(activity_text)
                    y_offset += 15
                
                # Exit activities
                for activity in exit_activities:
                    activity_text = dwg.text(
                        f"exit / {activity}",
                        insert=(x + 15, y_offset),
                        class_="activity-label"
                    )
                    state_group.add(activity_text)
                    y_offset += 15
                
                # Internal transitions
                for event, action in internal_transitions.items():
                    transition_text = dwg.text(
                        f"{event} / {action}",
                        insert=(x + 15, y_offset),
                        class_="activity-label"
                    )
                    state_group.add(transition_text)
                    y_offset += 15
        
        return state_group
    
    def _render_transition(self, dwg: svgwrite.Drawing, transition_data: Dict[str, Any],
                          diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a transition as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            transition_data: The transition data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the transition, or None if the transition can't be rendered.
        """
        source_id = transition_data.get("source_id")
        target_id = transition_data.get("target_id")
        label = transition_data.get("label", "")
        
        # Get source and target positions
        if source_id not in self.positions or target_id not in self.positions:
            return None
        
        # Create a group for the transition
        transition_group = dwg.g(id=f"transition-{source_id}-{target_id}")
        
        # Get source and target state data
        states = {s.get("id"): s for s in diagram_data.get("elements", []) if s.get("type") == "state"}
        source_state = states.get(source_id)
        target_state = states.get(target_id)
        
        if not source_state or not target_state:
            return None
        
        source_type = source_state.get("state_type")
        target_type = target_state.get("state_type")
        
        source_x, source_y = self.positions[source_id]
        target_x, target_y = self.positions[target_id]
        
        # Calculate connection points based on state types
        start_point = self._calculate_connection_point(source_x, source_y, target_x, target_y, source_type, source_id)
        end_point = self._calculate_connection_point(target_x, target_y, source_x, source_y, target_type, target_id)
        
        if not start_point or not end_point:
            return None
        
        # Create a line for the transition
        # For simplicity, we use a straight line
        # A more sophisticated renderer would use curved paths or orthogonal routing
        line = dwg.line(
            start=start_point,
            end=end_point,
            class_="transition",
            marker_end="url(#arrowhead)"
        )
        transition_group.add(line)
        
        # Add label if present
        if label:
            # Calculate a position for the label (midpoint with slight offset)
            mid_x = (start_point[0] + end_point[0]) / 2
            mid_y = (start_point[1] + end_point[1]) / 2
            
            # Add a slight offset perpendicular to the line
            angle = math.atan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
            offset_x = -10 * math.sin(angle)
            offset_y = 10 * math.cos(angle)
            
            text = dwg.text(
                label,
                insert=(mid_x + offset_x, mid_y + offset_y),
                class_="transition-label"
            )
            
            # Add a small white background for better readability
            text_bg = dwg.rect(
                insert=(mid_x + offset_x - 3, mid_y + offset_y - 12),
                size=(len(label) * 6 + 6, 16),
                fill="white",
                stroke="none"
            )
            
            transition_group.add(text_bg)
            transition_group.add(text)
        
        return transition_group
    
    def _render_region(self, dwg: svgwrite.Drawing, region_data: Dict[str, Any],
                      diagram_data: Dict[str, Any]) -> Optional[Group]:
        """
        Render a region as an SVG group.
        
        Args:
            dwg: The SVG drawing.
            region_data: The region data as a dictionary.
            diagram_data: The complete diagram data.
            
        Returns:
            An SVG group representing the region, or None if the region can't be rendered.
        """
        name = region_data.get("name", "")
        
        # In a real implementation, regions would be positioned within a composite state
        # For this simple example, we just create a placeholder
        region_group = dwg.g(id=f"region-{name}")
        
        # Placeholder rectangle
        rect = dwg.rect(
            insert=(50, 300),
            size=(300, 200),
            class_="region"
        )
        
        # Region name
        if name:
            text = dwg.text(
                name,
                insert=(60, 320),
                class_="region-name"
            )
            region_group.add(text)
        
        region_group.add(rect)
        
        return region_group
    
    def _calculate_connection_point(self, center_x: float, center_y: float,
                                   other_x: float, other_y: float,
                                   state_type: str, state_id: str) -> Tuple[float, float]:
        """
        Calculate the connection point for a transition.
        
        Args:
            center_x: The x-coordinate of the state's center.
            center_y: The y-coordinate of the state's center.
            other_x: The x-coordinate of the other state's center.
            other_y: The y-coordinate of the other state's center.
            state_type: The type of the state.
            state_id: The ID of the state.
            
        Returns:
            The (x, y) coordinates of the connection point.
        """
        # Calculate the angle between the centers
        angle = math.atan2(other_y - center_y, other_x - center_x)
        
        # Calculate the connection point based on state type
        if state_type == "initial":
            # Initial state is a circle
            return (
                center_x + self.initial_state_radius * math.cos(angle),
                center_y + self.initial_state_radius * math.sin(angle)
            )
        
        elif state_type == "final":
            # Final state is a double circle
            return (
                center_x + self.final_state_outer_radius * math.cos(angle),
                center_y + self.final_state_outer_radius * math.sin(angle)
            )
        
        elif state_type == "choice":
            # Choice pseudostate is a diamond
            half_size = self.choice_size / 2
            
            # Find the intersection of the ray with the diamond
            if abs(math.cos(angle)) > abs(math.sin(angle)):
                # Intersect with left or right edge
                dx = half_size * (1 if math.cos(angle) > 0 else -1)
                dy = dx * math.tan(angle)
            else:
                # Intersect with top or bottom edge
                dy = half_size * (1 if math.sin(angle) > 0 else -1)
                dx = dy / math.tan(angle) if math.tan(angle) != 0 else 0
            
            return (center_x + dx, center_y + dy)
        
        elif state_type == "junction":
            # Junction pseudostate is a filled circle
            return (
                center_x + self.junction_radius * math.cos(angle),
                center_y + self.junction_radius * math.sin(angle)
            )
        
        elif state_type in ["shallow_history", "deep_history"]:
            # History pseudostate is a circle
            return (
                center_x + self.history_radius * math.cos(angle),
                center_y + self.history_radius * math.sin(angle)
            )
        
        elif state_type in ["entry_point", "exit_point"]:
            # Entry/exit points are circles
            return (
                center_x + self.entry_exit_point_radius * math.cos(angle),
                center_y + self.entry_exit_point_radius * math.sin(angle)
            )
        
        elif state_type == "terminate":
            # Terminate pseudostate is an X
            half_size = self.terminate_size / 2
            return (
                center_x + half_size * math.cos(angle),
                center_y + half_size * math.sin(angle)
            )
        
        elif state_type == "composite":
            # Composite state is a rectangle
            width, height = self.composite_dimensions.get(state_id, (self.state_width + self.composite_state_padding * 2,
                                                                  self.state_height + self.composite_state_padding * 2))
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
        
        else:  # Simple state is a rectangle
            half_width = self.state_width / 2
            half_height = self.state_height / 2
            
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