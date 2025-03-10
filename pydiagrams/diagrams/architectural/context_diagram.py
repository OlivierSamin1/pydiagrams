#!/usr/bin/env python3
"""
System Context Diagram module for PyDiagrams.

This module provides the implementation for System Context Diagrams, which show
how a system interacts with users and external systems, providing a high-level
view of the system's interactions and boundaries.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class ElementType(Enum):
    """Types of elements in a System Context Diagram."""
    SYSTEM = auto()  # The system being described
    PERSON = auto()  # A user of the system
    EXTERNAL_SYSTEM = auto()  # An external system
    ENTERPRISE_BOUNDARY = auto()  # Enterprise boundary
    CONTAINER = auto()  # Container (when used in combination with Container Diagram)
    DATABASE = auto()  # Database system


class RelationshipType(Enum):
    """Types of relationships in a System Context Diagram."""
    USES = auto()  # One element uses another
    SENDS_DATA_TO = auto()  # One element sends data to another
    RECEIVES_DATA_FROM = auto()  # One element receives data from another
    DEPENDS_ON = auto()  # One element depends on another
    CUSTOM = auto()  # Custom relationship


@dataclass
class ContextElement:
    """
    Represents an element in a System Context Diagram.
    
    An element can be a system, person, external system, etc.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    element_type: ElementType = ElementType.SYSTEM
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Element_{self.id[:8]}"


@dataclass
class ContextRelationship:
    """
    Represents a relationship between elements in a System Context Diagram.
    
    Relationships show how elements interact with each other.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    source_id: str = ""  # ID of source element
    target_id: str = ""  # ID of target element
    relationship_type: RelationshipType = RelationshipType.USES
    technology: Optional[str] = None  # Technology used in the relationship (e.g., "REST API")
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Relationship_{self.id[:8]}"


@dataclass
class Boundary:
    """
    Represents a boundary in a System Context Diagram.
    
    Boundaries group elements to show organizational or technological boundaries.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    element_ids: List[str] = field(default_factory=list)  # IDs of elements within this boundary
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    parent_boundary_id: Optional[str] = None  # For nested boundaries
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Boundary_{self.id[:8]}"
    
    def add_element_id(self, element_id: str) -> None:
        """Add an element to this boundary."""
        if element_id not in self.element_ids:
            self.element_ids.append(element_id)


class SystemContextDiagram(BaseDiagram):
    """
    System Context Diagram model.
    
    System Context Diagrams show how a system interacts with users and external systems,
    providing a high-level view of the system's interactions and boundaries.
    """
    
    def __init__(self, name: str, description: str = ""):
        """Initialize a System Context Diagram."""
        super().__init__(name, description)
        self.elements: List[ContextElement] = []
        self.relationships: List[ContextRelationship] = []
        self.boundaries: List[Boundary] = []
        self.layout = HierarchicalLayout()
    
    def add_element(self, element: ContextElement) -> None:
        """Add an element to the diagram."""
        self.elements.append(element)
    
    def add_relationship(self, relationship: ContextRelationship) -> None:
        """Add a relationship to the diagram."""
        self.relationships.append(relationship)
    
    def add_boundary(self, boundary: Boundary) -> None:
        """Add a boundary to the diagram."""
        self.boundaries.append(boundary)
    
    def create_element(
        self,
        name: str,
        description: str = "",
        element_type: ElementType = ElementType.SYSTEM,
        tags: Optional[List[str]] = None
    ) -> ContextElement:
        """
        Create and add an element to the diagram.
        
        Args:
            name: Name of the element
            description: Description of the element
            element_type: Type of element (system, person, etc.)
            tags: Optional list of tags for filtering or styling
            
        Returns:
            The created ContextElement object
        """
        element = ContextElement(
            name=name,
            description=description,
            element_type=element_type,
            tags=tags or []
        )
        self.add_element(element)
        return element
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        description: str = "",
        relationship_type: RelationshipType = RelationshipType.USES,
        technology: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> ContextRelationship:
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
            The created ContextRelationship object
        """
        relationship = ContextRelationship(
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
        element_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        parent_boundary_id: Optional[str] = None
    ) -> Boundary:
        """
        Create and add a boundary to the diagram.
        
        Args:
            name: Name of the boundary
            description: Description of the boundary
            element_ids: IDs of elements to include in the boundary
            tags: Optional list of tags for filtering or styling
            parent_boundary_id: ID of the parent boundary for nesting
            
        Returns:
            The created Boundary object
        """
        boundary = Boundary(
            name=name,
            description=description,
            element_ids=element_ids or [],
            tags=tags or [],
            parent_boundary_id=parent_boundary_id
        )
        self.add_boundary(boundary)
        return boundary
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the system context diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This is a placeholder that will be implemented by renderers
        return file_path 