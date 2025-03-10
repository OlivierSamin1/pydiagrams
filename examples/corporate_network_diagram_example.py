#!/usr/bin/env python3
"""
Example script demonstrating the creation of a Network Diagram for a corporate network.

This example shows a typical corporate network architecture including:
- DMZ with web and email servers
- Internal network with workstations and servers
- Data center
- Cloud services
- Various network devices and connections
"""

from pydiagrams.diagrams.architectural.network_diagram import (
    NetworkDiagram, DeviceType, ConnectionType, 
    NetworkDevice, NetworkConnection, NetworkZone
)
from pydiagrams.renderers.network_renderer import NetworkDiagramRenderer
import os

def create_corporate_network_diagram():
    """Create a network diagram for a corporate network architecture."""
    # Create the diagram
    diagram = NetworkDiagram(
        name="Corporate Network Architecture",
        description="Network diagram showing a typical corporate network setup"
    )
    
    # Create network zones
    internet_zone = diagram.create_zone(
        name="Internet",
        description="External network / Internet",
        zone_type="External"
    )
    
    dmz_zone = diagram.create_zone(
        name="DMZ",
        description="Demilitarized Zone",
        zone_type="DMZ",
        cidr="192.168.1.0/24"
    )
    
    internal_zone = diagram.create_zone(
        name="Internal Network",
        description="Corporate internal network",
        zone_type="Internal",
        cidr="10.0.0.0/16"
    )
    
    data_center_zone = diagram.create_zone(
        name="Data Center",
        description="Corporate data center",
        zone_type="Data Center",
        cidr="10.10.0.0/16"
    )
    
    cloud_zone = diagram.create_zone(
        name="Cloud Services",
        description="Cloud-hosted services",
        zone_type="Cloud"
    )
    
    # Create internet gateway
    internet_gateway = diagram.create_device(
        name="Internet Gateway",
        description="Connection to the Internet",
        device_type=DeviceType.GATEWAY,
        ip_address="203.0.113.1",
        zone_id=internet_zone.id
    )
    
    # Create edge firewall
    edge_firewall = diagram.create_device(
        name="Edge Firewall",
        description="Perimeter firewall",
        device_type=DeviceType.FIREWALL,
        ip_address="192.168.1.1",
        zone_id=dmz_zone.id
    )
    
    # DMZ devices
    web_server = diagram.create_device(
        name="Web Server",
        description="Public web server",
        device_type=DeviceType.SERVER,
        ip_address="192.168.1.10",
        zone_id=dmz_zone.id
    )
    
    mail_server = diagram.create_device(
        name="Mail Server",
        description="Email server",
        device_type=DeviceType.SERVER,
        ip_address="192.168.1.20",
        zone_id=dmz_zone.id
    )
    
    load_balancer = diagram.create_device(
        name="Load Balancer",
        description="Web traffic load balancer",
        device_type=DeviceType.LOAD_BALANCER,
        ip_address="192.168.1.5",
        zone_id=dmz_zone.id
    )
    
    # Internal network devices
    internal_firewall = diagram.create_device(
        name="Internal Firewall",
        description="Internal firewall",
        device_type=DeviceType.FIREWALL,
        ip_address="10.0.0.1",
        zone_id=internal_zone.id
    )
    
    internal_router = diagram.create_device(
        name="Core Router",
        description="Main corporate router",
        device_type=DeviceType.ROUTER,
        ip_address="10.0.0.2",
        zone_id=internal_zone.id
    )
    
    wifi_controller = diagram.create_device(
        name="WiFi Controller",
        description="Corporate wireless network controller",
        device_type=DeviceType.CUSTOM,
        ip_address="10.0.0.10",
        zone_id=internal_zone.id
    )
    
    workstation1 = diagram.create_device(
        name="Workstation 1",
        description="Employee workstation",
        device_type=DeviceType.WORKSTATION,
        ip_address="10.0.1.101",
        mac_address="00:1A:2B:3C:4D:5E",
        zone_id=internal_zone.id
    )
    
    workstation2 = diagram.create_device(
        name="Workstation 2",
        description="Employee workstation",
        device_type=DeviceType.WORKSTATION,
        ip_address="10.0.1.102",
        mac_address="00:1A:2B:3C:4D:5F",
        zone_id=internal_zone.id
    )
    
    # Data center devices
    dc_router = diagram.create_device(
        name="DC Router",
        description="Data center router",
        device_type=DeviceType.ROUTER,
        ip_address="10.10.0.1",
        zone_id=data_center_zone.id
    )
    
    dc_switch = diagram.create_device(
        name="DC Switch",
        description="Data center core switch",
        device_type=DeviceType.SWITCH,
        ip_address="10.10.0.2",
        zone_id=data_center_zone.id
    )
    
    app_server = diagram.create_device(
        name="App Server",
        description="Application server",
        device_type=DeviceType.SERVER,
        ip_address="10.10.1.10",
        zone_id=data_center_zone.id
    )
    
    db_server = diagram.create_device(
        name="DB Server",
        description="Database server",
        device_type=DeviceType.SERVER,
        ip_address="10.10.1.20",
        zone_id=data_center_zone.id
    )
    
    storage = diagram.create_device(
        name="SAN",
        description="Storage Area Network",
        device_type=DeviceType.STORAGE,
        ip_address="10.10.1.30",
        zone_id=data_center_zone.id
    )
    
    # Cloud services
    cloud_gateway = diagram.create_device(
        name="VPN Gateway",
        description="VPN connection to cloud services",
        device_type=DeviceType.GATEWAY,
        ip_address="10.0.0.100",
        zone_id=internal_zone.id
    )
    
    cloud_services = diagram.create_device(
        name="Cloud Services",
        description="SaaS and cloud infrastructure",
        device_type=DeviceType.CLOUD,
        zone_id=cloud_zone.id
    )
    
    # Create connections
    # Internet to Edge Firewall
    diagram.create_connection(
        internet_gateway.id, edge_firewall.id,
        name="Internet Link",
        connection_type=ConnectionType.INTERNET,
        bandwidth="1 Gbps",
        protocol="TCP/IP"
    )
    
    # Edge Firewall to DMZ
    diagram.create_connection(
        edge_firewall.id, load_balancer.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="1 Gbps"
    )
    
    diagram.create_connection(
        load_balancer.id, web_server.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="1 Gbps",
        protocol="HTTP/HTTPS"
    )
    
    diagram.create_connection(
        edge_firewall.id, mail_server.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="1 Gbps",
        protocol="SMTP/IMAP"
    )
    
    # DMZ to Internal
    diagram.create_connection(
        edge_firewall.id, internal_firewall.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="10 Gbps"
    )
    
    # Internal network connections
    diagram.create_connection(
        internal_firewall.id, internal_router.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="10 Gbps"
    )
    
    diagram.create_connection(
        internal_router.id, wifi_controller.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="1 Gbps"
    )
    
    # Workstation connections
    diagram.create_connection(
        wifi_controller.id, workstation1.id,
        connection_type=ConnectionType.WIRELESS,
        bandwidth="300 Mbps",
        protocol="802.11n"
    )
    
    diagram.create_connection(
        wifi_controller.id, workstation2.id,
        connection_type=ConnectionType.WIRELESS,
        bandwidth="300 Mbps",
        protocol="802.11n"
    )
    
    # Internal to Data Center
    diagram.create_connection(
        internal_router.id, dc_router.id,
        connection_type=ConnectionType.FIBER,
        bandwidth="40 Gbps"
    )
    
    # Data center connections
    diagram.create_connection(
        dc_router.id, dc_switch.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="40 Gbps"
    )
    
    for server in [app_server, db_server, storage]:
        diagram.create_connection(
            dc_switch.id, server.id,
            connection_type=ConnectionType.ETHERNET,
            bandwidth="10 Gbps"
        )
    
    # Connection to cloud
    diagram.create_connection(
        internal_router.id, cloud_gateway.id,
        connection_type=ConnectionType.ETHERNET,
        bandwidth="1 Gbps"
    )
    
    diagram.create_connection(
        cloud_gateway.id, cloud_services.id,
        connection_type=ConnectionType.VPN,
        bandwidth="500 Mbps",
        protocol="IPSEC"
    )
    
    return diagram

def main():
    """Main function to create and render the network diagram."""
    # Create the diagram
    diagram = create_corporate_network_diagram()
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create renderer and render the diagram
    renderer = NetworkDiagramRenderer(
        width=1400,  # Larger width to accommodate the complex diagram
        height=1000  # Larger height to accommodate the complex diagram
    )
    output_path = "output/corporate_network_diagram.svg"
    renderer.render(diagram, output_path)
    print(f"Network diagram has been rendered to: {output_path}")

if __name__ == "__main__":
    main() 