"""
Tests for the Use Case Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import UseCaseDiagram
from pydiagrams.diagrams.uml.usecase_diagram import (
    Actor, UseCase, System, UseCaseRelationship, UseCaseRelationshipType
)


class TestUseCaseDiagram(unittest.TestCase):
    """Test cases for the UseCaseDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = UseCaseDiagram("Test Use Case Diagram")
    
    def test_actor_creation(self):
        """Test that an actor can be created and added to the diagram."""
        actor = self.diagram.create_actor("Test Actor")
        
        # Check that the actor was added to the diagram
        self.assertEqual(len(self.diagram.actors), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.actors[0], Actor)
        self.assertEqual(self.diagram.actors[0].name, "Test Actor")
        self.assertTrue(self.diagram.actors[0].is_primary)  # Default is primary
    
    def test_actor_creation_with_primary_flag(self):
        """Test that an actor can be created with a specified primary flag."""
        actor = self.diagram.create_actor("Secondary Actor", is_primary=False)
        
        # Check that the actor was added to the diagram
        self.assertEqual(len(self.diagram.actors), 1)
        self.assertFalse(self.diagram.actors[0].is_primary)
    
    def test_use_case_creation(self):
        """Test that a use case can be created and added to the diagram."""
        use_case = self.diagram.create_use_case("Test Use Case", "Description")
        
        # Check that the use case was added to the diagram
        self.assertEqual(len(self.diagram.use_cases), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.use_cases[0], UseCase)
        self.assertEqual(self.diagram.use_cases[0].name, "Test Use Case")
        self.assertEqual(self.diagram.use_cases[0].description, "Description")
    
    def test_system_creation(self):
        """Test that a system boundary can be created and added to the diagram."""
        system = self.diagram.create_system("Test System")
        
        # Check that the system was added to the diagram
        self.assertEqual(len(self.diagram.systems), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.systems[0], System)
        self.assertEqual(self.diagram.systems[0].name, "Test System")
    
    def test_add_use_case_to_system(self):
        """Test that a use case can be added to a system boundary."""
        system = self.diagram.create_system("Test System")
        use_case = self.diagram.create_use_case("Test Use Case")
        
        # Add the use case to the system
        self.diagram.add_use_case_to_system(use_case, system)
        
        # Check that the use case was added to the system
        self.assertEqual(len(system.use_cases), 1)
        self.assertEqual(system.use_cases[0], use_case)
    
    def test_association_creation(self):
        """Test that an association can be created between an actor and a use case."""
        actor = self.diagram.create_actor("Test Actor")
        use_case = self.diagram.create_use_case("Test Use Case")
        
        # Create an association
        association = self.diagram.create_association(actor, use_case)
        
        # Check that the association was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.relationships[0], UseCaseRelationship)
        self.assertEqual(association.source, actor)
        self.assertEqual(association.target, use_case)
        self.assertEqual(association.relationship_type, UseCaseRelationshipType.ASSOCIATION)
        
        # Check that the association was registered with the actor and use case
        self.assertEqual(len(actor.associations), 1)
        self.assertEqual(len(use_case.associations), 1)
        self.assertEqual(actor.associations[0], association)
        self.assertEqual(use_case.associations[0], association)
    
    def test_include_creation(self):
        """Test that an include relationship can be created between use cases."""
        base = self.diagram.create_use_case("Base Use Case")
        inclusion = self.diagram.create_use_case("Included Use Case")
        
        # Create an include relationship
        include = self.diagram.create_include(base, inclusion, "Test include")
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.relationships[0], UseCaseRelationship)
        self.assertEqual(include.source, base)
        self.assertEqual(include.target, inclusion)
        self.assertEqual(include.relationship_type, UseCaseRelationshipType.INCLUDE)
        self.assertEqual(include.description, "Test include")
        
        # Check that the relationship was registered with the base use case
        self.assertEqual(len(base.includes), 1)
        self.assertEqual(base.includes[0], include)
    
    def test_extend_creation(self):
        """Test that an extend relationship can be created between use cases."""
        extension = self.diagram.create_use_case("Extension Use Case")
        base = self.diagram.create_use_case("Base Use Case")
        
        # Create an extend relationship
        extend = self.diagram.create_extend(extension, base, "Test extend")
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.relationships[0], UseCaseRelationship)
        self.assertEqual(extend.source, extension)
        self.assertEqual(extend.target, base)
        self.assertEqual(extend.relationship_type, UseCaseRelationshipType.EXTEND)
        self.assertEqual(extend.description, "Test extend")
        
        # Check that the relationship was registered with the extension use case
        self.assertEqual(len(extension.extends), 1)
        self.assertEqual(extension.extends[0], extend)
    
    def test_generalization_creation_between_actors(self):
        """Test that a generalization can be created between actors."""
        parent = self.diagram.create_actor("Parent Actor")
        child = self.diagram.create_actor("Child Actor")
        
        # Create a generalization relationship
        generalization = self.diagram.create_generalization(child, parent)
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.relationships[0], UseCaseRelationship)
        self.assertEqual(generalization.source, child)
        self.assertEqual(generalization.target, parent)
        self.assertEqual(generalization.relationship_type, UseCaseRelationshipType.GENERALIZATION)
        
        # Check that the relationship was registered with the actors
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)
        self.assertEqual(child.parent, parent)
    
    def test_generalization_creation_between_use_cases(self):
        """Test that a generalization can be created between use cases."""
        parent = self.diagram.create_use_case("Parent Use Case")
        child = self.diagram.create_use_case("Child Use Case")
        
        # Create a generalization relationship
        generalization = self.diagram.create_generalization(child, parent)
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.relationships[0], UseCaseRelationship)
        self.assertEqual(generalization.source, child)
        self.assertEqual(generalization.target, parent)
        self.assertEqual(generalization.relationship_type, UseCaseRelationshipType.GENERALIZATION)
        
        # Check that the relationship was registered with the use cases
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0], child)
        self.assertEqual(child.parent, parent)
    
    def test_generalization_validation(self):
        """Test that generalization requires source and target of the same type."""
        actor = self.diagram.create_actor("Actor")
        use_case = self.diagram.create_use_case("Use Case")
        
        # Check that creating a generalization between different types raises an error
        with self.assertRaises(ValueError):
            self.diagram.create_generalization(actor, use_case)
    
    def test_use_case_with_flows(self):
        """Test that a use case can have preconditions, postconditions, and flows."""
        use_case = self.diagram.create_use_case("Test Use Case")
        
        # Add preconditions
        use_case.add_precondition("User is logged in")
        use_case.add_precondition("User has items in cart")
        
        # Add postconditions
        use_case.add_postcondition("Order is placed")
        use_case.add_postcondition("Inventory is updated")
        
        # Add main flow steps
        use_case.add_main_flow_step("User confirms order details")
        use_case.add_main_flow_step("User enters payment information")
        use_case.add_main_flow_step("System processes payment")
        
        # Add alternative flow
        use_case.add_alt_flow("Payment failure", [
            "Payment is declined",
            "System displays error message",
            "User is prompted to try another payment method"
        ])
        
        # Check that everything was added correctly
        self.assertEqual(len(use_case.preconditions), 2)
        self.assertEqual(len(use_case.postconditions), 2)
        self.assertEqual(len(use_case.main_flow), 3)
        self.assertEqual(len(use_case.alt_flows), 1)
        self.assertEqual(len(use_case.alt_flows["Payment failure"]), 3)
    
    def test_actor_with_description(self):
        """Test that an actor can have a description."""
        actor = self.diagram.create_actor("Test Actor")
        actor.set_description("This is a test actor description")
        
        # Check that the description was set
        self.assertEqual(actor.description, "This is a test actor description")
    
    def test_to_dict(self):
        """Test that the diagram can be converted to a dictionary."""
        # Create a simple use case diagram
        actor = self.diagram.create_actor("Test Actor")
        use_case = self.diagram.create_use_case("Test Use Case")
        association = self.diagram.create_association(actor, use_case)
        
        # Convert to dictionary
        diagram_dict = self.diagram.to_dict()
        
        # Check dictionary contents
        self.assertEqual(diagram_dict["name"], "Test Use Case Diagram")
        self.assertEqual(len(diagram_dict["elements"]), 2)  # Actor and use case
        self.assertEqual(len(diagram_dict["relationships"]), 1)  # Association


if __name__ == "__main__":
    unittest.main() 