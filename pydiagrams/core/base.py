"""
Base classes for PyDiagrams.

This module defines the abstract base classes that serve as the foundation
for all diagram types in the PyDiagrams library.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
import uuid

from pydiagrams.core.style import Style


class DiagramElement(ABC):
    """Base class for all diagram elements."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a diagram element.
        
        Args:
            name: The name of the element
            element_id: Optional unique identifier, generated if not provided
        """
        self.name = name
        self.id = element_id or str(uuid.uuid4())
        self.style = Style()
        self.properties: Dict[str, str] = {}
        
    def add_property(self, key: str, value: str) -> None:
        """
        Add a property to the element.
        
        Args:
            key: Property name
            value: Property value
        """
        self.properties[key] = value
        
    def set_style(self, style: Style) -> None:
        """
        Set the element's style.
        
        Args:
            style: The style to apply to this element
        """
        self.style = style
        
    @abstractmethod
    def render(self) -> Dict:
        """
        Render the element to a dictionary representation.
        
        Returns:
            Dict containing the element's properties for rendering
        """
        pass


class Relationship(DiagramElement):
    """Base class for relationships between diagram elements."""
    
    def __init__(
        self, 
        source: DiagramElement, 
        target: DiagramElement, 
        source_label: str = "", 
        target_label: str = "", 
        label: str = "",
        relationship_type: str = "default",
        element_id: Optional[str] = None
    ):
        """
        Initialize a relationship between two elements.
        
        Args:
            source: Source element
            target: Target element
            source_label: Label at the source end of the relationship
            target_label: Label at the target end of the relationship
            label: Label for the relationship itself
            relationship_type: Type of the relationship (e.g. "inheritance", "association")
            element_id: Optional unique identifier
        """
        super().__init__(label, element_id)
        self.source = source
        self.target = target
        self.source_label = source_label
        self.target_label = target_label
        self.relationship_type = relationship_type
        
    def render(self) -> Dict:
        """
        Render the relationship to a dictionary representation.
        
        Returns:
            Dict containing the relationship's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "relationship",
            "relationship_type": self.relationship_type,
            "source_id": self.source.id,
            "target_id": self.target.id,
            "source_label": self.source_label,
            "target_label": self.target_label,
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class BaseDiagram(ABC):
    """Base class for all diagrams."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a diagram.
        
        Args:
            name: The name of the diagram
            description: Optional description of the diagram
        """
        self.name = name
        self.description = description
        self.elements: List[DiagramElement] = []
        self.relationships: List[Relationship] = []
        self.id = str(uuid.uuid4())
        self.style = Style()
        
    def add_element(self, element: DiagramElement) -> None:
        """
        Add an element to the diagram.
        
        Args:
            element: The element to add
        """
        self.elements.append(element)
        
    def add_elements(self, elements: List[DiagramElement]) -> None:
        """
        Add multiple elements to the diagram.
        
        Args:
            elements: List of elements to add
        """
        self.elements.extend(elements)
        
    def add_relationship(self, relationship: Relationship) -> None:
        """
        Add a relationship to the diagram.
        
        Args:
            relationship: The relationship to add
        """
        self.relationships.append(relationship)
        
    def add_relationships(self, relationships: List[Relationship]) -> None:
        """
        Add multiple relationships to the diagram.
        
        Args:
            relationships: List of relationships to add
        """
        self.relationships.extend(relationships)
        
    def set_style(self, style: Style) -> None:
        """
        Set the diagram's style.
        
        Args:
            style: The style to apply to this diagram
        """
        self.style = style
        
    @abstractmethod
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the diagram to a file.
        
        Args:
            file_path: Path where the diagram should be saved
            format: Output format (e.g., 'svg', 'png', 'pdf')
            
        Returns:
            Path to the rendered file
        """
        pass
    
    def to_dict(self) -> Dict:
        """
        Convert the diagram to a dictionary representation.
        
        Returns:
            Dict containing the diagram's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.__class__.__name__,
            "elements": [element.render() for element in self.elements],
            "relationships": [relationship.render() for relationship in self.relationships],
            "style": self.style.to_dict()
        } 