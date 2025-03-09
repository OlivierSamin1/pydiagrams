"""
State Diagram module for UML state diagrams.

This module provides classes for creating and manipulating UML State Diagrams.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Set, Union

from pydiagrams.core.base import BaseDiagram, DiagramElement
from pydiagrams.core.base import Relationship
from pydiagrams.core.layout import Layout


class StateType(Enum):
    """Types of states in a state diagram."""
    INITIAL = "initial"
    FINAL = "final"
    SIMPLE = "simple"
    COMPOSITE = "composite"
    SUBMACHINE = "submachine"
    CHOICE = "choice"
    JUNCTION = "junction"
    ENTRY_POINT = "entry_point"
    EXIT_POINT = "exit_point"
    TERMINATE = "terminate"
    SHALLOW_HISTORY = "shallow_history"
    DEEP_HISTORY = "deep_history"


class TransitionType(Enum):
    """Types of transitions in a state diagram."""
    EXTERNAL = "external"
    INTERNAL = "internal"
    LOCAL = "local"


class State(DiagramElement):
    """
    Represents a state in a UML State Diagram.
    
    A state can have entry, exit, and do activities, and can contain
    sub-states in case of composite or submachine states.
    """
    
    def __init__(
        self,
        name: str,
        state_type: StateType = StateType.SIMPLE,
        element_id: Optional[str] = None
    ):
        """
        Initialize a state in a UML State Diagram.
        
        Args:
            name: The name of the state.
            state_type: The type of state (simple, composite, etc.)
            element_id: Optional unique identifier for the state.
        """
        super().__init__(name, element_id)
        self.state_type = state_type
        self.parent: Optional['State'] = None
        self.substates: List['State'] = []
        self.entry_activities: List[str] = []
        self.exit_activities: List[str] = []
        self.do_activities: List[str] = []
        self.internal_transitions: Dict[str, str] = {}  # event: action
        self.incoming_transitions: List['Transition'] = []
        self.outgoing_transitions: List['Transition'] = []
    
    def add_entry_activity(self, activity: str) -> None:
        """Add an entry activity to the state."""
        self.entry_activities.append(activity)
    
    def add_exit_activity(self, activity: str) -> None:
        """Add an exit activity to the state."""
        self.exit_activities.append(activity)
    
    def add_do_activity(self, activity: str) -> None:
        """Add a do activity to the state."""
        self.do_activities.append(activity)
    
    def add_internal_transition(self, event: str, action: str) -> None:
        """Add an internal transition to the state."""
        self.internal_transitions[event] = action
    
    def add_substate(self, state: 'State') -> None:
        """Add a substate to this state (for composite states)."""
        if self.state_type not in [StateType.COMPOSITE, StateType.SUBMACHINE]:
            self.state_type = StateType.COMPOSITE
        
        state.parent = self
        self.substates.append(state)
    
    def add_incoming_transition(self, transition: 'Transition') -> None:
        """Add an incoming transition to this state."""
        self.incoming_transitions.append(transition)
    
    def add_outgoing_transition(self, transition: 'Transition') -> None:
        """Add an outgoing transition from this state."""
        self.outgoing_transitions.append(transition)
    
    def render(self) -> Dict:
        """
        Render the state as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the state.
        """
        data = {
            "id": self.id,
            "type": "state",
            "state_type": self.state_type.value,
            "name": self.name,
            "entry_activities": self.entry_activities,
            "exit_activities": self.exit_activities,
            "do_activities": self.do_activities,
            "internal_transitions": self.internal_transitions,
        }
        
        if self.substates:
            data["substates"] = [state.render() for state in self.substates]
        
        return data


class InitialState(State):
    """Represents an initial pseudostate in a UML State Diagram."""
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize an initial pseudostate.
        
        Args:
            element_id: Optional unique identifier for the state.
        """
        super().__init__("", StateType.INITIAL, element_id)


class FinalState(State):
    """Represents a final state in a UML State Diagram."""
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize a final state.
        
        Args:
            element_id: Optional unique identifier for the state.
        """
        super().__init__("", StateType.FINAL, element_id)


class CompositeState(State):
    """Represents a composite state in a UML State Diagram."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a composite state.
        
        Args:
            name: The name of the composite state.
            element_id: Optional unique identifier for the state.
        """
        super().__init__(name, StateType.COMPOSITE, element_id)


class ChoicePseudostate(State):
    """Represents a choice pseudostate in a UML State Diagram."""
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize a choice pseudostate.
        
        Args:
            element_id: Optional unique identifier for the state.
        """
        super().__init__("", StateType.CHOICE, element_id)


