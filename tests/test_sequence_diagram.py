"""
Tests for the Sequence Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import SequenceDiagram
from pydiagrams.diagrams.uml.sequence_diagram import Lifeline, Message, Activation, MessageType, Fragment


class TestSequenceDiagram(unittest.TestCase):
    """Test cases for the SequenceDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = SequenceDiagram("Test Sequence Diagram")
        
    def test_lifeline_creation(self):
        """Test that a lifeline can be created and added to the diagram."""
        test_lifeline = Lifeline("TestLifeline")
        
        self.diagram.add_lifeline(test_lifeline)
        
        # Check that the lifeline was added to the diagram
        self.assertEqual(len(self.diagram.lifelines), 1)
        self.assertEqual(self.diagram.lifelines[0].name, "TestLifeline")
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertEqual(self.diagram.elements[0], test_lifeline)
        
    def test_actor_lifeline(self):
        """Test that an actor lifeline can be created."""
        actor = self.diagram.create_lifeline("TestActor", is_actor=True)
        
        # Check that the actor was created correctly
        self.assertEqual(actor.name, "TestActor")
        self.assertTrue(actor.is_actor)
        self.assertEqual(len(self.diagram.lifelines), 1)
        self.assertEqual(self.diagram.lifelines[0], actor)
        
    def test_lifeline_with_stereotype(self):
        """Test that a lifeline with stereotype can be created."""
        lifeline = self.diagram.create_lifeline("TestLifeline", stereotype="«boundary»")
        
        # Check that the stereotype was set correctly
        self.assertEqual(lifeline.stereotype, "«boundary»")
        
    def test_activation_creation(self):
        """Test that activations can be added to lifelines."""
        lifeline = self.diagram.create_lifeline("TestLifeline")
        
        # Add an activation
        activation = lifeline.add_activation(100, 200)
        
        # Check that the activation was added
        self.assertEqual(len(lifeline.activations), 1)
        self.assertEqual(activation.lifeline, lifeline)
        self.assertEqual(activation.start_time, 100)
        self.assertEqual(activation.end_time, 200)
        
    def test_nested_activation(self):
        """Test that nested activations can be created."""
        lifeline = self.diagram.create_lifeline("TestLifeline")
        
        # Add a parent activation
        parent = lifeline.add_activation(100, 200)
        
        # Add a nested activation
        nested = parent.add_nested_activation(120, 180)
        
        # Check that the nested activation was added correctly
        self.assertEqual(len(parent.nested_activations), 1)
        self.assertEqual(nested.lifeline, lifeline)
        self.assertEqual(nested.start_time, 120)
        self.assertEqual(nested.end_time, 180)
        
    def test_message_creation(self):
        """Test that messages can be created between lifelines."""
        lifeline1 = self.diagram.create_lifeline("Source")
        lifeline2 = self.diagram.create_lifeline("Target")
        
        # Create a message
        message = self.diagram.create_message(
            lifeline1, 
            lifeline2, 
            "Test Message", 
            MessageType.SYNCHRONOUS, 
            150
        )
        
        # Check that the message was created and added correctly
        self.assertEqual(len(self.diagram.messages), 1)
        self.assertEqual(message.source, lifeline1)
        self.assertEqual(message.target, lifeline2)
        self.assertEqual(message.name, "Test Message")
        self.assertEqual(message.message_type, MessageType.SYNCHRONOUS)
        self.assertEqual(message.time_point, 150)
        
    def test_fragment_creation(self):
        """Test that fragments can be created."""
        # Create a fragment
        fragment = self.diagram.create_fragment(
            "Test Fragment",
            Fragment.FragmentType.LOOP,
            100,
            200,
            "i < 10"
        )
        
        # Check that the fragment was created and added correctly
        self.assertEqual(len(self.diagram.fragments), 1)
        self.assertEqual(fragment.name, "Test Fragment")
        self.assertEqual(fragment.fragment_type, Fragment.FragmentType.LOOP)
        self.assertEqual(fragment.start_time, 100)
        self.assertEqual(fragment.end_time, 200)
        self.assertEqual(fragment.condition, "i < 10")
        
    def test_fragment_with_operands(self):
        """Test that fragments can have operands."""
        # Create an alt fragment
        fragment = self.diagram.create_fragment(
            "Test Alt",
            Fragment.FragmentType.ALT,
            100,
            300,
            "x > 0"
        )
        
        # Add operands
        fragment.add_operand("x == 0", 200)
        fragment.add_operand("x < 0", 250)
        
        # Check that the operands were added correctly
        self.assertEqual(len(fragment.operands), 2)
        self.assertEqual(fragment.operands[0], ("x == 0", 200))
        self.assertEqual(fragment.operands[1], ("x < 0", 250))
        
    def test_to_dict(self):
        """Test that the diagram can be converted to a dictionary."""
        # Create a simple sequence diagram
        lifeline1 = self.diagram.create_lifeline("Source")
        lifeline2 = self.diagram.create_lifeline("Target")
        
        lifeline1.add_activation(100, 200)
        
        self.diagram.create_message(
            lifeline1, 
            lifeline2, 
            "Test Message", 
            MessageType.SYNCHRONOUS, 
            150
        )
        
        # Convert to dictionary
        diagram_dict = self.diagram.to_dict()
        
        # Check dictionary contents
        self.assertEqual(diagram_dict["name"], "Test Sequence Diagram")
        self.assertEqual(len(diagram_dict["elements"]), 2)  # two lifelines
        self.assertEqual(len(diagram_dict["relationships"]), 1)  # one message
        
        # Check element types
        elements = diagram_dict["elements"]
        self.assertEqual(elements[0]["type"], "lifeline")
        self.assertEqual(elements[1]["type"], "lifeline")
        
        # Check relationship type
        relationships = diagram_dict["relationships"]
        self.assertEqual(relationships[0]["type"], "message")
        self.assertEqual(relationships[0]["message_type"], "synchronous")


if __name__ == "__main__":
    unittest.main() 