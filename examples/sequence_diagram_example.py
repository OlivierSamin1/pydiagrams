#!/usr/bin/env python3
"""
Sequence Diagram Example for PyDiagrams

This example demonstrates how to create a UML Sequence Diagram using the PyDiagrams library.
"""

import os
import sys

# Add the parent directory to sys.path to import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import SequenceDiagram
from pydiagrams.diagrams.uml.sequence_diagram import Lifeline, Message, Fragment, MessageType


def create_example_sequence_diagram():
    """Create an example sequence diagram of a login system."""
    
    # Create the diagram
    diagram = SequenceDiagram("Login System Sequence Diagram")
    
    # Create lifelines
    user = diagram.create_lifeline("User", is_actor=True)
    ui = diagram.create_lifeline("LoginScreen", stereotype="«boundary»")
    controller = diagram.create_lifeline("AuthController", stereotype="«control»")
    service = diagram.create_lifeline("AuthService", stereotype="«service»")
    db = diagram.create_lifeline("Database", stereotype="«database»")
    
    # Start activations
    # User is active throughout the sequence
    user_activation = user.add_activation(100, 350)
    ui_activation = ui.add_activation(120, 330)
    
    # Create messages
    # User enters credentials
    diagram.create_message(
        user, 
        ui, 
        "Enter username and password", 
        MessageType.SYNCHRONOUS, 
        120
    )
    
    # UI calls controller
    controller_activation = controller.add_activation(140, 310)
    diagram.create_message(
        ui, 
        controller, 
        "login(username, password)", 
        MessageType.SYNCHRONOUS, 
        140
    )
    
    # Controller calls service
    service_activation = service.add_activation(160, 290)
    diagram.create_message(
        controller, 
        service, 
        "authenticate(username, password)", 
        MessageType.SYNCHRONOUS, 
        160
    )
    
    # Service queries database
    db_activation = db.add_activation(180, 220)
    diagram.create_message(
        service, 
        db, 
        "findUser(username)", 
        MessageType.SYNCHRONOUS, 
        180
    )
    
    # Database returns user
    diagram.create_message(
        db, 
        service, 
        "return User", 
        MessageType.REPLY, 
        220
    )
    
    # Create a fragment for the password verification
    fragment = diagram.create_fragment(
        "Password Verification",
        Fragment.FragmentType.ALT,
        230, 
        280,
        "password_matches"
    )
    fragment.add_operand("else", 260)
    
    # Successful case
    diagram.create_message(
        service, 
        service, 
        "verifyPassword(password, hash)", 
        MessageType.SELF, 
        240
    )
    
    # Failure case (inside the 'else' operand)
    diagram.create_message(
        service, 
        controller, 
        "return Authentication Failed", 
        MessageType.REPLY, 
        270
    )
    
    # Service returns to controller
    diagram.create_message(
        service, 
        controller, 
        "return Authentication Success", 
        MessageType.REPLY, 
        290
    )
    
    # Controller returns to UI
    diagram.create_message(
        controller, 
        ui, 
        "return Login Result", 
        MessageType.REPLY, 
        310
    )
    
    # UI displays result to user
    diagram.create_message(
        ui, 
        user, 
        "Show login result", 
        MessageType.REPLY, 
        330
    )
    
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Render the diagram to SVG
    output_path = diagram.render("output/login_sequence_diagram.svg")
    print(f"Diagram rendered to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    create_example_sequence_diagram() 