class JunctionPseudostate(State):
    """Represents a junction pseudostate in a UML State Diagram."""
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize a junction pseudostate.
        
        Args:
            element_id: Optional unique identifier for the state.
        """
        super().__init__("", StateType.JUNCTION, element_id)


class EntryPointPseudostate(State):
    """Represents an entry point pseudostate in a UML State Diagram."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an entry point pseudostate.
        
        Args:
            name: The name of the entry point.
            element_id: Optional unique identifier for the state.
        """
        super().__init__(name, StateType.ENTRY_POINT, element_id)


class ExitPointPseudostate(State):
    """Represents an exit point pseudostate in a UML State Diagram."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an exit point pseudostate.
        
        Args:
            name: The name of the exit point.
            element_id: Optional unique identifier for the state.
        """
        super().__init__(name, StateType.EXIT_POINT, element_id)


class HistoryPseudostate(State):
    """Represents a history pseudostate (shallow or deep) in a UML State Diagram."""
    
    def __init__(self, is_deep: bool = False, element_id: Optional[str] = None):
        """
        Initialize a history pseudostate.
        
        Args:
            is_deep: Whether this is a deep history state (True) or shallow (False).
            element_id: Optional unique identifier for the state.
        """
        state_type = StateType.DEEP_HISTORY if is_deep else StateType.SHALLOW_HISTORY
        super().__init__("H" if not is_deep else "H*", state_type, element_id)
        self.is_deep = is_deep


class TerminatePseudostate(State):
    """Represents a terminate pseudostate in a UML State Diagram."""
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize a terminate pseudostate.
        
        Args:
            element_id: Optional unique identifier for the state.
        """
        super().__init__("", StateType.TERMINATE, element_id)


class Transition(Relationship):
    """
    Represents a transition between states in a UML State Diagram.
    
    A transition can have a trigger, guard condition, and effect (action).
    """
    
    def __init__(
        self,
        source: State,
        target: State,
        trigger: str = "",
        guard: str = "",
        effect: str = "",
        transition_type: TransitionType = TransitionType.EXTERNAL,
        element_id: Optional[str] = None
    ):
        """
        Initialize a transition between states.
        
        Args:
            source: The source state of the transition.
            target: The target state of the transition.
            trigger: The event that triggers the transition.
            guard: The guard condition that must be true for the transition.
            effect: The action that occurs when the transition executes.
            transition_type: The type of transition (external, internal, local).
            element_id: Optional unique identifier for the transition.
        """
        super().__init__(source, target, element_id)
        self.trigger = trigger
        self.guard = guard
        self.effect = effect
        self.transition_type = transition_type
        
        # Register with source and target states
        if transition_type != TransitionType.INTERNAL:
            source.add_outgoing_transition(self)
            target.add_incoming_transition(self)
    
    def render(self) -> Dict:
        """
        Render the transition as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the transition.
        """
        label = ""
        components = []
        
        if self.trigger:
            components.append(self.trigger)
        
        if self.guard:
            components.append(f"[{self.guard}]")
        
        if self.effect:
            components.append(f"/ {self.effect}")
        
        if components:
            label = " ".join(components)
        
        return {
            "id": self.id,
            "type": "transition",
            "transition_type": self.transition_type.value,
            "source_id": self.source.id,
            "target_id": self.target.id,
            "trigger": self.trigger,
            "guard": self.guard,
            "effect": self.effect,
            "label": label
        }


class Region:
    """
    Represents a region in a composite state.
    
    A region is a partition within a composite state that can contain
    its own set of states and transitions.
    """
    
    def __init__(self, name: str = ""):
        """
        Initialize a region.
        
        Args:
            name: The name of the region.
        """
        self.name = name
        self.states: List[State] = []
        self.transitions: List[Transition] = []
    
    def add_state(self, state: State) -> None:
        """Add a state to the region."""
        self.states.append(state)
    
    def add_transition(self, transition: Transition) -> None:
        """Add a transition to the region."""
        self.transitions.append(transition)
    
    def render(self) -> Dict:
        """
        Render the region as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the region.
        """
        return {
            "name": self.name,
            "states": [state.render() for state in self.states],
            "transitions": [transition.render() for transition in self.transitions]
        }


