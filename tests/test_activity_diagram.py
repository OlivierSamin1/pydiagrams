"""
Tests for the Activity Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import ActivityDiagram
from pydiagrams.diagrams.uml.activity_diagram import (
    ActivityNode, InitialNode, ActionNode, DecisionNode, MergeNode,
    ForkNode, JoinNode, ActivityFinalNode, ObjectNode, Swimlane,
    ActivityEdge
)


class TestActivityDiagram(unittest.TestCase):
    """Test cases for the ActivityDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = ActivityDiagram("Test Activity Diagram")
        
    def test_initial_node_creation(self):
        """Test that an initial node can be created and added to the diagram."""
        initial = self.diagram.create_initial_node()
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.nodes[0], InitialNode)
        
    def test_action_node_creation(self):
        """Test that an action node can be created and added to the diagram."""
        action = self.diagram.create_action_node("Test Action")
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertEqual(self.diagram.nodes[0].name, "Test Action")
        self.assertIsInstance(self.diagram.nodes[0], ActionNode)
        
    def test_decision_node_creation(self):
        """Test that a decision node can be created and added to the diagram."""
        decision = self.diagram.create_decision_node("Test Decision")
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertEqual(self.diagram.nodes[0].name, "Test Decision")
        self.assertIsInstance(self.diagram.nodes[0], DecisionNode)
        
    def test_merge_node_creation(self):
        """Test that a merge node can be created and added to the diagram."""
        merge = self.diagram.create_merge_node()
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertIsInstance(self.diagram.nodes[0], MergeNode)
        
    def test_fork_node_creation(self):
        """Test that a fork node can be created and added to the diagram."""
        fork = self.diagram.create_fork_node()
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertIsInstance(self.diagram.nodes[0], ForkNode)
        
    def test_join_node_creation(self):
        """Test that a join node can be created and added to the diagram."""
        join = self.diagram.create_join_node()
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertIsInstance(self.diagram.nodes[0], JoinNode)
        
    def test_object_node_creation(self):
        """Test that an object node can be created and added to the diagram."""
        obj = self.diagram.create_object_node("TestObject", "Active")
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertEqual(self.diagram.nodes[0].name, "TestObject")
        self.assertEqual(self.diagram.nodes[0].state, "Active")
        self.assertIsInstance(self.diagram.nodes[0], ObjectNode)
        
    def test_activity_final_node_creation(self):
        """Test that an activity final node can be created and added to the diagram."""
        final = self.diagram.create_activity_final_node()
        
        # Check that the node was added to the diagram
        self.assertEqual(len(self.diagram.nodes), 1)
        self.assertIsInstance(self.diagram.nodes[0], ActivityFinalNode)
        
    def test_edge_creation(self):
        """Test that edges can be created between nodes."""
        action1 = self.diagram.create_action_node("Action1")
        action2 = self.diagram.create_action_node("Action2")
        
        # Create an edge
        edge = self.diagram.create_edge(action1, action2)
        
        # Check that the edge was added to the diagram
        self.assertEqual(len(self.diagram.edges), 1)
        self.assertEqual(edge.source, action1)
        self.assertEqual(edge.target, action2)
        
        # Check that the edge was registered with the nodes
        self.assertEqual(len(action1.outgoing_edges), 1)
        self.assertEqual(len(action2.incoming_edges), 1)
        self.assertEqual(action1.outgoing_edges[0], edge)
        self.assertEqual(action2.incoming_edges[0], edge)
        
    def test_edge_with_guard(self):
        """Test that edges can have guard conditions."""
        decision = self.diagram.create_decision_node()
        action1 = self.diagram.create_action_node("Action1")
        
        # Create an edge with a guard
        edge = self.diagram.create_edge(decision, action1, "x > 0")
        
        # Check the guard condition
        self.assertEqual(edge.guard, "x > 0")
        
    def test_swimlane_creation(self):
        """Test that swimlanes can be created and nodes added to them."""
        # Create a swimlane
        swimlane = self.diagram.create_swimlane("TestLane")
        
        # Create a node
        action = self.diagram.create_action_node("Action")
        
        # Add the node to the swimlane
        self.diagram.add_node_to_swimlane(action, swimlane)
        
        # Check that the node was added to the swimlane
        self.assertEqual(len(swimlane.nodes), 1)
        self.assertEqual(swimlane.nodes[0], action)
        
    def test_to_dict(self):
        """Test that the diagram can be converted to a dictionary."""
        # Create a simple activity diagram
        initial = self.diagram.create_initial_node()
        action = self.diagram.create_action_node("TestAction")
        edge = self.diagram.create_edge(initial, action)
        
        # Convert to dictionary
        diagram_dict = self.diagram.to_dict()
        
        # Check dictionary contents
        self.assertEqual(diagram_dict["name"], "Test Activity Diagram")
        self.assertEqual(len(diagram_dict["elements"]), 2)  # Two nodes
        self.assertEqual(len(diagram_dict["relationships"]), 1)  # One edge
        
        # Check node types
        element_types = [e["type"] for e in diagram_dict["elements"]]
        self.assertIn("activity_node", element_types)
        
        # Check node_types
        node_types = [e.get("node_type") for e in diagram_dict["elements"] if e.get("type") == "activity_node"]
        self.assertIn("initial", node_types)
        self.assertIn("action", node_types)
        
        # Check edge type
        self.assertEqual(diagram_dict["relationships"][0]["type"], "activity_edge")


if __name__ == "__main__":
    unittest.main() 