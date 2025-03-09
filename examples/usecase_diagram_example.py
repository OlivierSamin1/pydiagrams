#!/usr/bin/env python3
"""
Example of creating a UML Use Case Diagram using the PyDiagrams library.

This example demonstrates creating a use case diagram for an e-commerce system,
showing different actors, use cases, and their relationships.
"""

import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import UseCaseDiagram
from pydiagrams.diagrams.uml.usecase_diagram import (
    Actor, UseCase, System, UseCaseRelationship, UseCaseRelationshipType
)


def create_example_usecase_diagram():
    """
    Create a UML Use Case Diagram for an e-commerce system.
    
    The diagram shows the interactions between different actors and use cases
    in an online shopping system.
    
    Returns:
        The path to the rendered diagram file.
    """
    # Create a new use case diagram
    diagram = UseCaseDiagram("E-Commerce System Use Case Diagram")
    
    # Create actors
    customer = diagram.create_actor("Customer")
    admin = diagram.create_actor("Administrator", is_primary=False)
    payment_processor = diagram.create_actor("Payment Processor", is_primary=False)
    warehouse_manager = diagram.create_actor("Warehouse Manager", is_primary=False)
    shipping_company = diagram.create_actor("Shipping Company", is_primary=False)
    
    # Create system boundary
    system = diagram.create_system("E-Commerce System")
    
    # Create use cases
    # Customer-related use cases
    browse_products = diagram.create_use_case("Browse Products", 
                                             "Search and view products in the catalog")
    register_account = diagram.create_use_case("Register Account", 
                                              "Create a new customer account")
    login = diagram.create_use_case("Login", 
                                   "Authenticate and access the system")
    add_to_cart = diagram.create_use_case("Add to Cart", 
                                         "Add products to shopping cart")
    checkout = diagram.create_use_case("Checkout", 
                                      "Complete the purchase process")
    track_order = diagram.create_use_case("Track Order", 
                                         "Check the status of an order")
    manage_profile = diagram.create_use_case("Manage Profile", 
                                            "View and update account information")
    
    # Admin-related use cases
    manage_products = diagram.create_use_case("Manage Products", 
                                             "Add, edit, or remove products")
    manage_orders = diagram.create_use_case("Manage Orders", 
                                           "View and update order status")
    generate_reports = diagram.create_use_case("Generate Reports", 
                                              "Create sales and inventory reports")
    
    # Included/extended use cases
    validate_payment = diagram.create_use_case("Validate Payment", 
                                              "Verify payment information")
    process_payment = diagram.create_use_case("Process Payment", 
                                             "Handle payment transaction")
    notify_warehouse = diagram.create_use_case("Notify Warehouse", 
                                              "Send order details to warehouse")
    ship_order = diagram.create_use_case("Ship Order", 
                                        "Prepare and ship the order")
    handle_discount = diagram.create_use_case("Apply Discount", 
                                             "Apply coupon or promotional discount")
    
    # Add use cases to the system
    diagram.add_use_case_to_system(browse_products, system)
    diagram.add_use_case_to_system(register_account, system)
    diagram.add_use_case_to_system(login, system)
    diagram.add_use_case_to_system(add_to_cart, system)
    diagram.add_use_case_to_system(checkout, system)
    diagram.add_use_case_to_system(track_order, system)
    diagram.add_use_case_to_system(manage_profile, system)
    diagram.add_use_case_to_system(manage_products, system)
    diagram.add_use_case_to_system(manage_orders, system)
    diagram.add_use_case_to_system(generate_reports, system)
    diagram.add_use_case_to_system(validate_payment, system)
    diagram.add_use_case_to_system(process_payment, system)
    diagram.add_use_case_to_system(notify_warehouse, system)
    diagram.add_use_case_to_system(ship_order, system)
    diagram.add_use_case_to_system(handle_discount, system)
    
    # Create associations between actors and use cases
    # Customer associations
    diagram.create_association(customer, browse_products)
    diagram.create_association(customer, register_account)
    diagram.create_association(customer, login)
    diagram.create_association(customer, add_to_cart)
    diagram.create_association(customer, checkout)
    diagram.create_association(customer, track_order)
    diagram.create_association(customer, manage_profile)
    
    # Admin associations
    diagram.create_association(admin, login)
    diagram.create_association(admin, manage_products)
    diagram.create_association(admin, manage_orders)
    diagram.create_association(admin, generate_reports)
    
    # Other actor associations
    diagram.create_association(payment_processor, process_payment)
    diagram.create_association(warehouse_manager, notify_warehouse)
    diagram.create_association(shipping_company, ship_order)
    
    # Create include and extend relationships
    diagram.create_include(checkout, validate_payment)
    diagram.create_include(checkout, process_payment)
    diagram.create_include(checkout, notify_warehouse)
    diagram.create_include(notify_warehouse, ship_order)
    diagram.create_extend(handle_discount, checkout)
    
    # Create generalizations
    # No generalizations in this example
    
    # Ensure the output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram to an SVG file
    output_path = "output/ecommerce_usecase_diagram.svg"
    diagram.render(output_path)
    
    print(f"Diagram rendered to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_example_usecase_diagram() 