class StateDiagram(BaseDiagram):
    """
    Represents a UML State Diagram.
    
    A state diagram shows the possible states of an object and the
    transitions between those states.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a UML State Diagram.
        
        Args:
            name: The name of the diagram.
            description: Optional description of the diagram.
        """
        super().__init__(name, description)
        self.states: List[State] = []
        self.transitions: List[Transition] = []
        self.regions: List[Region] = []
    
    def add_state(self, state: State) -> None:
        """
        Add a state to the diagram.
        
        Args:
            state: The state to add.
        """
        self.states.append(state)
        self.elements.append(state)
    
    def add_transition(self, transition: Transition) -> None:
        """
        Add a transition to the diagram.
        
        Args:
            transition: The transition to add.
        """
        self.transitions.append(transition)
        self.relationships.append(transition)
    
    def add_region(self, region: Region) -> None:
        """
        Add a region to the diagram.
        
        Args:
            region: The region to add.
        """
        self.regions.append(region)
    
    def create_initial_state(self) -> InitialState:
        """
        Create and add an initial state to the diagram.
        
        Returns:
            The created initial state.
        """
        initial_state = InitialState()
        self.add_state(initial_state)
        return initial_state
    
    def create_final_state(self) -> FinalState:
        """
        Create and add a final state to the diagram.
        
        Returns:
            The created final state.
        """
        final_state = FinalState()
        self.add_state(final_state)
        return final_state
    
    def create_state(self, name: str) -> State:
        """
        Create and add a simple state to the diagram.
        
        Args:
            name: The name of the state.
            
        Returns:
            The created state.
        """
        state = State(name)
        self.add_state(state)
        return state
    
    def create_composite_state(self, name: str) -> CompositeState:
        """
        Create and add a composite state to the diagram.
        
        Args:
            name: The name of the composite state.
            
        Returns:
            The created composite state.
        """
        state = CompositeState(name)
        self.add_state(state)
        return state
    
    def create_choice_pseudostate(self) -> ChoicePseudostate:
        """
        Create and add a choice pseudostate to the diagram.
        
        Returns:
            The created choice pseudostate.
        """
        pseudostate = ChoicePseudostate()
        self.add_state(pseudostate)
        return pseudostate
    
    def create_junction_pseudostate(self) -> JunctionPseudostate:
        """
        Create and add a junction pseudostate to the diagram.
        
        Returns:
            The created junction pseudostate.
        """
        pseudostate = JunctionPseudostate()
        self.add_state(pseudostate)
        return pseudostate
    
    def create_entry_point(self, name: str) -> EntryPointPseudostate:
        """
        Create and add an entry point pseudostate to the diagram.
        
        Args:
            name: The name of the entry point.
            
        Returns:
            The created entry point pseudostate.
        """
        pseudostate = EntryPointPseudostate(name)
        self.add_state(pseudostate)
        return pseudostate
    
    def create_exit_point(self, name: str) -> ExitPointPseudostate:
        """
        Create and add an exit point pseudostate to the diagram.
        
        Args:
            name: The name of the exit point.
            
        Returns:
            The created exit point pseudostate.
        """
        pseudostate = ExitPointPseudostate(name)
        self.add_state(pseudostate)
        return pseudostate
    
    def create_history_state(self, is_deep: bool = False) -> HistoryPseudostate:
        """
        Create and add a history pseudostate to the diagram.
        
        Args:
            is_deep: Whether this is a deep history state (True) or shallow (False).
            
        Returns:
            The created history pseudostate.
        """
        pseudostate = HistoryPseudostate(is_deep)
        self.add_state(pseudostate)
        return pseudostate
    
    def create_terminate_pseudostate(self) -> TerminatePseudostate:
        """
        Create and add a terminate pseudostate to the diagram.
        
        Returns:
            The created terminate pseudostate.
        """
        pseudostate = TerminatePseudostate()
        self.add_state(pseudostate)
        return pseudostate
    
    def create_transition(
        self,
        source: State,
        target: State,
        trigger: str = "",
        guard: str = "",
        effect: str = "",
        transition_type: TransitionType = TransitionType.EXTERNAL
    ) -> Transition:
        """
        Create and add a transition between states.
        
        Args:
            source: The source state of the transition.
            target: The target state of the transition.
            trigger: The event that triggers the transition.
            guard: The guard condition that must be true for the transition.
            effect: The action that occurs when the transition executes.
            transition_type: The type of transition (external, internal, local).
            
        Returns:
            The created transition.
        """
        transition = Transition(source, target, trigger, guard, effect, transition_type)
        self.add_transition(transition)
        return transition
    
    def create_region(self, name: str = "") -> Region:
        """
        Create and add a region to the diagram.
        
        Args:
            name: The name of the region.
            
        Returns:
            The created region.
        """
        region = Region(name)
        self.add_region(region)
        return region
    
    def set_layout(self, layout: Layout) -> None:
        """
        Set the layout algorithm for the diagram.
        
        Args:
            layout: The layout algorithm to use.
        """
        self.layout = layout
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the state diagram to a file.
        
        Args:
            file_path: The path where the diagram will be saved.
            format: The format of the output file (default: 'svg').
            
        Returns:
            The path to the rendered file.
        """
        from pydiagrams.renderers.state_renderer import StateDiagramRenderer
        
        renderer = StateDiagramRenderer()
        return renderer.render(self.to_dict(), file_path) 