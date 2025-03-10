#!/usr/bin/env python3
"""
Container Diagram module for PyDiagrams.

This module provides the implementation for Container Diagrams, which show
the high-level technical building blocks (containers) that make up a system
and how they interact with each other and with users.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class ContainerType(Enum):
    """Types of containers in a Container Diagram."""
    WEB_APPLICATION = auto()  # Web application or site
    MOBILE_APP = auto()  # Mobile application
    DESKTOP_APP = auto()  # Desktop application
    API = auto()  # API or service
    DATABASE = auto()  # Database
    FILE_SYSTEM = auto()  # File system
    MICROSERVICE = auto()  # Microservice
    QUEUE = auto()  # Message queue or bus
    SERVER_SIDE = auto()  # Generic server-side application
    CACHE = auto()  # Cache system
    CUSTOM = auto()  # Custom container type


class ContainerRelationshipType(Enum):
    """Types of relationships between containers."""
    USES = auto()  # One container uses another
    SENDS_DATA_TO = auto()  # One container sends data to another
    READS_FROM = auto()  # One container reads from another
    WRITES_TO = auto()  # One container writes to another
    NOTIFIES = auto()  # One container notifies another
    DEPENDS_ON = auto()  # One container depends on another
    CUSTOM = auto()  # Custom relationship type


@dataclass
class Person:
    """
    Represents a person/user in a Container Diagram.
    
    This corresponds to a user or stakeholder of the system.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    external: bool = False  # Whether this is an external user
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Person_{self.id[:8]}"


@dataclass
class Container:
    """
    Represents a container in a Container Diagram.
    
    A container is a standalone application, data store, or thing that executes code.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    technology: Optional[str] = None  # Technology used (e.g., "Spring Boot", "React")
    container_type: ContainerType = ContainerType.SERVER_SIDE
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Container_{self.id[:8]}"


@dataclass
class ExternalSystem:
    """
    Represents an external system in a Container Diagram.
    
    External systems are systems that yours interacts with but are not part of it.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    technology: Optional[str] = None  # Technology used, if known
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"ExternalSystem_{self.id[:8]}"


@dataclass
class ContainerRelationship:
    """
    Represents a relationship between elements in a Container Diagram.
    
    Relationships show how containers, people, and external systems interact.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    source_id: str = ""  # ID of source element
    target_id: str = ""  # ID of target element
    relationship_type: ContainerRelationshipType = ContainerRelationshipType.USES
    technology: Optional[str] = None  # Technology used (e.g., "REST", "JDBC")
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Relationship_{self.id[:8]}"


class SystemBoundary:
    """
    Represents a system boundary in a Container Diagram.
    
    System boundaries group containers that belong to the same system.
    """
    def __init__(self, name: str, description: str = ""):
        """Initialize a system boundary."""
        self.id = str(uuid.uuid4())
        self.name = name if name else f"Boundary_{self.id[:8]}"
        self.description = description
        self.container_ids: List[str] = []
        self.tags: List[str] = []
        self.properties: Dict[str, str] = {}
    
    def add_container_id(self, container_id: str) -> None:
        """Add a container to this boundary."""
        if container_id not in self.container_ids:
            self.container_ids.append(container_id)


class ContainerDiagram(BaseDiagram):
    """
    Container Diagram model.
    
    Container Diagrams show the high-level technical components (containers) of a system,
    how they interact with each other, and how they interact with users and external systems.
    """
    
    def __init__(self, name: str, description: str = ""):
        """Initialize a Container Diagram."""
        super().__init__(name, description)
        self.people: List[Person] = []
        self.containers: List[Container] = []
        self.external_systems: List[ExternalSystem] = []
        self.relationships: List[ContainerRelationship] = []
        self.boundaries: List[SystemBoundary] = []
        self.layout = HierarchicalLayout()
    
    def add_person(self, person: Person) -> None:
        """Add a person to the diagram."""
        self.people.append(person)
    
    def add_container(self, container: Container) -> None:
        """Add a container to the diagram."""
        self.containers.append(container)
    
    def add_external_system(self, external_system: ExternalSystem) -> None:
        """Add an external system to the diagram."""
        self.external_systems.append(external_system)
    
    def add_relationship(self, relationship: ContainerRelationship) -> None:
        """Add a relationship to the diagram."""
        self.relationships.append(relationship)
    
    def add_boundary(self, boundary: SystemBoundary) -> None:
        """Add a system boundary to the diagram."""
        self.boundaries.append(boundary)
    
    def create_person(
        self,
        name: str,
        description: str = "",
        external: bool = False,
        tags: Optional[List[str]] = None
    ) -> Person:
        """
        Create and add a person to the diagram.
        
        Args:
            name: Name of the person
            description: Description of the person
            external: Whether this is an external user
            tags: Optional list of tags for filtering or styling
            
        Returns:
            The created Person object
        """
        person = Person(
            name=name,
            description=description,
            external=external,
            tags=tags or []
        )
        self.add_person(person)
        return person
    
    def create_container(
        self,
        name: str,
        description: str = "",
        technology: Optional[str] = None,
        container_type: ContainerType = ContainerType.SERVER_SIDE,
        tags: Optional[List[str]] = None
    ) -> Container:
        """
        Create and add a container to the diagram.
        
        Args:
            name: Name of the container
            description: Description of the container
            technology: Technology used by the container
            container_type: Type of container
            tags: Optional list of tags for filtering or styling
            
        Returns:
            The created Container object
        """
        container = Container(
            name=name,
            description=description,
            technology=technology,
            container_type=container_type,
            tags=tags or []
        )
        self.add_container(container)
        return container
    
    def create_external_system(
        self,
        name: str,
        description: str = "",
        technology: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ExternalSystem:
        """
        Create and add an external system to the diagram.
        
        Args:
            name: Name of the external system
            description: Description of the external system
            technology: Technology used by the external system, if known
            tags: Optional list of tags for filtering or styling
            
        Returns:
            The created ExternalSystem object
        """
        external_system = ExternalSystem(
            name=name,
            description=description,
            technology=technology,
            tags=tags or []
        )
        self.add_external_system(external_system)
        return external_system
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        description: str = "",
        relationship_type: ContainerRelationshipType = ContainerRelationshipType.USES,
        technology: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ContainerRelationship:
        """
        Create and add a relationship to the diagram.
        
        Args:
            source_id: ID of the source element
            target_id: ID of the target element
            name: Name of the relationship
            description: Description of the relationship
            relationship_type: Type of relationship
            technology: Technology used in the relationship
            tags: Optional list of tags for filtering or styling
            
        Returns:
            The created ContainerRelationship object
        """
        relationship = ContainerRelationship(
            name=name,
            description=description,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            technology=technology,
            tags=tags or []
        )
        self.add_relationship(relationship)
        return relationship
    
    def create_boundary(
        self,
        name: str,
        description: str = "",
        container_ids: Optional[List[str]] = None
    ) -> SystemBoundary:
        """
        Create and add a system boundary to the diagram.
        
        Args:
            name: Name of the boundary
            description: Description of the boundary
            container_ids: IDs of containers to include in this boundary
            
        Returns:
            The created SystemBoundary object
        """
        boundary = SystemBoundary(name, description)
        
        if container_ids:
            for container_id in container_ids:
                boundary.add_container_id(container_id)
        
        self.add_boundary(boundary)
        return boundary
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the container diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This is a placeholder that will be implemented by renderers
        return file_path 