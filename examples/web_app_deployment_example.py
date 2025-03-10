#!/usr/bin/env python3
"""
Example script demonstrating the creation of a Deployment Diagram for a web application.

This example shows a typical web application deployment architecture including:
- Load balancer
- Web servers
- Application servers
- Database server
- Message queue
- Monitoring system
"""

from pydiagrams.diagrams.architectural.deployment_diagram import (
    DeploymentDiagram, NodeType, CommunicationType
)
from pydiagrams.renderers.deployment_renderer import DeploymentDiagramRenderer
import os

def create_web_app_deployment_diagram():
    """Create a deployment diagram for a web application architecture."""
    # Create the diagram
    diagram = DeploymentDiagram(
        name="Web Application Deployment",
        description="Deployment diagram showing the architecture of a web application"
    )
    
    # Create infrastructure nodes
    load_balancer = diagram.create_node(
        name="Load Balancer",
        description="NGINX Load Balancer",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    load_balancer.add_artifact(diagram.create_artifact(
        name="NGINX",
        description="NGINX Load Balancer",
        artifact_type="software",
        stereotype="executable"
    ))

    # Web Server nodes
    web_server1 = diagram.create_node(
        name="Web Server 1",
        description="Web Server Instance 1",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    web_server2 = diagram.create_node(
        name="Web Server 2",
        description="Web Server Instance 2",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )

    # Add containers to web servers
    for web_server in [web_server1, web_server2]:
        web_server.add_artifact(diagram.create_artifact(
            name="Web Container",
            description="Docker container running web application",
            artifact_type="container",
            stereotype="container"
        ))
        web_server.add_artifact(diagram.create_artifact(
            name="Static Files",
            description="Web application static files",
            artifact_type="files",
            stereotype="artifact"
        ))

    # Application Server
    app_server = diagram.create_node(
        name="Application Server",
        description="Main application server",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    app_server.add_artifact(diagram.create_artifact(
        name="App Container",
        description="Docker container running application logic",
        artifact_type="container",
        stereotype="container"
    ))
    app_server.add_artifact(diagram.create_artifact(
        name="Cache",
        description="Redis cache instance",
        artifact_type="service",
        stereotype="service"
    ))

    # Database Server
    db_server = diagram.create_node(
        name="Database Server",
        description="PostgreSQL Database Server",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    db_server.add_artifact(diagram.create_artifact(
        name="PostgreSQL",
        description="PostgreSQL Database",
        artifact_type="database",
        stereotype="database"
    ))

    # Message Queue Server
    mq_server = diagram.create_node(
        name="Message Queue",
        description="RabbitMQ Server",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    mq_server.add_artifact(diagram.create_artifact(
        name="RabbitMQ",
        description="Message Queue Service",
        artifact_type="service",
        stereotype="queue"
    ))

    # Monitoring Server
    monitoring = diagram.create_node(
        name="Monitoring",
        description="Monitoring and Logging Server",
        node_type=NodeType.DEVICE,
        stereotype="device"
    )
    monitoring.add_artifact(diagram.create_artifact(
        name="Prometheus",
        description="Metrics Collection",
        artifact_type="service",
        stereotype="monitoring"
    ))
    monitoring.add_artifact(diagram.create_artifact(
        name="Grafana",
        description="Metrics Visualization",
        artifact_type="service",
        stereotype="monitoring"
    ))

    # Add communication paths
    # Load Balancer to Web Servers
    diagram.create_communication_path(
        load_balancer.id, web_server1.id,
        name="HTTP Traffic",
        communication_type=CommunicationType.NETWORK,
        protocol="HTTP/HTTPS"
    )
    diagram.create_communication_path(
        load_balancer.id, web_server2.id,
        name="HTTP Traffic",
        communication_type=CommunicationType.NETWORK,
        protocol="HTTP/HTTPS"
    )

    # Web Servers to Application Server
    for web_server in [web_server1, web_server2]:
        diagram.create_communication_path(
            web_server.id, app_server.id,
            name="API Calls",
            communication_type=CommunicationType.NETWORK,
            protocol="HTTP/REST"
        )

    # Application Server to Database
    diagram.create_communication_path(
        app_server.id, db_server.id,
        name="Database Connection",
        communication_type=CommunicationType.NETWORK,
        protocol="PostgreSQL"
    )

    # Application Server to Message Queue
    diagram.create_communication_path(
        app_server.id, mq_server.id,
        name="Message Queue",
        communication_type=CommunicationType.NETWORK,
        protocol="AMQP"
    )

    # All nodes to Monitoring
    for node in [load_balancer, web_server1, web_server2, app_server, db_server, mq_server]:
        diagram.create_communication_path(
            node.id, monitoring.id,
            name="Metrics",
            communication_type=CommunicationType.NETWORK,
            protocol="HTTP"
        )

    return diagram

def main():
    """Main function to create and render the deployment diagram."""
    # Create the diagram
    diagram = create_web_app_deployment_diagram()

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Create renderer and render the diagram
    renderer = DeploymentDiagramRenderer(
        width=1200,  # Larger width to accommodate the complex diagram
        height=1000  # Larger height to accommodate the complex diagram
    )
    output_path = "output/web_app_deployment.svg"
    renderer.render(diagram, output_path)
    print(f"Deployment diagram has been rendered to: {output_path}")

if __name__ == "__main__":
    main() 