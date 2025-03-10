#!/usr/bin/env python3
"""
Example script demonstrating the creation of a Container Diagram for a banking system.

This example shows a banking system broken down into its constituent containers,
including web applications, mobile apps, APIs, databases, and their relationships
with users and external systems.
"""

from pydiagrams.diagrams.architectural.container_diagram import (
    ContainerDiagram, ContainerType, ContainerRelationshipType, 
    Person, Container, ExternalSystem, SystemBoundary
)
from pydiagrams.renderers.container_renderer import ContainerDiagramRenderer
import os

def create_banking_container_diagram():
    """Create a container diagram for a banking system."""
    # Create the diagram
    diagram = ContainerDiagram(
        name="Banking System - Container Diagram",
        description="A detailed view of the containers within the digital banking system"
    )
    
    # Create System Boundary
    banking_system_boundary = diagram.create_boundary(
        name="Digital Banking System",
        description="Core banking platform providing online and mobile banking services"
    )
    
    # Create People (Users)
    customer = diagram.create_person(
        name="Customer",
        description="A customer of the bank with one or more accounts",
        external=True
    )
    
    bank_staff = diagram.create_person(
        name="Bank Staff",
        description="Staff who support customers and manage accounts",
        external=False
    )
    
    # Create External Systems
    core_banking = diagram.create_external_system(
        name="Core Banking System",
        description="Manages customer accounts, transactions, and balances",
        technology="Mainframe/Oracle"
    )
    
    payment_gateway = diagram.create_external_system(
        name="Payment Gateway",
        description="Processes payments and transfers to external accounts",
        technology="Third-party API"
    )
    
    email_system = diagram.create_external_system(
        name="Email System",
        description="Sends email notifications to customers",
        technology="SMTP"
    )
    
    # Create Containers
    web_app = diagram.create_container(
        name="Web Application",
        description="Provides online banking functionality to customers via their web browser",
        technology="React, JavaScript",
        container_type=ContainerType.WEB_APPLICATION
    )
    banking_system_boundary.add_container_id(web_app.id)
    
    mobile_app = diagram.create_container(
        name="Mobile Application",
        description="Provides banking functionality to customers via their mobile device",
        technology="Native iOS/Android",
        container_type=ContainerType.MOBILE_APP
    )
    banking_system_boundary.add_container_id(mobile_app.id)
    
    staff_app = diagram.create_container(
        name="Staff Portal",
        description="Allows bank staff to manage customer accounts and handle issues",
        technology="Angular, TypeScript",
        container_type=ContainerType.WEB_APPLICATION
    )
    banking_system_boundary.add_container_id(staff_app.id)
    
    api_gateway = diagram.create_container(
        name="API Gateway",
        description="Routes API requests to appropriate microservices",
        technology="NGINX, Kong",
        container_type=ContainerType.API
    )
    banking_system_boundary.add_container_id(api_gateway.id)
    
    account_service = diagram.create_container(
        name="Account Service",
        description="Provides account management functionality",
        technology="Spring Boot, Java",
        container_type=ContainerType.MICROSERVICE
    )
    banking_system_boundary.add_container_id(account_service.id)
    
    transaction_service = diagram.create_container(
        name="Transaction Service",
        description="Processes bank transactions and transfers",
        technology="Spring Boot, Java",
        container_type=ContainerType.MICROSERVICE
    )
    banking_system_boundary.add_container_id(transaction_service.id)
    
    notification_service = diagram.create_container(
        name="Notification Service",
        description="Sends notifications to customers via different channels",
        technology="Node.js, Express",
        container_type=ContainerType.MICROSERVICE
    )
    banking_system_boundary.add_container_id(notification_service.id)
    
    customer_db = diagram.create_container(
        name="Customer Database",
        description="Stores customer profile information",
        technology="MongoDB",
        container_type=ContainerType.DATABASE
    )
    banking_system_boundary.add_container_id(customer_db.id)
    
    transaction_db = diagram.create_container(
        name="Transaction Database",
        description="Stores transaction history and details",
        technology="PostgreSQL",
        container_type=ContainerType.DATABASE
    )
    banking_system_boundary.add_container_id(transaction_db.id)
    
    message_queue = diagram.create_container(
        name="Message Queue",
        description="Handles asynchronous messaging between services",
        technology="RabbitMQ",
        container_type=ContainerType.QUEUE
    )
    banking_system_boundary.add_container_id(message_queue.id)
    
    cache = diagram.create_container(
        name="Cache",
        description="Caches frequently accessed data",
        technology="Redis",
        container_type=ContainerType.CACHE
    )
    banking_system_boundary.add_container_id(cache.id)
    
    # Create Relationships
    # Customer to Applications
    diagram.create_relationship(
        customer.id, web_app.id,
        name="Uses",
        description="Accesses banking services via web browser",
        relationship_type=ContainerRelationshipType.USES,
        technology="HTTPS"
    )
    
    diagram.create_relationship(
        customer.id, mobile_app.id,
        name="Uses",
        description="Accesses banking services via mobile app",
        relationship_type=ContainerRelationshipType.USES,
        technology="HTTPS"
    )
    
    # Bank Staff to Staff Portal
    diagram.create_relationship(
        bank_staff.id, staff_app.id,
        name="Uses",
        description="Manages customer accounts and issues",
        relationship_type=ContainerRelationshipType.USES,
        technology="HTTPS"
    )
    
    # Applications to API Gateway
    for app in [web_app, mobile_app, staff_app]:
        diagram.create_relationship(
            app.id, api_gateway.id,
            name="Makes API calls to",
            relationship_type=ContainerRelationshipType.USES,
            technology="JSON/HTTPS"
        )
    
    # API Gateway to Microservices
    diagram.create_relationship(
        api_gateway.id, account_service.id,
        name="Routes account requests to",
        relationship_type=ContainerRelationshipType.USES,
        technology="JSON/HTTPS"
    )
    
    diagram.create_relationship(
        api_gateway.id, transaction_service.id,
        name="Routes transaction requests to",
        relationship_type=ContainerRelationshipType.USES,
        technology="JSON/HTTPS"
    )
    
    # Services to Databases
    diagram.create_relationship(
        account_service.id, customer_db.id,
        name="Reads from and writes to",
        relationship_type=ContainerRelationshipType.USES,
        technology="MongoDB Driver"
    )
    
    diagram.create_relationship(
        transaction_service.id, transaction_db.id,
        name="Reads from and writes to",
        relationship_type=ContainerRelationshipType.USES,
        technology="JDBC"
    )
    
    # Services to Cache
    diagram.create_relationship(
        account_service.id, cache.id,
        name="Reads from and writes to",
        relationship_type=ContainerRelationshipType.USES,
        technology="Redis Client"
    )
    
    diagram.create_relationship(
        transaction_service.id, cache.id,
        name="Reads from and writes to",
        relationship_type=ContainerRelationshipType.USES,
        technology="Redis Client"
    )
    
    # Services to Message Queue
    diagram.create_relationship(
        transaction_service.id, message_queue.id,
        name="Publishes messages to",
        relationship_type=ContainerRelationshipType.WRITES_TO,
        technology="AMQP"
    )
    
    diagram.create_relationship(
        notification_service.id, message_queue.id,
        name="Consumes messages from",
        relationship_type=ContainerRelationshipType.READS_FROM,
        technology="AMQP"
    )
    
    # Services to External Systems
    diagram.create_relationship(
        account_service.id, core_banking.id,
        name="Retrieves account details from",
        relationship_type=ContainerRelationshipType.USES,
        technology="SOAP/MQ"
    )
    
    diagram.create_relationship(
        transaction_service.id, core_banking.id,
        name="Sends transactions to",
        relationship_type=ContainerRelationshipType.SENDS_DATA_TO,
        technology="SOAP/MQ"
    )
    
    diagram.create_relationship(
        transaction_service.id, payment_gateway.id,
        name="Sends payment instructions to",
        relationship_type=ContainerRelationshipType.SENDS_DATA_TO,
        technology="HTTPS/REST"
    )
    
    diagram.create_relationship(
        notification_service.id, email_system.id,
        name="Sends emails via",
        relationship_type=ContainerRelationshipType.USES,
        technology="SMTP"
    )
    
    return diagram

def main():
    """Main function to create and render the container diagram."""
    # Create the diagram
    diagram = create_banking_container_diagram()
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create renderer and render the diagram
    renderer = ContainerDiagramRenderer(
        width=1400,  # Larger width to accommodate the complex diagram
        height=1200  # Larger height to accommodate the complex diagram
    )
    output_path = "output/banking_container_diagram.svg"
    renderer.render(diagram, output_path)
    print(f"Container diagram has been rendered to: {output_path}")

if __name__ == "__main__":
    main() 