#!/usr/bin/env python3
"""
Renderer for Network Diagrams.

This module provides specialized rendering for Network Diagrams,
visualizing network devices, connections, and zones.
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

from pydiagrams.diagrams.architectural.network_diagram import (
    NetworkDiagram, NetworkDevice, NetworkConnection, 
    NetworkZone, DeviceType, ConnectionType
)
from pydiagrams.renderers.svg_renderer import SVGRenderer


@dataclass
class NetworkDiagramRenderer(SVGRenderer):
    """
    Specialized renderer for Network Diagrams.
    
    This renderer visualizes network devices, connections, and zones
    in a Network Diagram.
    """
    # Default dimensions of the diagram
    width: int = 1200
    height: int = 900
    unit: str = "px"
    
    # Styling properties
    device_width: int = 120
    device_height: int = 100
    device_spacing: int = 60
    zone_padding: int = 30
    text_margin: int = 5
    line_stroke_width: int = 2
    arrow_size: int = 8
    
    # Colors
    device_fill: Dict[DeviceType, str] = field(default_factory=lambda: {
        DeviceType.ROUTER: "#FFECB3",
        DeviceType.SWITCH: "#C8E6C9",
        DeviceType.FIREWALL: "#FFCDD2",
        DeviceType.SERVER: "#BBDEFB",
        DeviceType.WORKSTATION: "#D1C4E9",
        DeviceType.CLOUD: "#E1F5FE",
        DeviceType.STORAGE: "#F5F5F5",
        DeviceType.LOAD_BALANCER: "#FFE0B2",
        DeviceType.GATEWAY: "#E1BEE7",
        DeviceType.CUSTOM: "#CFD8DC"
    })
    device_stroke: str = "#333333"
    connection_color: Dict[ConnectionType, str] = field(default_factory=lambda: {
        ConnectionType.ETHERNET: "#4CAF50",
        ConnectionType.FIBER: "#2196F3",
        ConnectionType.WIRELESS: "#9C27B0",
        ConnectionType.VPN: "#FF9800",
        ConnectionType.INTERNET: "#607D8B",
        ConnectionType.CUSTOM: "#000000"
    })
    zone_fill: str = "#F5F5F5"
    zone_stroke: str = "#9E9E9E"
    text_color: str = "#212121"
    
    def render(self, 
               diagram: NetworkDiagram, 
               output_path: str, 
               **kwargs) -> str:
        """
        Render a Network Diagram to an SVG file.
        
        Args:
            diagram: The NetworkDiagram object to render
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
        zone_group = self.drawing.add(Group(id="zones"))
        device_group = self.drawing.add(Group(id="devices"))
        connection_group = self.drawing.add(Group(id="connections"))
        label_group = self.drawing.add(Group(id="labels"))
        
        # Calculate positions for devices
        positions = self._calculate_positions(diagram)
        
        # Map zones to their contained devices
        zone_devices = self._map_zones_to_devices(diagram)
        
        # Draw zones first (they'll be in the background)
        zone_bounds = self._calculate_zone_bounds(diagram, positions, zone_devices)
        for zone in diagram.zones:
            if zone.id in zone_bounds:
                self._render_zone(zone_group, zone, zone_bounds[zone.id])
        
        # Draw connections between devices
        connection_labels = {}
        for connection in diagram.connections:
            source_pos = positions.get(connection.source_id)
            target_pos = positions.get(connection.target_id)
            
            if source_pos and target_pos:
                midpoint = self._render_connection(
                    connection_group,
                    connection,
                    source_pos,
                    target_pos
                )
                connection_labels[connection.id] = midpoint
        
        # Draw devices
        for device in diagram.devices:
            pos = positions.get(device.id, (50, 50))
            self._render_device(device_group, device, pos)
        
        # Draw connection labels
        for connection in diagram.connections:
            if connection.id in connection_labels:
                self._render_connection_label(
                    label_group,
                    connection,
                    connection_labels[connection.id]
                )
        
        # Save the SVG
        self.drawing.save()
        return output_path
    
    def _add_defs(self) -> None:
        """Add definitions to the SVG (markers, patterns, etc.)."""
        # Add arrow marker for directed connections
        marker = self.drawing.marker(
            insert=(10, 5),
            size=(10, 10),
            orient="auto",
            id="arrow"
        )
        marker.add(self.drawing.path(
            "M0,0 L10,5 L0,10 L3,5 Z",
            fill="#000000"
        ))
        self.drawing.defs.add(marker)
        
        # Add device icons as symbols
        self._add_device_symbols()
    
    def _add_device_symbols(self) -> None:
        """Add symbols for different device types."""
        # Router symbol
        router = self.drawing.symbol(id="router", viewBox="0 0 60 60")
        router.add(self.drawing.rect(
            insert=(5, 10),
            size=(50, 30),
            rx=2, ry=2,
            fill="#FFECB3",
            stroke="#333333",
            stroke_width=2
        ))
        for i in range(1, 4):
            router.add(self.drawing.circle(
                center=(15 * i, 45),
                r=3,
                fill="#333333"
            ))
        self.drawing.defs.add(router)
        
        # Switch symbol
        switch = self.drawing.symbol(id="switch", viewBox="0 0 60 60")
        switch.add(self.drawing.rect(
            insert=(5, 20),
            size=(50, 20),
            rx=2, ry=2,
            fill="#C8E6C9",
            stroke="#333333",
            stroke_width=2
        ))
        for i in range(1, 6):
            switch.add(self.drawing.line(
                start=(5 + 10 * i, 20),
                end=(5 + 10 * i, 40),
                stroke="#333333",
                stroke_width=1
            ))
        self.drawing.defs.add(switch)
        
        # Firewall symbol
        firewall = self.drawing.symbol(id="firewall", viewBox="0 0 60 60")
        firewall.add(self.drawing.rect(
            insert=(10, 10),
            size=(40, 40),
            fill="#FFCDD2",
            stroke="#333333",
            stroke_width=2
        ))
        firewall.add(self.drawing.path(
            d="M10,10 L50,50 M10,50 L50,10",
            fill="none",
            stroke="#333333",
            stroke_width=2
        ))
        self.drawing.defs.add(firewall)
        
        # Server symbol
        server = self.drawing.symbol(id="server", viewBox="0 0 60 60")
        server.add(self.drawing.rect(
            insert=(15, 5),
            size=(30, 50),
            fill="#BBDEFB",
            stroke="#333333",
            stroke_width=2
        ))
        for i in range(3):
            y = 15 + i * 15
            server.add(self.drawing.line(
                start=(15, y),
                end=(45, y),
                stroke="#333333",
                stroke_width=1
            ))
        self.drawing.defs.add(server)
        
        # Workstation symbol
        workstation = self.drawing.symbol(id="workstation", viewBox="0 0 60 60")
        workstation.add(self.drawing.rect(
            insert=(5, 30),
            size=(50, 20),
            fill="#D1C4E9",
            stroke="#333333",
            stroke_width=2
        ))
        workstation.add(self.drawing.rect(
            insert=(15, 5),
            size=(30, 25),
            fill="#D1C4E9",
            stroke="#333333",
            stroke_width=2
        ))
        self.drawing.defs.add(workstation)
        
        # Cloud symbol
        cloud = self.drawing.symbol(id="cloud", viewBox="0 0 60 60")
        cloud.add(self.drawing.ellipse(
            center=(30, 30),
            r=(25, 15),
            fill="#E1F5FE",
            stroke="#333333",
            stroke_width=2
        ))
        self.drawing.defs.add(cloud)
    
    def _calculate_positions(self, diagram: NetworkDiagram) -> Dict[str, Tuple[int, int]]:
        """
        Calculate positions for each device in the diagram.
        
        Args:
            diagram: The NetworkDiagram to calculate positions for
            
        Returns:
            A dictionary mapping device IDs to (x, y) positions
        """
        # Use the layout manager to calculate positions
        elements = diagram.devices
        relationships = diagram.connections
        
        positions = diagram.layout.apply(elements, relationships)
        
        # If the layout manager didn't provide positions for all devices,
        # use a simple grid layout as fallback
        if not positions or len(positions) < len(diagram.devices):
            positions = {}
            rows = int(math.ceil(math.sqrt(len(diagram.devices))))
            cols = int(math.ceil(len(diagram.devices) / rows))
            
            for i, device in enumerate(diagram.devices):
                row = i // cols
                col = i % cols
                
                x = 100 + col * (self.device_width + self.device_spacing)
                y = 100 + row * (self.device_height + self.device_spacing)
                
                positions[device.id] = (x, y)
        
        return positions
    
    def _map_zones_to_devices(self, diagram: NetworkDiagram) -> Dict[str, List[str]]:
        """
        Create a mapping from zone IDs to lists of device IDs.
        
        Args:
            diagram: The NetworkDiagram to process
            
        Returns:
            Dictionary mapping zone IDs to lists of device IDs
        """
        zone_devices = {zone.id: [] for zone in diagram.zones}
        
        for device in diagram.devices:
            if device.zone_id and device.zone_id in zone_devices:
                zone_devices[device.zone_id].append(device.id)
        
        return zone_devices
    
    def _calculate_zone_bounds(
        self,
        diagram: NetworkDiagram,
        positions: Dict[str, Tuple[int, int]],
        zone_devices: Dict[str, List[str]]
    ) -> Dict[str, Tuple[int, int, int, int]]:
        """
        Calculate the bounding box for each zone based on contained devices.
        
        Args:
            diagram: The NetworkDiagram to process
            positions: Dictionary mapping device IDs to (x, y) positions
            zone_devices: Dictionary mapping zone IDs to lists of device IDs
            
        Returns:
            Dictionary mapping zone IDs to (x, y, width, height) bounds
        """
        zone_bounds = {}
        
        for zone_id, device_ids in zone_devices.items():
            if not device_ids:
                continue
                
            # Get positions of all devices in this zone
            device_positions = [positions[d_id] for d_id in device_ids if d_id in positions]
            
            if not device_positions:
                continue
                
            # Calculate min/max coordinates
            min_x = min(pos[0] for pos in device_positions) - self.device_width // 2
            min_y = min(pos[1] for pos in device_positions) - self.device_height // 2
            max_x = max(pos[0] for pos in device_positions) + self.device_width // 2
            max_y = max(pos[1] for pos in device_positions) + self.device_height // 2
            
            # Add padding
            min_x -= self.zone_padding
            min_y -= self.zone_padding
            max_x += self.zone_padding
            max_y += self.zone_padding
            
            # Calculate width and height
            width = max_x - min_x
            height = max_y - min_y
            
            zone_bounds[zone_id] = (min_x, min_y, width, height)
        
        return zone_bounds
    
    def _render_device(self,
                      group: Group,
                      device: NetworkDevice,
                      position: Tuple[int, int]) -> None:
        """
        Render a network device at the specified position.
        
        Args:
            group: The SVG group to add the device to
            device: The NetworkDevice object to render
            position: The (x, y) position to place the device
        """
        x, y = position
        
        # Create device group
        device_group = group.add(Group(id=f"device-{device.id}"))
        
        # Determine icon type
        icon_id = "server"  # Default icon
        if device.device_type == DeviceType.ROUTER:
            icon_id = "router"
        elif device.device_type == DeviceType.SWITCH:
            icon_id = "switch"
        elif device.device_type == DeviceType.FIREWALL:
            icon_id = "firewall"
        elif device.device_type == DeviceType.WORKSTATION:
            icon_id = "workstation"
        elif device.device_type == DeviceType.CLOUD:
            icon_id = "cloud"
        
        # Adjust position to center the device
        x -= self.device_width // 2
        y -= self.device_height // 2
        
        # Add device shape or icon
        fill_color = self.device_fill.get(device.device_type, "#CFD8DC")
        
        # Draw the device as a rectangle with icon symbol
        rect = Rect(
            insert=(x, y),
            size=(self.device_width, self.device_height),
            rx=5, ry=5,
            fill=fill_color,
            stroke=self.device_stroke,
            stroke_width=2
        )
        device_group.add(rect)
        
        # Add device name
        name_text = Text(
            device.name,
            insert=(x + self.device_width // 2, y + self.device_height + 15),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            font_size="12px",
            text_anchor="middle",
            font_weight="bold"
        )
        device_group.add(name_text)
        
        # Add IP address if present
        if device.ip_address:
            ip_text = Text(
                device.ip_address,
                insert=(x + self.device_width // 2, y + self.device_height + 30),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            device_group.add(ip_text)
        
        # Add device type label
        type_text = Text(
            device.device_type.name,
            insert=(x + self.device_width // 2, y + self.device_height // 2),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            font_size="12px",
            text_anchor="middle",
            font_weight="bold"
        )
        device_group.add(type_text)
    
    def _render_connection(self,
                          group: Group,
                          connection: NetworkConnection,
                          start_pos: Tuple[int, int],
                          end_pos: Tuple[int, int]) -> Tuple[float, float]:
        """
        Render a connection between two devices.
        
        Args:
            group: The SVG group to add the connection to
            connection: The NetworkConnection object to render
            start_pos: The (x, y) position of the source device
            end_pos: The (x, y) position of the target device
            
        Returns:
            The (x, y) midpoint of the connection for label placement
        """
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Calculate the midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Determine line style based on connection type
        stroke_color = self.connection_color.get(connection.connection_type, "#000000")
        
        # Create the connection line
        line = Line(
            start=(x1, y1),
            end=(x2, y2),
            stroke=stroke_color,
            stroke_width=self.line_stroke_width
        )
        
        # Add arrowhead for unidirectional connections
        if not connection.is_bidirectional:
            line["marker-end"] = "url(#arrow)"
        
        # Add dashing for certain connection types
        if connection.connection_type == ConnectionType.WIRELESS:
            line["stroke-dasharray"] = "5,3"
        elif connection.connection_type == ConnectionType.VPN:
            line["stroke-dasharray"] = "10,5"
        
        group.add(line)
        
        return (mid_x, mid_y)
    
    def _render_connection_label(self,
                               group: Group,
                               connection: NetworkConnection,
                               position: Tuple[float, float]) -> None:
        """
        Render a label for a connection.
        
        Args:
            group: The SVG group to add the label to
            connection: The NetworkConnection object
            position: The (x, y) position for the label
        """
        x, y = position
        
        # Create background for the label
        if connection.bandwidth or connection.protocol:
            label_bg = Rect(
                insert=(x - 40, y - 10),
                size=(80, 20),
                rx=5, ry=5,
                fill="white",
                fill_opacity=0.7,
                stroke="none"
            )
            group.add(label_bg)
        
        # Add bandwidth label if present
        if connection.bandwidth:
            bandwidth_text = Text(
                connection.bandwidth,
                insert=(x, y),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle"
            )
            group.add(bandwidth_text)
        
        # Add protocol label if present
        if connection.protocol:
            protocol_text = Text(
                connection.protocol,
                insert=(x, y - 15 if connection.bandwidth else y),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="10px",
                text_anchor="middle",
                font_style="italic"
            )
            group.add(protocol_text)
    
    def _render_zone(self,
                    group: Group,
                    zone: NetworkZone,
                    bounds: Tuple[int, int, int, int]) -> None:
        """
        Render a network zone.
        
        Args:
            group: The SVG group to add the zone to
            zone: The NetworkZone object to render
            bounds: The (x, y, width, height) bounds of the zone
        """
        x, y, width, height = bounds
        
        # Create zone rectangle
        rect = Rect(
            insert=(x, y),
            size=(width, height),
            rx=15, ry=15,
            fill=self.zone_fill,
            fill_opacity=0.3,
            stroke=self.zone_stroke,
            stroke_width=2,
            stroke_dasharray="5,5"
        )
        group.add(rect)
        
        # Add zone name
        name_text = Text(
            zone.name,
            insert=(x + 20, y + 25),
            fill=self.text_color,
            font_family="Arial, sans-serif",
            font_size="14px",
            font_weight="bold"
        )
        group.add(name_text)
        
        # Add zone type if present
        if zone.zone_type:
            type_text = Text(
                f"({zone.zone_type})",
                insert=(x + 20, y + 45),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="12px",
                font_style="italic"
            )
            group.add(type_text)
        
        # Add CIDR if present
        if zone.cidr:
            cidr_text = Text(
                zone.cidr,
                insert=(x + 20, y + 65),
                fill=self.text_color,
                font_family="Arial, sans-serif",
                font_size="12px"
            )
            group.add(cidr_text) 