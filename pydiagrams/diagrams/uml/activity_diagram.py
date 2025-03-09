"""
Activity Diagram module for PyDiagrams.

This module provides the implementation for UML Activity Diagrams.
"""

from typing import Dict, List, Optional, Any, Set, Union
import os
from enum import Enum
from uuid import uuid4

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import Layout, HierarchicalLayout


class ActivityNodeType(Enum):
    """Types of nodes in an activity diagram."""
    ACTION = "action"
    INITIAL = "initial"
    FINAL = "final"
    DECISION = "decision"
    MERGE = "merge"
    FORK = "fork"
    JOIN = "join"
    OBJECT = "object"
    ACTIVITY_FINAL = "activity_final"
    SEND_SIGNAL = "send_signal"
    RECEIVE_SIGNAL = "receive_signal"
    TIME_EVENT = "time_event"
    ACCEPT_EVENT = "accept_event"


class ActivityNode(DiagramElement):
    """
    Base class for all nodes in an activity diagram.
    
    Nodes represent actions, decisions, and other elements in the activity flow.
    """
    
    def __init__(
        self,
        name: str,
        node_type: ActivityNodeType,
        element_id: Optional[str] = None
    ):
        """
        Initialize an activity node.
        
        Args:
            name: Name of the node
            node_type: Type of the node
            element_id: Optional unique identifier
        """
        super().__init__(name, element_id)
        self.node_type = node_type
        self.incoming_edges: List['ActivityEdge'] = []
        self.outgoing_edges: List['ActivityEdge'] = []
        
    def add_incoming_edge(self, edge: 'ActivityEdge') -> None:
        """
        Add an incoming edge to this node.
        
        Args:
            edge: The edge coming into this node
        """
        self.incoming_edges.append(edge)
        
    def add_outgoing_edge(self, edge: 'ActivityEdge') -> None:
        """
        Add an outgoing edge from this node.
        
        Args:
            edge: The edge going out from this node
        """
        self.outgoing_edges.append(edge)
        
    def render(self) -> Dict:
        """
        Render the node to a dictionary representation.
        
        Returns:
            Dict containing the node's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "activity_node",
            "node_type": self.node_type.value,
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class InitialNode(ActivityNode):
    """
    Initial node (start point) of an activity diagram.
    
    There is typically only one initial node in an activity diagram.
    """
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize an initial node.
        
        Args:
            element_id: Optional unique identifier
        """
        super().__init__("Initial", ActivityNodeType.INITIAL, element_id)


class ActivityFinalNode(ActivityNode):
    """
    Activity final node (end point) of an activity diagram.
    
    There can be multiple activity final nodes in an activity diagram.
    """
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize an activity final node.
        
        Args:
            element_id: Optional unique identifier
        """
        super().__init__("Final", ActivityNodeType.ACTIVITY_FINAL, element_id)


class FlowFinalNode(ActivityNode):
    """
    Flow final node that terminates a specific flow without terminating the entire activity.
    """
    
    def __init__(self, element_id: Optional[str] = None):
        """
        Initialize a flow final node.
        
        Args:
            element_id: Optional unique identifier
        """
        super().__init__("FlowFinal", ActivityNodeType.FINAL, element_id)


class ActionNode(ActivityNode):
    """
    Action node representing a single step in an activity.
    
    Actions are the basic executable units in an activity diagram.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an action node.
        
        Args:
            name: Name of the action
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.ACTION, element_id)


class DecisionNode(ActivityNode):
    """
    Decision node representing a branch point where flow can take different paths.
    
    Decision nodes have one incoming edge and multiple outgoing edges with guards.
    """
    
    def __init__(self, name: str = "Decision", element_id: Optional[str] = None):
        """
        Initialize a decision node.
        
        Args:
            name: Name of the decision
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.DECISION, element_id)


class MergeNode(ActivityNode):
    """
    Merge node that brings together multiple alternative flows.
    
    Merge nodes have multiple incoming edges and one outgoing edge.
    """
    
    def __init__(self, name: str = "Merge", element_id: Optional[str] = None):
        """
        Initialize a merge node.
        
        Args:
            name: Name of the merge
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.MERGE, element_id)


class ForkNode(ActivityNode):
    """
    Fork node that splits flow into multiple concurrent flows.
    
    Fork nodes have one incoming edge and multiple outgoing edges.
    """
    
    def __init__(self, name: str = "Fork", element_id: Optional[str] = None):
        """
        Initialize a fork node.
        
        Args:
            name: Name of the fork
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.FORK, element_id)


class JoinNode(ActivityNode):
    """
    Join node that synchronizes multiple concurrent flows.
    
    Join nodes have multiple incoming edges and one outgoing edge.
    """
    
    def __init__(self, name: str = "Join", element_id: Optional[str] = None):
        """
        Initialize a join node.
        
        Args:
            name: Name of the join
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.JOIN, element_id)


