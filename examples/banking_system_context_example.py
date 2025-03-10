#!/usr/bin/env python3
"""
Example script demonstrating the creation of a System Context Diagram for a banking system.

This example shows a banking system in the context of its users and external systems,
including customers, bank staff, partner systems, and regulatory systems.
"""

from pydiagrams.diagrams.architectural.context_diagram import (
    SystemContextDiagram, ElementType, RelationshipType
)
from pydiagrams.renderers.context_renderer import SystemContextDiagramRenderer
import os

def create_banking_system_context_diagram():
    """Create a system context diagram for a banking system."""
    # Create the diagram
    diagram = SystemContextDiagram(
        name="Banking System - System Context Diagram",
        description="High-level view of the banking system and its interactions"
    )
    
    # Create Enterprise Boundary
    enterprise_boundary = diagram.create_boundary(
        name="Bank Enterprise",
        description="Digital Banking Division"
    )
    
    # Create Central System
    banking_system = diagram.create_element(
        name="Digital Banking System",
        description="Core banking platform providing online and mobile banking services",
        element_type=ElementType.SYSTEM
    )
    
    # Add the system to the enterprise boundary
    enterprise_boundary.add_element_id(banking_system.id)
    
    # Create People (Users)
    customer = diagram.create_element(
        name="Customer",
        description="A customer of the bank with one or more accounts",
        element_type=ElementType.PERSON
    )
    
    bank_staff = diagram.create_element(
        name="Bank Staff",
        description="Staff who support customers and manage accounts",
        element_type=ElementType.PERSON
    )
    
    # Add staff to the enterprise boundary
    enterprise_boundary.add_element_id(bank_staff.id)
    
    # Create External Systems
    core_banking = diagram.create_element(
        name="Core Banking System",
        description="Manages customer accounts, transactions, and balances",
        element_type=ElementType.EXTERNAL_SYSTEM
    )
    
    payment_gateway = diagram.create_element(
        name="Payment Gateway",
        description="Processes payments and transfers to external accounts",
        element_type=ElementType.EXTERNAL_SYSTEM
    )
    
    authentication_system = diagram.create_element(
        name="Authentication System",
        description="Manages user identity and authentication",
        element_type=ElementType.EXTERNAL_SYSTEM
    )
    
    regulatory_system = diagram.create_element(
        name="Regulatory Reporting",
        description="Compliance reporting for financial regulations",
        element_type=ElementType.EXTERNAL_SYSTEM
    )
    
    # Add some systems to the enterprise boundary
    enterprise_boundary.add_element_id(core_banking.id)
    enterprise_boundary.add_element_id(authentication_system.id)
    
    # Create Relationships
    # Customer to Banking System
    diagram.create_relationship(
        customer.id, banking_system.id,
        name="Views accounts",
        description="Views account information and transaction history",
        relationship_type=RelationshipType.USES,
        technology="Web/Mobile App"
    )
    
    diagram.create_relationship(
        customer.id, banking_system.id,
        name="Makes payments",
        description="Transfers money and pays bills",
        relationship_type=RelationshipType.USES,
        technology="Web/Mobile App"
    )
    
    # Bank Staff to Banking System
    diagram.create_relationship(
        bank_staff.id, banking_system.id,
        name="Manages accounts",
        description="Manages customer accounts and assists with issues",
        relationship_type=RelationshipType.USES,
        technology="Web Application"
    )
    
    # Banking System to Core Banking
    diagram.create_relationship(
        banking_system.id, core_banking.id,
        name="Gets account data",
        description="Retrieves account information and processes transactions",
        relationship_type=RelationshipType.USES,
        technology="API/MQ"
    )
    
    # Banking System to Authentication System
    diagram.create_relationship(
        banking_system.id, authentication_system.id,
        name="Authenticates users",
        description="Verifies user identity and manages sessions",
        relationship_type=RelationshipType.USES,
        technology="SAML/OAuth"
    )
    
    # Banking System to Payment Gateway
    diagram.create_relationship(
        banking_system.id, payment_gateway.id,
        name="Processes payments",
        description="Sends payment instructions to external financial systems",
        relationship_type=RelationshipType.SENDS_DATA_TO,
        technology="API"
    )
    
    # Banking System to Regulatory Reporting
    diagram.create_relationship(
        banking_system.id, regulatory_system.id,
        name="Sends compliance data",
        description="Provides transaction and account data for regulatory reporting",
        relationship_type=RelationshipType.SENDS_DATA_TO,
        technology="Batch/API"
    )
    
    return diagram

def main():
    """Main function to create and render the system context diagram."""
    # Create the diagram
    diagram = create_banking_system_context_diagram()
    
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create renderer and render the diagram
    renderer = SystemContextDiagramRenderer(
        width=1200,
        height=900
    )
    output_path = "output/banking_system_context_diagram.svg"
    renderer.render(diagram, output_path)
    print(f"System Context diagram has been rendered to: {output_path}")

if __name__ == "__main__":
    main() 