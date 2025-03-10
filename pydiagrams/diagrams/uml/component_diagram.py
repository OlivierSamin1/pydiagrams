#!/usr/bin/env python3
"""
Module for UML Component Diagram models.

UML Component Diagrams are used to illustrate the relationships between 
components in a system. Components represent independent, encapsulated
units within a system's architecture that provides and requires interfaces.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import uuid


class ComponentType(Enum):
    """Types of components in a UML Component Diagram."""
    COMPONENT = auto()
    SUBSYSTEM = auto()
    PACKAGE = auto()
    NODE = auto()
    DEVICE = auto()
    EXECUTION_ENVIRONMENT = auto()


class InterfaceType(Enum):
    """Types of interfaces in a UML Component Diagram."""
    PROVIDED = auto()  # Interface that a component provides (lollipop)
    REQUIRED = auto()  # Interface that a component requires (socket)


@dataclass
class Interface:
    """
    Represents an interface in a Component Diagram.
    
    Interfaces define sets of operations that components can provide or require.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    operations: List[str] = field(default_factory=list)
    interface_type: InterfaceType = InterfaceType.PROVIDED
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Interface_{self.id[:8]}"


@dataclass
class Component:
    """
    Represents a component in a Component Diagram.
    
    Components are modular, deployable, and replaceable parts of a system
    that encapsulate implementation and expose it through interfaces.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    stereotype: Optional[str] = None
    component_type: ComponentType = ComponentType.COMPONENT
    provided_interfaces: List[Interface] = field(default_factory=list)
    required_interfaces: List[Interface] = field(default_factory=list)
    nested_components: List['Component'] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Component_{self.id[:8]}"
    
    def add_provided_interface(self, interface: Interface) -> None:
        """Add a provided interface to this component."""
        interface.interface_type = InterfaceType.PROVIDED
        self.provided_interfaces.append(interface)
    
    def add_required_interface(self, interface: Interface) -> None:
        """Add a required interface to this component."""
        interface.interface_type = InterfaceType.REQUIRED
        self.required_interfaces.append(interface)
    
    def add_nested_component(self, component: 'Component') -> None:
        """Add a nested component to this component."""
        self.nested_components.append(component)


@dataclass
class Port:
    """
    Represents a port in a Component Diagram.
    
    Ports are interaction points through which components communicate
    with each other.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    provided_interfaces: List[Interface] = field(default_factory=list)
    required_interfaces: List[Interface] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Port_{self.id[:8]}"


class ConnectorType(Enum):
    """Types of connectors in a UML Component Diagram."""
    ASSEMBLY = auto()  # Connects required and provided interfaces
    DELEGATION = auto()  # Forwards interactions
    DEPENDENCY = auto()  # One component depends on another
    REALIZATION = auto()  # Implementation relationship
    GENERALIZATION = auto()  # Inheritance relationship


@dataclass
class Connector:
    """
    Represents a connector between components, ports, or interfaces.
    
    Connectors define the relationships between components and their
    interfaces, establishing the communication paths in the system.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_id: str = ""  # ID of source component, port, or interface
    target_id: str = ""  # ID of target component, port, or interface
    connector_type: ConnectorType = ConnectorType.ASSEMBLY
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Connector_{self.id[:8]}"


@dataclass
class Artifact:
    """
    Represents an artifact in a Component Diagram.
    
    Artifacts are physical pieces of information that are used or produced
    by a development process or deployment operation.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Artifact_{self.id[:8]}"


@dataclass
class ComponentDiagram:
    """
    UML Component Diagram model.
    
    Component Diagrams are used to visualize the organization and 
    dependencies among components in a system, showing how they 
    fit together and communicate through interfaces.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    components: List[Component] = field(default_factory=list)
    connectors: List[Connector] = field(default_factory=list)
    artifacts: List[Artifact] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"ComponentDiagram_{self.id[:8]}"
    
    def add_component(self, component: Component) -> None:
        """Add a component to the diagram."""
        self.components.append(component)
    
    def add_connector(self, connector: Connector) -> None:
        """Add a connector to the diagram."""
        self.connectors.append(connector)
    
    def add_artifact(self, artifact: Artifact) -> None:
        """Add an artifact to the diagram."""
        self.artifacts.append(artifact)
    
    def create_component(
        self, 
        name: str, 
        description: str = "", 
        stereotype: Optional[str] = None,
        component_type: ComponentType = ComponentType.COMPONENT
    ) -> Component:
        """Create and add a new component to the diagram."""
        component = Component(
            name=name, 
            description=description, 
            stereotype=stereotype,
            component_type=component_type
        )
        self.components.append(component)
        return component
    
    def create_interface(
        self, 
        name: str, 
        operations: List[str] = None, 
        interface_type: InterfaceType = InterfaceType.PROVIDED
    ) -> Interface:
        """Create a new interface (not added to diagram directly)."""
        if operations is None:
            operations = []
        return Interface(name=name, operations=operations, interface_type=interface_type)
    
    def create_connector(
        self, 
        source_id: str, 
        target_id: str, 
        name: str = "", 
        connector_type: ConnectorType = ConnectorType.ASSEMBLY,
        stereotype: Optional[str] = None
    ) -> Connector:
        """Create and add a new connector to the diagram."""
        connector = Connector(
            name=name, 
            source_id=source_id, 
            target_id=target_id, 
            connector_type=connector_type,
            stereotype=stereotype
        )
        self.connectors.append(connector)
        return connector
    
    def create_artifact(
        self, 
        name: str, 
        description: str = "", 
        stereotype: Optional[str] = None
    ) -> Artifact:
        """Create and add a new artifact to the diagram."""
        artifact = Artifact(
            name=name, 
            description=description, 
            stereotype=stereotype
        )
        self.artifacts.append(artifact)
        return artifact 