class ObjectNode(ActivityNode):
    """
    Object node representing an object or data used in the activity.
    
    Object nodes show the state of objects as they flow through the activity.
    """
    
    def __init__(
        self, 
        name: str, 
        state: str = "", 
        element_id: Optional[str] = None
    ):
        """
        Initialize an object node.
        
        Args:
            name: Name of the object
            state: Optional state of the object
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.OBJECT, element_id)
        self.state = state
        
    def render(self) -> Dict:
        """
        Render the object node to a dictionary representation.
        
        Returns:
            Dict containing the object node's properties for rendering
        """
        result = super().render()
        result["state"] = self.state
        return result


class SendSignalNode(ActivityNode):
    """
    Send signal node representing the sending of a signal to another entity.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a send signal node.
        
        Args:
            name: Name of the signal
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.SEND_SIGNAL, element_id)


class ReceiveSignalNode(ActivityNode):
    """
    Receive signal node representing the receipt of a signal from another entity.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a receive signal node.
        
        Args:
            name: Name of the signal
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.RECEIVE_SIGNAL, element_id)


class TimeEventNode(ActivityNode):
    """
    Time event node representing a time trigger or delay.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a time event node.
        
        Args:
            name: Description of the time event
            element_id: Optional unique identifier
        """
        super().__init__(name, ActivityNodeType.TIME_EVENT, element_id)


class ActivityEdge(Relationship):
    """
    Edge connecting activity nodes.
    
    Edges represent the flow of control between nodes.
    """
    
    def __init__(
        self,
        source: ActivityNode,
        target: ActivityNode,
        guard: str = "",
        element_id: Optional[str] = None
    ):
        """
        Initialize an activity edge.
        
        Args:
            source: Source node
            target: Target node
            guard: Optional guard condition
            element_id: Optional unique identifier
        """
        super().__init__(
            source,
            target,
            "",
            "",
            "",
            "control_flow",
            element_id
        )
        self.guard = guard
        
        # Register the edge with its source and target nodes
        source.add_outgoing_edge(self)
        target.add_incoming_edge(self)
        
    def render(self) -> Dict:
        """
        Render the edge to a dictionary representation.
        
        Returns:
            Dict containing the edge's properties for rendering
        """
        result = super().render()
        result.update({
            "type": "activity_edge",
            "guard": self.guard
        })
        return result


class Swimlane(DiagramElement):
    """
    Swimlane for organizing activities by responsibility.
    
    Swimlanes can be horizontal or vertical and can represent roles, systems, etc.
    """
    
    def __init__(
        self,
        name: str,
        is_horizontal: bool = True,
        element_id: Optional[str] = None
    ):
        """
        Initialize a swimlane.
        
        Args:
            name: Name of the swimlane
            is_horizontal: Whether the swimlane is horizontal
            element_id: Optional unique identifier
        """
        super().__init__(name, element_id)
        self.is_horizontal = is_horizontal
        self.nodes: List[ActivityNode] = []
        
    def add_node(self, node: ActivityNode) -> None:
        """
        Add a node to this swimlane.
        
        Args:
            node: The node to add
        """
        self.nodes.append(node)
        
    def render(self) -> Dict:
        """
        Render the swimlane to a dictionary representation.
        
        Returns:
            Dict containing the swimlane's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "swimlane",
            "is_horizontal": self.is_horizontal,
            "node_ids": [node.id for node in self.nodes],
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class ActivityDiagram(BaseDiagram):
    """Class for creating and rendering UML Activity Diagrams."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize an activity diagram.
        
        Args:
            name: Diagram name
            description: Optional description
        """
        super().__init__(name, description)
        self.nodes: List[ActivityNode] = []
        self.edges: List[ActivityEdge] = []
        self.swimlanes: List[Swimlane] = []
        self.layout = HierarchicalLayout()
        
    def add_node(self, node: ActivityNode) -> None:
        """
        Add a node to the diagram.
        
        Args:
            node: Node to add
        """
        self.nodes.append(node)
        self.add_element(node)
        
    def add_edge(self, edge: ActivityEdge) -> None:
        """
        Add an edge to the diagram.
        
        Args:
            edge: Edge to add
        """
        self.edges.append(edge)
        self.add_relationship(edge)

    def add_swimlane(self, swimlane: Swimlane) -> None:
        """
        Add a swimlane to the diagram.
        
        Args:
            swimlane: Swimlane to add
        """
        self.swimlanes.append(swimlane)
        self.add_element(swimlane)
        
    def create_initial_node(self) -> InitialNode:
        """
        Create and add an initial node.
        
        Returns:
            The created initial node
        """
        node = InitialNode()
        self.add_node(node)
        return node
        
    def create_activity_final_node(self) -> ActivityFinalNode:
        """
        Create and add an activity final node.
        
        Returns:
            The created activity final node
        """
        node = ActivityFinalNode()
        self.add_node(node)
        return node
        
    def create_flow_final_node(self) -> FlowFinalNode:
        """
        Create and add a flow final node.
        
        Returns:
            The created flow final node
        """
        node = FlowFinalNode()
        self.add_node(node)
        return node
        
    def create_action_node(self, name: str) -> ActionNode:
        """
        Create and add an action node.
        
        Args:
            name: Name of the action
            
        Returns:
            The created action node
        """
        node = ActionNode(name)
        self.add_node(node)
        return node
        
    def create_decision_node(self, name: str = "Decision") -> DecisionNode:
        """
        Create and add a decision node.
        
        Args:
            name: Name of the decision
            
        Returns:
            The created decision node
        """
        node = DecisionNode(name)
        self.add_node(node)
        return node
        
    def create_merge_node(self, name: str = "Merge") -> MergeNode:
        """
        Create and add a merge node.
        
        Args:
            name: Name of the merge
            
        Returns:
            The created merge node
        """
        node = MergeNode(name)
        self.add_node(node)
        return node
        
    def create_fork_node(self, name: str = "Fork") -> ForkNode:
        """
        Create and add a fork node.
        
        Args:
            name: Name of the fork
            
        Returns:
            The created fork node
        """
        node = ForkNode(name)
        self.add_node(node)
        return node
        
    def create_join_node(self, name: str = "Join") -> JoinNode:
        """
        Create and add a join node.
        
        Args:
            name: Name of the join
            
        Returns:
            The created join node
        """
        node = JoinNode(name)
        self.add_node(node)
        return node
        
    def create_object_node(self, name: str, state: str = "") -> ObjectNode:
        """
        Create and add an object node.
        
        Args:
            name: Name of the object
            state: Optional state of the object
            
        Returns:
            The created object node
        """
        node = ObjectNode(name, state)
        self.add_node(node)
        return node
        
    def create_send_signal_node(self, name: str) -> SendSignalNode:
        """
        Create and add a send signal node.
        
        Args:
            name: Name of the signal
            
        Returns:
            The created send signal node
        """
        node = SendSignalNode(name)
        self.add_node(node)
        return node
        
    def create_receive_signal_node(self, name: str) -> ReceiveSignalNode:
        """
        Create and add a receive signal node.
        
        Args:
            name: Name of the signal
            
        Returns:
            The created receive signal node
        """
        node = ReceiveSignalNode(name)
        self.add_node(node)
        return node
        
    def create_time_event_node(self, name: str) -> TimeEventNode:
        """
        Create and add a time event node.
        
        Args:
            name: Description of the time event
            
        Returns:
            The created time event node
        """
        node = TimeEventNode(name)
        self.add_node(node)
        return node
        
    def create_edge(
        self, 
        source: ActivityNode, 
        target: ActivityNode, 
        guard: str = ""
    ) -> ActivityEdge:
        """
        Create and add an edge between nodes.
        
        Args:
            source: Source node
            target: Target node
            guard: Optional guard condition
            
        Returns:
            The created edge
        """
        edge = ActivityEdge(source, target, guard)
        self.add_edge(edge)
        return edge
        
    def create_swimlane(
        self, 
        name: str, 
        is_horizontal: bool = True
    ) -> Swimlane:
        """
        Create and add a swimlane.
        
        Args:
            name: Name of the swimlane
            is_horizontal: Whether the swimlane is horizontal
            
        Returns:
            The created swimlane
        """
        swimlane = Swimlane(name, is_horizontal)
        self.add_swimlane(swimlane)
        return swimlane
        
    def add_node_to_swimlane(self, node: ActivityNode, swimlane: Swimlane) -> None:
        """
        Add a node to a swimlane.
        
        Args:
            node: Node to add
            swimlane: Swimlane to add the node to
        """
        swimlane.add_node(node)
        
    def set_layout(self, layout: Layout) -> None:
        """
        Set the layout algorithm for the diagram.
        
        Args:
            layout: Layout algorithm to use
        """
        self.layout = layout
        
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
        
        # Apply layout to position elements
        diagram_data = self.layout.apply(diagram_data)
        
        # Create the renderer based on the format
        if format.lower() == "svg":
            from pydiagrams.renderers.activity_renderer import ActivityDiagramRenderer
            renderer = ActivityDiagramRenderer()
            return renderer.render(diagram_data, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}. Currently only 'svg' is fully supported.") 