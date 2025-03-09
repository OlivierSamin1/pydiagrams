"""
Sequence Diagram module for PyDiagrams.

This module provides the implementation for UML Sequence Diagrams.
"""

from typing import Dict, List, Optional, Any, Tuple, Union
import os
from enum import Enum
from uuid import uuid4

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import Layout, HierarchicalLayout
from pydiagrams.renderers.svg_renderer import SVGRenderer
from pydiagrams.renderers.sequence_renderer import SequenceDiagramRenderer


class MessageType(Enum):
    """Enum for different types of sequence diagram messages."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    REPLY = "reply"
    CREATE = "create"
    DESTROY = "destroy"
    SELF = "self"


class Lifeline(DiagramElement):
    """
    Represents a participant (object or actor) in a sequence diagram.
    
    Lifelines are vertical lines that represent the existence of an object over time.
    """
    
    def __init__(
        self, 
        name: str, 
        is_actor: bool = False, 
        element_id: Optional[str] = None,
        stereotype: str = ""
    ):
        """
        Initialize a lifeline.
        
        Args:
            name: Name of the lifeline
            is_actor: Whether this lifeline represents an actor (vs an object)
            element_id: Optional unique identifier
            stereotype: Optional stereotype (e.g., «boundary», «control», etc.)
        """
        super().__init__(name, element_id)
        self.is_actor = is_actor
        self.stereotype = stereotype
        self.activations: List[Activation] = []
        
    def add_activation(self, start_time: int, end_time: int) -> 'Activation':
        """
        Add an activation to this lifeline.
        
        Args:
            start_time: Start time (y-coordinate) of the activation
            end_time: End time (y-coordinate) of the activation
            
        Returns:
            The created activation
        """
        activation = Activation(self, start_time, end_time)
        self.activations.append(activation)
        return activation
    
    def render(self) -> Dict:
        """
        Render the lifeline to a dictionary representation.
        
        Returns:
            Dict containing the lifeline's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "lifeline",
            "is_actor": self.is_actor,
            "stereotype": self.stereotype,
            "activations": [activation.render() for activation in self.activations],
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class Activation(DiagramElement):
    """
    Represents an activation bar on a lifeline.
    
    Activations show when an object is active or performing an operation.
    """
    
    def __init__(
        self,
        lifeline: Lifeline,
        start_time: int,
        end_time: int,
        element_id: Optional[str] = None
    ):
        """
        Initialize an activation.
        
        Args:
            lifeline: The lifeline this activation belongs to
            start_time: Start time (y-coordinate) of the activation
            end_time: End time (y-coordinate) of the activation
            element_id: Optional unique identifier
        """
        super().__init__(f"Activation_{lifeline.name}_{start_time}", element_id)
        self.lifeline = lifeline
        self.start_time = start_time
        self.end_time = end_time
        self.nested_activations: List[Activation] = []
        
    def add_nested_activation(self, start_time: int, end_time: int) -> 'Activation':
        """
        Add a nested activation (for recursive calls).
        
        Args:
            start_time: Start time of the nested activation
            end_time: End time of the nested activation
            
        Returns:
            The created nested activation
        """
        nested = Activation(self.lifeline, start_time, end_time)
        self.nested_activations.append(nested)
        return nested
        
    def render(self) -> Dict:
        """
        Render the activation to a dictionary representation.
        
        Returns:
            Dict containing the activation's properties for rendering
        """
        return {
            "id": self.id,
            "type": "activation",
            "lifeline_id": self.lifeline.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "nested_activations": [nested.render() for nested in self.nested_activations],
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class Message(Relationship):
    """
    Represents a message between lifelines or activations.
    
    Messages show the interactions between objects/lifelines.
    """
    
    def __init__(
        self,
        source: Union[Lifeline, Activation],
        target: Union[Lifeline, Activation],
        message_text: str,
        message_type: MessageType = MessageType.SYNCHRONOUS,
        time_point: int = 0,
        element_id: Optional[str] = None
    ):
        """
        Initialize a message.
        
        Args:
            source: Source lifeline or activation
            target: Target lifeline or activation
            message_text: Text describing the message
            message_type: Type of message
            time_point: The y-coordinate where the message appears
            element_id: Optional unique identifier
        """
        super().__init__(
            source,
            target,
            "",
            "",
            message_text,
            message_type.value,
            element_id
        )
        self.message_type = message_type
        self.time_point = time_point
        
    def render(self) -> Dict:
        """
        Render the message to a dictionary representation.
        
        Returns:
            Dict containing the message's properties for rendering
        """
        result = super().render()
        result.update({
            "type": "message",
            "message_type": self.message_type.value,
            "time_point": self.time_point
        })
        return result


class Fragment(DiagramElement):
    """
    Represents a combined fragment in a sequence diagram.
    
    Combined fragments are used to group messages together (e.g., loops, conditionals).
    """
    
    class FragmentType(Enum):
        """Types of combined fragments in sequence diagrams."""
        ALT = "alt"  # Alternative paths
        OPT = "opt"  # Optional path
        LOOP = "loop"  # Loop
        PAR = "par"  # Parallel execution
        CRITICAL = "critical"  # Critical region
        NEG = "neg"  # Negative behavior
        BREAK = "break"  # Break from loop
        REF = "ref"  # Reference to another diagram
        
    def __init__(
        self,
        name: str,
        fragment_type: FragmentType,
        start_time: int,
        end_time: int,
        condition: str = "",
        element_id: Optional[str] = None
    ):
        """
        Initialize a fragment.
        
        Args:
            name: Name of the fragment
            fragment_type: Type of fragment
            start_time: Start time (y-coordinate) of the fragment
            end_time: End time (y-coordinate) of the fragment
            condition: Optional condition text for the fragment
            element_id: Optional unique identifier
        """
        super().__init__(name, element_id)
        self.fragment_type = fragment_type
        self.start_time = start_time
        self.end_time = end_time
        self.condition = condition
        self.operands: List[Tuple[str, int]] = []  # (condition, separator_time)
        
    def add_operand(self, condition: str, separator_time: int) -> None:
        """
        Add an operand to this fragment (e.g., an "else" block in an "alt" fragment).
        
        Args:
            condition: The condition text for this operand
            separator_time: The y-coordinate where this operand starts
        """
        self.operands.append((condition, separator_time))
        
    def render(self) -> Dict:
        """
        Render the fragment to a dictionary representation.
        
        Returns:
            Dict containing the fragment's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "fragment",
            "fragment_type": self.fragment_type.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "condition": self.condition,
            "operands": self.operands,
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class SequenceDiagram(BaseDiagram):
    """Class for creating and rendering UML Sequence Diagrams."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a sequence diagram.
        
        Args:
            name: Diagram name
            description: Optional description
        """
        super().__init__(name, description)
        self.lifelines: List[Lifeline] = []
        self.messages: List[Message] = []
        self.fragments: List[Fragment] = []
        
    def add_lifeline(self, lifeline: Lifeline) -> None:
        """
        Add a lifeline to the diagram.
        
        Args:
            lifeline: Lifeline to add
        """
        self.lifelines.append(lifeline)
        self.add_element(lifeline)
        
    def create_lifeline(
        self, 
        name: str, 
        is_actor: bool = False, 
        stereotype: str = ""
    ) -> Lifeline:
        """
        Create and add a new lifeline.
        
        Args:
            name: Name of the lifeline
            is_actor: Whether this lifeline represents an actor
            stereotype: Optional stereotype
            
        Returns:
            The created lifeline
        """
        lifeline = Lifeline(name, is_actor, stereotype=stereotype)
        self.add_lifeline(lifeline)
        return lifeline
        
    def add_message(self, message: Message) -> None:
        """
        Add a message to the diagram.
        
        Args:
            message: Message to add
        """
        self.messages.append(message)
        self.add_relationship(message)
        
    def create_message(
        self,
        source: Union[Lifeline, Activation],
        target: Union[Lifeline, Activation],
        message_text: str,
        message_type: MessageType = MessageType.SYNCHRONOUS,
        time_point: int = 0
    ) -> Message:
        """
        Create and add a new message.
        
        Args:
            source: Source lifeline or activation
            target: Target lifeline or activation
            message_text: Text describing the message
            message_type: Type of message
            time_point: The y-coordinate where the message appears
            
        Returns:
            The created message
        """
        message = Message(source, target, message_text, message_type, time_point)
        self.add_message(message)
        return message
        
    def add_fragment(self, fragment: Fragment) -> None:
        """
        Add a fragment to the diagram.
        
        Args:
            fragment: Fragment to add
        """
        self.fragments.append(fragment)
        self.add_element(fragment)
        
    def create_fragment(
        self,
        name: str,
        fragment_type: Fragment.FragmentType,
        start_time: int,
        end_time: int,
        condition: str = ""
    ) -> Fragment:
        """
        Create and add a new fragment.
        
        Args:
            name: Name of the fragment
            fragment_type: Type of fragment
            start_time: Start time (y-coordinate) of the fragment
            end_time: End time (y-coordinate) of the fragment
            condition: Optional condition text for the fragment
            
        Returns:
            The created fragment
        """
        fragment = Fragment(name, fragment_type, start_time, end_time, condition)
        self.add_fragment(fragment)
        return fragment
        
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the diagram to a file.
        
        Args:
            file_path: Path where the diagram should be saved
            format: Output format (currently only 'svg' is fully implemented)
            
        Returns:
            Path to the rendered file
        """
        # Convert the diagram to a dictionary representation
        diagram_data = self.to_dict()
        
        # Use the specialized sequence diagram renderer
        if format.lower() == "svg":
            renderer = SequenceDiagramRenderer()
            return renderer.render(diagram_data, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}. Currently only 'svg' is fully supported.")
            
    def _calculate_time_points(self, diagram_data: Dict) -> None:
        """
        Calculate message time points to ensure proper vertical ordering.
        
        This is called automatically during rendering if time_points are not manually set.
        
        Args:
            diagram_data: Dictionary representation of the diagram
        """
        # This is a placeholder for the auto-calculation logic
        # In a real implementation, this would analyze message dependencies
        # and assign appropriate time points
        
        # For now, just ensure we have some minimal spacing
        messages = diagram_data.get("relationships", [])
        current_time = 50  # Start at y=50
        
        for i, message in enumerate(messages):
            if message.get("type") == "message" and message.get("time_point", 0) == 0:
                message["time_point"] = current_time
                current_time += 30  # Add 30 pixels between messages
                
    def _calculate_lifeline_positions(self, diagram_data: Dict) -> None:
        """
        Calculate horizontal positions for lifelines.
        
        This is called automatically during rendering if positions are not manually set.
        
        Args:
            diagram_data: Dictionary representation of the diagram
        """
        # This is a placeholder for the auto-positioning logic
        # In a real implementation, this would use a more sophisticated algorithm
        
        # For now, just space lifelines evenly
        lifelines = [e for e in diagram_data.get("elements", []) if e.get("type") == "lifeline"]
        lifeline_width = 100  # Assume 100px width for each lifeline
        diagram_width = len(lifelines) * lifeline_width + 100  # Add 100px for margins
        
        x = 50  # Start at x=50
        for lifeline in lifelines:
            if "position" not in lifeline:
                lifeline["position"] = {"x": x, "y": 50}
            x += lifeline_width + 50  # Add 50px between lifelines
            
        # Update diagram size if needed
        if diagram_data.get("width", 0) < diagram_width:
            diagram_data["width"] = diagram_width 