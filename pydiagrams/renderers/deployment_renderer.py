#!/usr/bin/env python3
"""
Renderer for Deployment Diagrams.

This module provides specialized rendering for Deployment Diagrams,
visualizing nodes, artifacts, and their relationships.
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

from pydiagrams.diagrams.architectural.deployment_diagram import (
    DeploymentDiagram, DeploymentNode, DeploymentArtifact,
    CommunicationPath, Manifest, NodeType, CommunicationType
)
from pydiagrams.renderers.svg_renderer import SVGRenderer


@dataclass
class DeploymentDiagramRenderer(SVGRenderer):
    """
    Specialized renderer for Deployment Diagrams.
    
    This renderer visualizes deployment nodes, artifacts, and their
    relationships in a Deployment Diagram.
    """
    # Default dimensions of the diagram
    width: int = 1000
    height: int = 800
    unit: str = "px"
    
    # Styling properties
    node_width: int = 200
    node_height: int = 150
    node_spacing: int = 50
    artifact_width: int = 120
    artifact_height: int = 60
    text_margin: int = 5
    line_stroke_width: int = 2
    arrow_size: int = 10
    
    # Colors
    node_fill: str = "#E8F0FF"
    node_stroke: str = "#2F4F4F"
    artifact_fill: str = "#F8F8FF"
    artifact_stroke: str = "#696969"
    text_color: str = "#000000"
    path_color: str = "#000000"
    
    def render(self, 
               diagram: DeploymentDiagram, 
               output_path: str, 
               **kwargs) -> str:
        """
        Render a Deployment Diagram to an SVG file.
        
        Args:
            diagram: The DeploymentDiagram object to render
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
        node_group = self.drawing.add(Group(id="nodes"))
        artifact_group = self.drawing.add(Group(id="artifacts"))
        path_group = self.drawing.add(Group(id="paths"))
        
        # Calculate positions for nodes
        positions = self._calculate_positions(diagram)
        
        # Draw nodes and their artifacts
        node_positions = {}
        for node in diagram.nodes:
            pos = positions.get(node.id, (50, 50))
            node_positions[node.id] = pos
            self._render_node(node_group, node, pos)
        
        # Draw communication paths
        for path in diagram.communication_paths:
            source_pos = node_positions.get(path.source_id)
            target_pos = node_positions.get(path.target_id)
            
            if source_pos and target_pos:
                self._render_communication_path(
                    path_group,
                    path,
                    source_pos,
                    target_pos
                )
        
        # Save the SVG
        self.drawing.save()
        return output_path
    
    def _add_defs(self) -> None:
        """Add definitions to the SVG (markers, patterns, etc.)."""
        # Add arrow marker for communication paths
        marker = self.drawing.marker(
            insert=(10, 5),
            size=(10, 10),
            orient="auto",
            id="arrow"
        )
        marker.add(self.drawing.path(
            "M0,0 L10,5 L0,10 L3,5 Z",
            fill=self.path_color
        ))
        self.drawing.defs.add(marker)
    
    def _calculate_positions(self, diagram: DeploymentDiagram) -> Dict[str, Tuple[int, int]]:
        """
        Calculate positions for each node in the diagram.
        
        In a more advanced implementation, this would use a proper layout algorithm.
        For now, we'll use a simple grid layout.
        
        Args:
            diagram: The DeploymentDiagram to calculate positions for
            
        Returns:
            A dictionary mapping node IDs to (x, y) positions
        """
        positions = {}
        rows = int(math.ceil(math.sqrt(len(diagram.nodes))))
        cols = int(math.ceil(len(diagram.nodes) / rows))
        
        for i, node in enumerate(diagram.nodes):
            row = i // cols
            col = i % cols
            
            x = 50 + col * (self.node_width + self.node_spacing)
            y = 50 + row * (self.node_height + self.node_spacing)
            
            positions[node.id] = (x, y)
        
        return positions
    
    def _render_node(self,
                    group: Group,
                    node: DeploymentNode,
                    position: Tuple[int, int]) -> None:
        """
        Render a node at the specified position.
        
        Args:
            group: The SVG group to add the node to
            node: The DeploymentNode object to render
            position: The (x, y) position to place the node
        """
        x, y = position
        
        # Create node cube (3D effect)
        cube_depth = 20
        
        # Front face
        front = Rect(
            insert=(x, y),
            size=(self.node_width, self.node_height),
            fill=self.node_fill,
            stroke=self.node_stroke,
            stroke_width=2
        )
        group.add(front)
        
        # Top face
        top_points = [
            (x, y),
            (x + cube_depth, y - cube_depth),
            (x + self.node_width + cube_depth, y - cube_depth),
            (x + self.node_width, y)
        ]
        top = Polygon(
            points=top_points,
            fill=self.node_fill,
            stroke=self.node_stroke,
            stroke_width=2
        )
        group.add(top)
        
        # Right face
        right_points = [
            (x + self.node_width, y),
            (x + self.node_width + cube_depth, y - cube_depth),
            (x + self.node_width + cube_depth, y + self.node_height - cube_depth),
            (x + self.node_width, y + self.node_height)
        ]
        right = Polygon(
            points=right_points,
            fill=self.node_fill,
            stroke=self.node_stroke,
            stroke_width=2
        )
        group.add(right)
        
        # Add stereotype if present
        text_y = y + 25
        if node.stereotype:
            stereotype_text = Text(
                f"«{node.stereotype}»",
                insert=(x + self.node_width / 2, text_y),
                fill="#696969",
                font_family="Arial, sans-serif",
                font_style="italic",
                text_anchor="middle"
            )
            group.add(stereotype_text)
            text_y += 20
        
        # Node name
        name_text = Text(
            node.name,
            insert=(x + self.node_width / 2, text_y),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Node type indicator
        if node.node_type != NodeType.NODE:
            type_text = Text(
                f"({node.node_type.name.lower()})",
                insert=(x + self.node_width / 2, text_y + 20),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(type_text)
        
        # Render artifacts
        artifact_y = text_y + 40
        for artifact in node.artifacts:
            self._render_artifact(
                group,
                artifact,
                (x + (self.node_width - self.artifact_width) / 2, artifact_y)
            )
            artifact_y += self.artifact_height + 10
    
    def _render_artifact(self,
                        group: Group,
                        artifact: DeploymentArtifact,
                        position: Tuple[int, int]) -> None:
        """
        Render an artifact at the specified position.
        
        Args:
            group: The SVG group to add the artifact to
            artifact: The DeploymentArtifact object to render
            position: The (x, y) position to place the artifact
        """
        x, y = position
        
        # Create the main rectangle
        rect = Rect(
            insert=(x, y),
            size=(self.artifact_width, self.artifact_height),
            fill=self.artifact_fill,
            stroke=self.artifact_stroke,
            stroke_width=1.5
        )
        group.add(rect)
        
        # Create the "dog-ear" effect in the top-right corner
        fold_size = 15
        path_data = f"M {x + self.artifact_width - fold_size} {y} " \
                    f"L {x + self.artifact_width} {y + fold_size} " \
                    f"L {x + self.artifact_width} {y} Z"
        fold = Path(
            d=path_data,
            fill=self.artifact_fill,
            stroke=self.artifact_stroke,
            stroke_width=1.5
        )
        group.add(fold)
        
        # Add line for folded corner
        fold_line = Path(
            d=f"M {x + self.artifact_width - fold_size} {y} " \
              f"L {x + self.artifact_width - fold_size} {y + fold_size} " \
              f"L {x + self.artifact_width} {y + fold_size}",
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
                insert=(x + self.artifact_width / 2, text_y),
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
            insert=(x + self.artifact_width / 2, text_y),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            text_anchor="middle",
            font_weight="bold"
        )
        group.add(name_text)
    
    def _render_communication_path(self,
                                 group: Group,
                                 path: CommunicationPath,
                                 start_pos: Tuple[int, int],
                                 end_pos: Tuple[int, int]) -> None:
        """
        Render a communication path between two nodes.
        
        Args:
            group: The SVG group to add the path to
            path: The CommunicationPath object to render
            start_pos: The (x, y) position of the source node
            end_pos: The (x, y) position of the target node
        """
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Adjust start and end points to node boundaries
        x1 += self.node_width / 2
        y1 += self.node_height / 2
        x2 += self.node_width / 2
        y2 += self.node_height / 2
        
        # Add line with appropriate style
        line = Line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=self.path_color,
            stroke_width=2,
            marker_end="url(#arrow)"
        )
        
        # Add dashed pattern for certain communication types
        if path.communication_type in [CommunicationType.BUS, CommunicationType.CUSTOM]:
            line["stroke-dasharray"] = "5,3"
        
        group.add(line)
        
        # Add path name and protocol if present
        if path.name or path.protocol:
            # Calculate midpoint
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Offset the label perpendicular to the line
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                offset = 15
                nx = -dy / length * offset
                ny = dx / length * offset
                
                if path.name:
                    name_text = Text(
                        path.name,
                        insert=(mid_x + nx, mid_y + ny),
                        fill=self.text_color,
                        font_family="Arial, sans-serif",
                        font_size="12px",
                        text_anchor="middle"
                    )
                    group.add(name_text)
                
                if path.protocol:
                    protocol_text = Text(
                        f"«{path.protocol}»",
                        insert=(mid_x + nx, mid_y + ny - 15),
                        fill="#696969",
                        font_family="Arial, sans-serif",
                        font_style="italic",
                        font_size="10px",
                        text_anchor="middle"
                    )
                    group.add(protocol_text) 