#!/usr/bin/env python3
"""
Activity Diagram Example for PyDiagrams

This example demonstrates how to create a UML Activity Diagram using the PyDiagrams library.
The example models an online shopping checkout process.
"""

import os
import sys

# Add the parent directory to sys.path to import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import ActivityDiagram
from pydiagrams.diagrams.uml.activity_diagram import (
    ActivityNode, InitialNode, ActionNode, DecisionNode, MergeNode,
    ForkNode, JoinNode, ActivityFinalNode, ObjectNode, Swimlane
)


def create_example_activity_diagram():
    """Create an example activity diagram of an online shopping checkout process."""
    
    # Create the diagram
    diagram = ActivityDiagram("Online Shopping Checkout Process")
    
    # Create swimlanes for different actors
    customer_lane = diagram.create_swimlane("Customer", is_horizontal=True)
    system_lane = diagram.create_swimlane("System", is_horizontal=True)
    payment_lane = diagram.create_swimlane("Payment Processor", is_horizontal=True)
    
    # Create the nodes with positions
    # Initial node
    initial = diagram.create_initial_node()
    initial.properties["position"] = {"x": 400, "y": 50}
    diagram.add_node_to_swimlane(initial, customer_lane)
    
    # Customer actions
    review_cart = diagram.create_action_node("Review Shopping Cart")
    review_cart.properties["position"] = {"x": 350, "y": 100}
    diagram.add_node_to_swimlane(review_cart, customer_lane)
    
    proceed_checkout = diagram.create_action_node("Proceed to Checkout")
    proceed_checkout.properties["position"] = {"x": 350, "y": 180}
    diagram.add_node_to_swimlane(proceed_checkout, customer_lane)
    
    enter_shipping = diagram.create_action_node("Enter Shipping Information")
    enter_shipping.properties["position"] = {"x": 350, "y": 260}
    diagram.add_node_to_swimlane(enter_shipping, customer_lane)
    
    select_payment = diagram.create_action_node("Select Payment Method")
    select_payment.properties["position"] = {"x": 350, "y": 340}
    diagram.add_node_to_swimlane(select_payment, customer_lane)
    
    # Decision node - registered user?
    registered_decision = diagram.create_decision_node("Registered User?")
    registered_decision.properties["position"] = {"x": 650, "y": 180}
    diagram.add_node_to_swimlane(registered_decision, system_lane)
    
    # System actions
    load_saved_info = diagram.create_action_node("Load Saved Info")
    load_saved_info.properties["position"] = {"x": 750, "y": 180}
    diagram.add_node_to_swimlane(load_saved_info, system_lane)
    
    merge_node = diagram.create_merge_node()
    merge_node.properties["position"] = {"x": 650, "y": 260}
    diagram.add_node_to_swimlane(merge_node, system_lane)
    
    calculate_total = diagram.create_action_node("Calculate Total")
    calculate_total.properties["position"] = {"x": 650, "y": 340}
    diagram.add_node_to_swimlane(calculate_total, system_lane)
    
    # Fork and process payment in parallel
    fork_node = diagram.create_fork_node()
    fork_node.properties["position"] = {"x": 650, "y": 420}
    fork_node.properties["width"] = 100  # Make this a horizontal bar
    fork_node.properties["height"] = 10
    diagram.add_node_to_swimlane(fork_node, system_lane)
    
    process_order = diagram.create_action_node("Process Order")
    process_order.properties["position"] = {"x": 550, "y": 460}
    diagram.add_node_to_swimlane(process_order, system_lane)
    
    send_confirmation = diagram.create_action_node("Send Email Confirmation")
    send_confirmation.properties["position"] = {"x": 750, "y": 460}
    diagram.add_node_to_swimlane(send_confirmation, system_lane)
    
    # Join node
    join_node = diagram.create_join_node()
    join_node.properties["position"] = {"x": 650, "y": 540}
    join_node.properties["width"] = 100  # Make this a horizontal bar
    join_node.properties["height"] = 10
    diagram.add_node_to_swimlane(join_node, system_lane)
    
    # Payment processor action
    process_payment = diagram.create_action_node("Process Payment")
    process_payment.properties["position"] = {"x": 650, "y": 460}
    diagram.add_node_to_swimlane(process_payment, payment_lane)
    
    # Object node for the order
    order_object = diagram.create_object_node("Order", "Completed")
    order_object.properties["position"] = {"x": 650, "y": 580}
    diagram.add_node_to_swimlane(order_object, system_lane)
    
    # Final node
    final = diagram.create_activity_final_node()
    final.properties["position"] = {"x": 650, "y": 660}
    diagram.add_node_to_swimlane(final, customer_lane)
    
    # Connect the nodes with edges
    diagram.create_edge(initial, review_cart)
    diagram.create_edge(review_cart, proceed_checkout)
    diagram.create_edge(proceed_checkout, registered_decision)
    
    diagram.create_edge(registered_decision, load_saved_info, "yes")
    diagram.create_edge(registered_decision, merge_node, "no")
    diagram.create_edge(load_saved_info, merge_node)
    
    diagram.create_edge(merge_node, enter_shipping)
    diagram.create_edge(enter_shipping, select_payment)
    diagram.create_edge(select_payment, calculate_total)
    diagram.create_edge(calculate_total, fork_node)
    
    diagram.create_edge(fork_node, process_order)
    diagram.create_edge(fork_node, process_payment)
    diagram.create_edge(fork_node, send_confirmation)
    
    diagram.create_edge(process_order, join_node)
    diagram.create_edge(process_payment, join_node)
    diagram.create_edge(send_confirmation, join_node)
    
    diagram.create_edge(join_node, order_object)
    diagram.create_edge(order_object, final)
    
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram to SVG
    output_path = diagram.render("output/checkout_activity_diagram.svg")
    print(f"Diagram rendered to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    create_example_activity_diagram() 