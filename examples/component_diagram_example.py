#!/usr/bin/env python3
"""
Example of creating a UML Component Diagram with the PyDiagrams library.

This example creates a component diagram for a simplified e-commerce system.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from pydiagrams.diagrams.uml.component_diagram import (
    ComponentDiagram, Component, Interface, Connector,
    Artifact, ConnectorType, ComponentType, InterfaceType
)
from pydiagrams.renderers.component_renderer import ComponentDiagramRenderer


def create_example_component_diagram():
    """
    Create an example UML Component Diagram for an e-commerce system.
    
    Returns:
        The path to the rendered SVG file
    """
    # Create a new Component Diagram
    diagram = ComponentDiagram(
        name="E-Commerce System Architecture",
        description="Component diagram showing the architecture of an e-commerce system"
    )
    
    # Create components
    web_app = diagram.create_component(
        name="Web Application",
        stereotype="subsystem"
    )
    
    api_gateway = diagram.create_component(
        name="API Gateway",
        component_type=ComponentType.COMPONENT
    )
    
    auth_service = diagram.create_component(
        name="Authentication Service",
        component_type=ComponentType.COMPONENT
    )
    
    catalog_service = diagram.create_component(
        name="Catalog Service",
        component_type=ComponentType.COMPONENT
    )
    
    order_service = diagram.create_component(
        name="Order Service",
        component_type=ComponentType.COMPONENT
    )
    
    payment_service = diagram.create_component(
        name="Payment Service",
        component_type=ComponentType.COMPONENT
    )
    
    db_server = diagram.create_component(
        name="Database Server",
        stereotype="device",
        component_type=ComponentType.DEVICE
    )
    
    # Create interfaces
    # API Gateway interfaces
    rest_api = diagram.create_interface(
        name="REST API",
        operations=["getProducts()", "placeOrder()", "getOrderStatus()"]
    )
    api_gateway.add_provided_interface(rest_api)
    
    auth_api = diagram.create_interface(
        name="Auth API",
        operations=["login()", "logout()", "register()"]
    )
    api_gateway.add_required_interface(auth_api)
    
    catalog_api = diagram.create_interface(
        name="Catalog API",
        operations=["getProducts()", "getProductDetails()"]
    )
    api_gateway.add_required_interface(catalog_api)
    
    order_api = diagram.create_interface(
        name="Order API",
        operations=["createOrder()", "getOrderStatus()"]
    )
    api_gateway.add_required_interface(order_api)
    
    # Service interfaces
    auth_service.add_provided_interface(auth_api)
    catalog_service.add_provided_interface(catalog_api)
    order_service.add_provided_interface(order_api)
    
    payment_api = diagram.create_interface(
        name="Payment API",
        operations=["processPayment()", "refundPayment()"]
    )
    payment_service.add_provided_interface(payment_api)
    
    order_service_payment = diagram.create_interface(
        name="Payment Processing",
        operations=["processPayment()"]
    )
    order_service.add_required_interface(order_service_payment)
    
    # Database interfaces
    db_auth = diagram.create_interface(name="Auth DB")
    auth_service.add_required_interface(db_auth)
    
    db_catalog = diagram.create_interface(name="Catalog DB")
    catalog_service.add_required_interface(db_catalog)
    
    db_order = diagram.create_interface(name="Order DB")
    order_service.add_required_interface(db_order)
    
    db_payment = diagram.create_interface(name="Payment DB")
    payment_service.add_required_interface(db_payment)
    
    # Create connectors
    # Web App to API Gateway
    diagram.create_connector(
        source_id=web_app.id,
        target_id=api_gateway.id,
        connector_type=ConnectorType.DEPENDENCY,
        name="uses"
    )
    
    # API Gateway to Services
    diagram.create_connector(
        source_id=api_gateway.id,
        target_id=auth_service.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    diagram.create_connector(
        source_id=api_gateway.id,
        target_id=catalog_service.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    diagram.create_connector(
        source_id=api_gateway.id,
        target_id=order_service.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    # Order Service to Payment Service
    diagram.create_connector(
        source_id=order_service.id,
        target_id=payment_service.id,
        connector_type=ConnectorType.DEPENDENCY,
        name="processes payments through"
    )
    
    # Services to Database
    diagram.create_connector(
        source_id=auth_service.id,
        target_id=db_server.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    diagram.create_connector(
        source_id=catalog_service.id,
        target_id=db_server.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    diagram.create_connector(
        source_id=order_service.id,
        target_id=db_server.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    diagram.create_connector(
        source_id=payment_service.id,
        target_id=db_server.id,
        connector_type=ConnectorType.DEPENDENCY
    )
    
    # Create artifacts
    web_artifact = diagram.create_artifact(
        name="web-app.war",
        stereotype="artifact"
    )
    
    api_gateway_artifact = diagram.create_artifact(
        name="api-gateway.jar",
        stereotype="artifact"
    )
    
    auth_artifact = diagram.create_artifact(
        name="auth-service.jar",
        stereotype="artifact"
    )
    
    catalog_artifact = diagram.create_artifact(
        name="catalog-service.jar",
        stereotype="artifact"
    )
    
    order_artifact = diagram.create_artifact(
        name="order-service.jar",
        stereotype="artifact"
    )
    
    payment_artifact = diagram.create_artifact(
        name="payment-service.jar",
        stereotype="artifact"
    )
    
    # Render the diagram
    renderer = ComponentDiagramRenderer(width=1000, height=800)
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram
    output_path = "output/ecommerce_component_diagram.svg"
    output_file = renderer.render(diagram, output_path)
    
    print(f"Diagram rendered to: {output_file}")
    return output_file


if __name__ == "__main__":
    create_example_component_diagram() 