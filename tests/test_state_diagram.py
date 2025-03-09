"""
Tests for the State Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import StateDiagram
from pydiagrams.diagrams.uml.state_diagram import (
    StateType, TransitionType, State, InitialState, FinalState,
    CompositeState, ChoicePseudostate, JunctionPseudostate,
    EntryPointPseudostate, ExitPointPseudostate, HistoryPseudostate,
    TerminatePseudostate, Transition, Region
)


class TestStateDiagram(unittest.TestCase):
    """Test cases for the StateDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = StateDiagram("Test State Diagram")
    
    def test_initial_state_creation(self):
        """Test that an initial state can be created and added to the diagram."""
        initial = self.diagram.create_initial_state()
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], InitialState)
        self.assertEqual(self.diagram.states[0].state_type, StateType.INITIAL)
    
    def test_final_state_creation(self):
        """Test that a final state can be created and added to the diagram."""
        final = self.diagram.create_final_state()
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], FinalState)
        self.assertEqual(self.diagram.states[0].state_type, StateType.FINAL)
    
    def test_state_creation(self):
        """Test that a simple state can be created and added to the diagram."""
        state = self.diagram.create_state("Test State")
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], State)
        self.assertEqual(self.diagram.states[0].name, "Test State")
        self.assertEqual(self.diagram.states[0].state_type, StateType.SIMPLE)
    
    def test_composite_state_creation(self):
        """Test that a composite state can be created and added to the diagram."""
        composite = self.diagram.create_composite_state("Composite State")
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], CompositeState)
        self.assertEqual(self.diagram.states[0].name, "Composite State")
        self.assertEqual(self.diagram.states[0].state_type, StateType.COMPOSITE)
    
    def test_composite_state_with_substates(self):
        """Test that substates can be added to a composite state."""
        composite = self.diagram.create_composite_state("Composite State")
        substate = self.diagram.create_state("Substate")
        
        # Add the substate to the composite state
        composite.add_substate(substate)
        
        # Check that the substate was added to the composite state
        self.assertEqual(len(composite.substates), 1)
        self.assertEqual(composite.substates[0], substate)
        self.assertEqual(substate.parent, composite)
    
    def test_choice_pseudostate_creation(self):
        """Test that a choice pseudostate can be created and added to the diagram."""
        choice = self.diagram.create_choice_pseudostate()
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], ChoicePseudostate)
        self.assertEqual(self.diagram.states[0].state_type, StateType.CHOICE)
    
    def test_junction_pseudostate_creation(self):
        """Test that a junction pseudostate can be created and added to the diagram."""
        junction = self.diagram.create_junction_pseudostate()
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], JunctionPseudostate)
        self.assertEqual(self.diagram.states[0].state_type, StateType.JUNCTION)
    
    def test_entry_point_creation(self):
        """Test that an entry point can be created and added to the diagram."""
        entry = self.diagram.create_entry_point("Entry")
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], EntryPointPseudostate)
        self.assertEqual(self.diagram.states[0].name, "Entry")
        self.assertEqual(self.diagram.states[0].state_type, StateType.ENTRY_POINT)
    
    def test_exit_point_creation(self):
        """Test that an exit point can be created and added to the diagram."""
        exit_point = self.diagram.create_exit_point("Exit")
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], ExitPointPseudostate)
        self.assertEqual(self.diagram.states[0].name, "Exit")
        self.assertEqual(self.diagram.states[0].state_type, StateType.EXIT_POINT)
    
    def test_history_state_creation(self):
        """Test that history states can be created and added to the diagram."""
        shallow = self.diagram.create_history_state(is_deep=False)
        deep = self.diagram.create_history_state(is_deep=True)
        
        # Check that both states were added to the diagram
        self.assertEqual(len(self.diagram.states), 2)
        self.assertEqual(len(self.diagram.elements), 2)
        
        # Check the shallow history state
        self.assertIsInstance(self.diagram.states[0], HistoryPseudostate)
        self.assertEqual(self.diagram.states[0].state_type, StateType.SHALLOW_HISTORY)
        self.assertFalse(self.diagram.states[0].is_deep)
        
        # Check the deep history state
        self.assertIsInstance(self.diagram.states[1], HistoryPseudostate)
        self.assertEqual(self.diagram.states[1].state_type, StateType.DEEP_HISTORY)
        self.assertTrue(self.diagram.states[1].is_deep)
    
    def test_terminate_pseudostate_creation(self):
        """Test that a terminate pseudostate can be created and added to the diagram."""
        terminate = self.diagram.create_terminate_pseudostate()
        
        # Check that the state was added to the diagram
        self.assertEqual(len(self.diagram.states), 1)
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertIsInstance(self.diagram.states[0], TerminatePseudostate)
        self.assertEqual(self.diagram.states[0].state_type, StateType.TERMINATE)
    
    def test_transition_creation(self):
        """Test that transitions can be created between states."""
        source = self.diagram.create_state("Source")
        target = self.diagram.create_state("Target")
        
        # Create a transition
        transition = self.diagram.create_transition(
            source, target, 
            trigger="event", 
            guard="condition", 
            effect="action"
        )
        
        # Check that the transition was added to the diagram
        self.assertEqual(len(self.diagram.transitions), 1)
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertIsInstance(self.diagram.transitions[0], Transition)
        
        # Check the transition properties
        self.assertEqual(transition.source, source)
        self.assertEqual(transition.target, target)
        self.assertEqual(transition.trigger, "event")
        self.assertEqual(transition.guard, "condition")
        self.assertEqual(transition.effect, "action")
        self.assertEqual(transition.transition_type, TransitionType.EXTERNAL)
        
        # Check that the transition was registered with the states
        self.assertEqual(len(source.outgoing_transitions), 1)
        self.assertEqual(len(target.incoming_transitions), 1)
        self.assertEqual(source.outgoing_transitions[0], transition)
        self.assertEqual(target.incoming_transitions[0], transition)
    
    def test_region_creation(self):
        """Test that regions can be created and states added to them."""
        region = self.diagram.create_region("TestRegion")
        state = self.diagram.create_state("TestState")
        
        # Add the state to the region
        region.add_state(state)
        
        # Check that the region was added to the diagram
        self.assertEqual(len(self.diagram.regions), 1)
        self.assertEqual(self.diagram.regions[0].name, "TestRegion")
        
        # Check that the state was added to the region
        self.assertEqual(len(region.states), 1)
        self.assertEqual(region.states[0], state)
    
    def test_state_activities(self):
        """Test that activities can be added to states."""
        state = self.diagram.create_state("TestState")
        
        # Add activities
        state.add_entry_activity("entry_action()")
        state.add_do_activity("do_action()")
        state.add_exit_activity("exit_action()")
        
        # Check that activities were added
        self.assertEqual(len(state.entry_activities), 1)
        self.assertEqual(len(state.do_activities), 1)
        self.assertEqual(len(state.exit_activities), 1)
        self.assertEqual(state.entry_activities[0], "entry_action()")
        self.assertEqual(state.do_activities[0], "do_action()")
        self.assertEqual(state.exit_activities[0], "exit_action()")
    
    def test_internal_transitions(self):
        """Test that internal transitions can be added to states."""
        state = self.diagram.create_state("TestState")
        
        # Add internal transitions
        state.add_internal_transition("event1", "action1()")
        state.add_internal_transition("event2", "action2()")
        
        # Check that internal transitions were added
        self.assertEqual(len(state.internal_transitions), 2)
        self.assertEqual(state.internal_transitions["event1"], "action1()")
        self.assertEqual(state.internal_transitions["event2"], "action2()")
    
    def test_to_dict(self):
        """Test that the diagram can be converted to a dictionary."""
        # Create a simple state diagram
        initial = self.diagram.create_initial_state()
        state = self.diagram.create_state("TestState")
        transition = self.diagram.create_transition(initial, state)
        
        # Convert to dictionary
        diagram_dict = self.diagram.to_dict()
        
        # Check dictionary contents
        self.assertEqual(diagram_dict["name"], "Test State Diagram")
        self.assertEqual(len(diagram_dict["elements"]), 2)  # Two states
        self.assertEqual(len(diagram_dict["relationships"]), 1)  # One transition


if __name__ == "__main__":
    unittest.main() 