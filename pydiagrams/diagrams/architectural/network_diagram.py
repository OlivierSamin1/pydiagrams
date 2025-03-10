#!/usr/bin/env python3
"""
Network Diagram module for PyDiagrams.

This module provides the implementation for Network Diagrams, which show
network topology, devices, connections, and network zones in a system.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class DeviceType(Enum):
    """Types of network devices in a Network Diagram."""
    ROUTER = auto()
    SWITCH = auto()
    FIREWALL = auto()
    SERVER = auto()
    WORKSTATION = auto()
    CLOUD = auto()
    STORAGE = auto()
    LOAD_BALANCER = auto()
    GATEWAY = auto()
    CUSTOM = auto()


class ConnectionType(Enum):
    """Types of network connections in a Network Diagram."""
    ETHERNET = auto()
    FIBER = auto()
    WIRELESS = auto()
    VPN = auto()
    INTERNET = auto()
    CUSTOM = auto()


@dataclass
class NetworkDevice:
    """
    Represents a device in a Network Diagram.
    
    A device can be a router, switch, server, workstation, etc.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    device_type: DeviceType = DeviceType.SERVER
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    zone_id: Optional[str] = None  # Reference to the zone this device belongs to
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Device_{self.id[:8]}"


@dataclass
class NetworkConnection:
    """
    Represents a network connection between devices in a Network Diagram.
    
    Connections represent how devices communicate with each other in the network.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_id: str = ""  # ID of source device
    target_id: str = ""  # ID of target device
    connection_type: ConnectionType = ConnectionType.ETHERNET
    bandwidth: Optional[str] = None  # e.g., "1Gbps", "10Gbps"
    protocol: Optional[str] = None  # e.g., "TCP/IP", "HTTP"
    is_bidirectional: bool = True
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Connection_{self.id[:8]}"


@dataclass
class NetworkZone:
    """
    Represents a network zone or segment in a Network Diagram.
    
    Zones represent logical or physical network segments, such as DMZ,
    internal network, or VLANs.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    zone_type: str = ""  # e.g., "DMZ", "Internal", "VLAN"
    cidr: Optional[str] = None  # CIDR notation for the network
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    parent_zone_id: Optional[str] = None  # Reference to parent zone for nested zones
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Zone_{self.id[:8]}"


class NetworkDiagram(BaseDiagram):
    """
    Network Diagram model.
    
    Network Diagrams visualize network topology, showing how network devices
    are connected and organized into zones, along with relevant networking
    information such as IP addresses, protocols, and bandwidth.
    """
    def __init__(self, name: str, description: str = ""):
        """Initialize a network diagram."""
        super().__init__(name, description)
        self.devices: List[NetworkDevice] = []
        self.connections: List[NetworkConnection] = []
        self.zones: List[NetworkZone] = []
        self.layout = HierarchicalLayout()
    
    def add_device(self, device: NetworkDevice) -> None:
        """Add a network device to the diagram."""
        self.devices.append(device)
    
    def add_connection(self, connection: NetworkConnection) -> None:
        """Add a network connection to the diagram."""
        self.connections.append(connection)
    
    def add_zone(self, zone: NetworkZone) -> None:
        """Add a network zone to the diagram."""
        self.zones.append(zone)
    
    def create_device(
        self,
        name: str,
        description: str = "",
        device_type: DeviceType = DeviceType.SERVER,
        ip_address: Optional[str] = None,
        mac_address: Optional[str] = None,
        stereotype: Optional[str] = None,
        zone_id: Optional[str] = None
    ) -> NetworkDevice:
        """
        Create and add a network device to the diagram.
        
        Args:
            name: Name of the device
            description: Description of the device
            device_type: Type of device (router, switch, etc.)
            ip_address: IP address of the device
            mac_address: MAC address of the device
            stereotype: UML stereotype for the device
            zone_id: ID of the zone this device belongs to
            
        Returns:
            The created NetworkDevice object
        """
        device = NetworkDevice(
            name=name,
            description=description,
            device_type=device_type,
            ip_address=ip_address,
            mac_address=mac_address,
            stereotype=stereotype,
            zone_id=zone_id
        )
        self.add_device(device)
        return device
    
    def create_connection(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        connection_type: ConnectionType = ConnectionType.ETHERNET,
        bandwidth: Optional[str] = None,
        protocol: Optional[str] = None,
        is_bidirectional: bool = True,
        stereotype: Optional[str] = None
    ) -> NetworkConnection:
        """
        Create and add a network connection to the diagram.
        
        Args:
            source_id: ID of the source device
            target_id: ID of the target device
            name: Name of the connection
            connection_type: Type of connection (ethernet, fiber, etc.)
            bandwidth: Bandwidth of the connection
            protocol: Communication protocol used
            is_bidirectional: Whether the connection is bidirectional
            stereotype: UML stereotype for the connection
            
        Returns:
            The created NetworkConnection object
        """
        connection = NetworkConnection(
            name=name,
            source_id=source_id,
            target_id=target_id,
            connection_type=connection_type,
            bandwidth=bandwidth,
            protocol=protocol,
            is_bidirectional=is_bidirectional,
            stereotype=stereotype
        )
        self.add_connection(connection)
        return connection
    
    def create_zone(
        self,
        name: str,
        description: str = "",
        zone_type: str = "",
        cidr: Optional[str] = None,
        stereotype: Optional[str] = None,
        parent_zone_id: Optional[str] = None
    ) -> NetworkZone:
        """
        Create and add a network zone to the diagram.
        
        Args:
            name: Name of the zone
            description: Description of the zone
            zone_type: Type of zone (DMZ, Internal, VLAN, etc.)
            cidr: CIDR notation for the network
            stereotype: UML stereotype for the zone
            parent_zone_id: ID of the parent zone for nested zones
            
        Returns:
            The created NetworkZone object
        """
        zone = NetworkZone(
            name=name,
            description=description,
            zone_type=zone_type,
            cidr=cidr,
            stereotype=stereotype,
            parent_zone_id=parent_zone_id
        )
        self.add_zone(zone)
        return zone
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the network diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This is a placeholder that will be implemented by renderers
        return file_path 