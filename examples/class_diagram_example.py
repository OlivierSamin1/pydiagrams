#!/usr/bin/env python3
"""
Class Diagram Example for PyDiagrams

This example demonstrates how to create a UML Class Diagram using the PyDiagrams library.
"""

import os
import sys

# Add the parent directory to sys.path to import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import ClassDiagram
from pydiagrams.diagrams.uml.class_diagram import Class, Interface, Enumeration
from pydiagrams.core.style import Style


def create_example_class_diagram():
    """Create an example class diagram of a simple e-commerce system."""
    
    # Create the diagram
    diagram = ClassDiagram("E-Commerce System Class Diagram")
    
    # Create classes
    customer = Class("Customer")
    customer.add_attribute("id", "int", "private")
    customer.add_attribute("name", "str", "private")
    customer.add_attribute("email", "str", "private")
    customer.add_method("register", "bool", [("email", "str"), ("password", "str")])
    customer.add_method("login", "bool", [("email", "str"), ("password", "str")])
    customer.add_method("update_profile", "bool")
    
    order = Class("Order")
    order.add_attribute("id", "int", "private")
    order.add_attribute("date", "datetime", "private")
    order.add_attribute("status", "OrderStatus", "private")
    order.add_method("place", "bool")
    order.add_method("cancel", "bool")
    order.add_method("ship", "bool")
    
    order_item = Class("OrderItem")
    order_item.add_attribute("quantity", "int", "private")
    order_item.add_attribute("price", "float", "private")
    order_item.add_method("calculate_subtotal", "float")
    
    product = Class("Product")
    product.add_attribute("id", "int", "private")
    product.add_attribute("name", "str", "private")
    product.add_attribute("description", "str", "private")
    product.add_attribute("price", "float", "private")
    product.add_attribute("stock", "int", "private")
    product.add_method("update_stock", "bool", [("quantity", "int")])
    
    payment = Class("Payment")
    payment.add_attribute("id", "int", "private")
    payment.add_attribute("amount", "float", "private")
    payment.add_attribute("date", "datetime", "private")
    payment.add_attribute("status", "PaymentStatus", "private")
    payment.add_method("process", "bool")
    payment.add_method("refund", "bool")
    
    # Create interfaces
    payable = Interface("Payable")
    payable.add_method("process_payment", "bool", [("amount", "float")])
    
    shippable = Interface("Shippable")
    shippable.add_method("ship", "bool", [("address", "str")])
    
    # Create enumerations
    order_status = Enumeration("OrderStatus")
    order_status.add_value("PENDING")
    order_status.add_value("PROCESSING")
    order_status.add_value("SHIPPED")
    order_status.add_value("DELIVERED")
    order_status.add_value("CANCELED")
    
    payment_status = Enumeration("PaymentStatus")
    payment_status.add_value("PENDING")
    payment_status.add_value("COMPLETED")
    payment_status.add_value("FAILED")
    payment_status.add_value("REFUNDED")
    
    # Add all classes to the diagram
    diagram.add_class(customer)
    diagram.add_class(order)
    diagram.add_class(order_item)
    diagram.add_class(product)
    diagram.add_class(payment)
    
    # Add interfaces
    diagram.add_interface(payable)
    diagram.add_interface(shippable)
    
    # Add enumerations
    diagram.add_enumeration(order_status)
    diagram.add_enumeration(payment_status)
    
    # Add relationships
    # Customer places orders
    diagram.add_association(customer, order, "1", "*", "places")
    
    # Order contains OrderItems
    diagram.add_composition(order, order_item, "1", "*", "contains")
    
    # OrderItem references Product
    diagram.add_association(order_item, product, "*", "1", "refers to")
    
    # Order has Payment
    diagram.add_association(order, payment, "1", "1..*", "has")
    
    # Order implements Shippable
    diagram.add_implementation(order, shippable)
    
    # Payment implements Payable
    diagram.add_implementation(payment, payable)
    
    # Order uses OrderStatus
    diagram.add_dependency(order, order_status, "«use»")
    
    # Payment uses PaymentStatus
    diagram.add_dependency(payment, payment_status, "«use»")
    
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram to SVG
    output_path = diagram.render("output/ecommerce_class_diagram.svg")
    print(f"Diagram rendered to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    create_example_class_diagram() 