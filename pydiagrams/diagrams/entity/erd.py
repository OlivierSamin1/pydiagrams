#!/usr/bin/env python3
"""
Entity Relationship Diagram module for PyDiagrams.

This module provides the implementation for Entity Relationship Diagrams (ERD),
used to visualize database schema with entities (tables) and their relationships.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, Any
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class AttributeType(Enum):
    """Types of attributes in an Entity Relationship Diagram."""
    TEXT = auto()        # Text/string data
    NUMBER = auto()      # Numeric data (integer, float, etc.)
    DATE = auto()        # Date or datetime
    BOOLEAN = auto()     # Boolean/logical value
    BLOB = auto()        # Binary large object
    JSON = auto()        # JSON data
    ENUM = auto()        # Enumeration
    CUSTOM = auto()      # Custom/user-defined type


class RelationshipType(Enum):
    """Types of relationships in an Entity Relationship Diagram."""
    ONE_TO_ONE = auto()          # One-to-one relationship
    ONE_TO_MANY = auto()         # One-to-many relationship
    MANY_TO_ONE = auto()         # Many-to-one relationship
    MANY_TO_MANY = auto()        # Many-to-many relationship
    INHERITANCE = auto()         # Inheritance/generalization relationship
    AGGREGATION = auto()         # Aggregation relationship (whole-part)
    COMPOSITION = auto()         # Composition relationship (strong whole-part)


class Cardinality(Enum):
    """Cardinality options for entity relationships."""
    ZERO_OR_ONE = auto()     # 0..1
    EXACTLY_ONE = auto()     # 1
    ZERO_OR_MANY = auto()    # 0..*
    ONE_OR_MANY = auto()     # 1..*
    CUSTOM = auto()          # Custom cardinality (e.g., "2..5")


@dataclass
class Attribute:
    """
    Represents an attribute (column) in an entity (table).
    
    Attributes are properties that describe an entity.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    attribute_type: AttributeType = AttributeType.TEXT
    data_type: str = ""  # SQL data type or equivalent
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_nullable: bool = True
    is_unique: bool = False
    default_value: Optional[str] = None
    reference_entity_id: Optional[str] = None  # For foreign keys
    reference_attribute_id: Optional[str] = None  # For foreign keys
    custom_type_name: Optional[str] = None  # For custom types
    length: Optional[int] = None  # For types with length constraints
    precision: Optional[int] = None  # For numeric types
    scale: Optional[int] = None  # For numeric types
    constraints: List[str] = field(default_factory=list)  # Additional constraints
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Attribute_{self.id[:8]}"


@dataclass
class Entity:
    """
    Represents an entity (table) in an Entity Relationship Diagram.
    
    An entity represents a concept or object in the data model.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    attributes: List[Attribute] = field(default_factory=list)
    is_weak: bool = False  # Indicates a weak entity
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Entity_{self.id[:8]}"
    
    def add_attribute(self, attribute: Attribute) -> None:
        """Add an attribute to this entity."""
        self.attributes.append(attribute)
    
    def create_attribute(
        self,
        name: str,
        description: str = "",
        attribute_type: AttributeType = AttributeType.TEXT,
        data_type: str = "",
        is_primary_key: bool = False,
        is_foreign_key: bool = False,
        is_nullable: bool = True,
        is_unique: bool = False,
        default_value: Optional[str] = None,
        reference_entity_id: Optional[str] = None,
        reference_attribute_id: Optional[str] = None,
        custom_type_name: Optional[str] = None,
        length: Optional[int] = None,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
        constraints: Optional[List[str]] = None
    ) -> Attribute:
        """
        Create and add an attribute to this entity.
        
        Args:
            name: Name of the attribute
            description: Description of the attribute
            attribute_type: Type of the attribute
            data_type: SQL data type or equivalent
            is_primary_key: Whether this is a primary key
            is_foreign_key: Whether this is a foreign key
            is_nullable: Whether this attribute can be null
            is_unique: Whether this attribute must be unique
            default_value: Default value for the attribute
            reference_entity_id: ID of referenced entity for foreign keys
            reference_attribute_id: ID of referenced attribute for foreign keys
            custom_type_name: Name for custom types
            length: Length constraint for applicable types
            precision: Precision for numeric types
            scale: Scale for numeric types
            constraints: Additional constraints
            
        Returns:
            The created Attribute object
        """
        attribute = Attribute(
            name=name,
            description=description,
            attribute_type=attribute_type,
            data_type=data_type,
            is_primary_key=is_primary_key,
            is_foreign_key=is_foreign_key,
            is_nullable=is_nullable,
            is_unique=is_unique,
            default_value=default_value,
            reference_entity_id=reference_entity_id,
            reference_attribute_id=reference_attribute_id,
            custom_type_name=custom_type_name,
            length=length,
            precision=precision,
            scale=scale,
            constraints=constraints or []
        )
        self.add_attribute(attribute)
        return attribute
    
    def get_primary_keys(self) -> List[Attribute]:
        """Get all primary key attributes."""
        return [attr for attr in self.attributes if attr.is_primary_key]
    
    def get_foreign_keys(self) -> List[Attribute]:
        """Get all foreign key attributes."""
        return [attr for attr in self.attributes if attr.is_foreign_key]


@dataclass
class EntityRelationship:
    """
    Represents a relationship between entities in an ERD.
    
    Relationships define how entities are connected to each other.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    source_entity_id: str = ""  # ID of source entity
    target_entity_id: str = ""  # ID of target entity
    relationship_type: RelationshipType = RelationshipType.ONE_TO_MANY
    source_cardinality: Cardinality = Cardinality.ZERO_OR_MANY
    target_cardinality: Cardinality = Cardinality.EXACTLY_ONE
    source_role: Optional[str] = None  # Role name at source
    target_role: Optional[str] = None  # Role name at target
    identifying: bool = False  # Whether this is an identifying relationship
    source_optional: bool = True  # Whether the source entity is optional
    target_optional: bool = False  # Whether the target entity is optional
    custom_source_cardinality: Optional[str] = None  # For custom cardinality
    custom_target_cardinality: Optional[str] = None  # For custom cardinality
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Relationship_{self.id[:8]}"


class EntityRelationshipDiagram(BaseDiagram):
    """
    Entity Relationship Diagram model.
    
    Entity Relationship Diagrams visualize the structure of databases, including
    entities (tables), their attributes (columns), and relationships between entities.
    """
    
    def __init__(self, name: str, description: str = "", notation: str = "chen"):
        """
        Initialize an entity relationship diagram.
        
        Args:
            name: Diagram name
            description: Optional description
            notation: ERD notation type (chen, crow's foot, etc.)
        """
        super().__init__(name, description)
        self.entities: List[Entity] = []
        self.relationships: List[EntityRelationship] = []
        self.notation = notation
        self.layout = HierarchicalLayout()
    
    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the diagram."""
        self.entities.append(entity)
    
    def add_relationship(self, relationship: EntityRelationship) -> None:
        """Add a relationship to the diagram."""
        self.relationships.append(relationship)
    
    def create_entity(
        self,
        name: str,
        description: str = "",
        is_weak: bool = False,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Entity:
        """
        Create and add an entity to the diagram.
        
        Args:
            name: Name of the entity
            description: Description of the entity
            is_weak: Whether this is a weak entity
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Entity object
        """
        entity = Entity(
            name=name,
            description=description,
            is_weak=is_weak,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_entity(entity)
        return entity
    
    def create_relationship(
        self,
        source_entity_id: str,
        target_entity_id: str,
        name: str = "",
        description: str = "",
        relationship_type: RelationshipType = RelationshipType.ONE_TO_MANY,
        source_cardinality: Cardinality = Cardinality.ZERO_OR_MANY,
        target_cardinality: Cardinality = Cardinality.EXACTLY_ONE,
        source_role: Optional[str] = None,
        target_role: Optional[str] = None,
        identifying: bool = False,
        source_optional: bool = True,
        target_optional: bool = False,
        custom_source_cardinality: Optional[str] = None,
        custom_target_cardinality: Optional[str] = None
    ) -> EntityRelationship:
        """
        Create and add a relationship to the diagram.
        
        Args:
            source_entity_id: ID of the source entity
            target_entity_id: ID of the target entity
            name: Name of the relationship
            description: Description of the relationship
            relationship_type: Type of relationship
            source_cardinality: Cardinality at the source end
            target_cardinality: Cardinality at the target end
            source_role: Role name at the source end
            target_role: Role name at the target end
            identifying: Whether this is an identifying relationship
            source_optional: Whether the source entity is optional
            target_optional: Whether the target entity is optional
            custom_source_cardinality: Custom cardinality at the source end
            custom_target_cardinality: Custom cardinality at the target end
            
        Returns:
            The created EntityRelationship object
        """
        relationship = EntityRelationship(
            name=name,
            description=description,
            source_entity_id=source_entity_id,
            target_entity_id=target_entity_id,
            relationship_type=relationship_type,
            source_cardinality=source_cardinality,
            target_cardinality=target_cardinality,
            source_role=source_role,
            target_role=target_role,
            identifying=identifying,
            source_optional=source_optional,
            target_optional=target_optional,
            custom_source_cardinality=custom_source_cardinality,
            custom_target_cardinality=custom_target_cardinality
        )
        self.add_relationship(relationship)
        return relationship
    
    def find_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """Find an entity by its ID."""
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None
    
    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        """Find an entity by its name."""
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None
    
    def find_relationship_by_id(self, relationship_id: str) -> Optional[EntityRelationship]:
        """Find a relationship by its ID."""
        for relationship in self.relationships:
            if relationship.id == relationship_id:
                return relationship
        return None
    
    def get_relationships_for_entity(self, entity_id: str) -> List[EntityRelationship]:
        """
        Get all relationships involving a specific entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of relationships where the entity is either source or target
        """
        return [r for r in self.relationships 
                if r.source_entity_id == entity_id or r.target_entity_id == entity_id]
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the entity relationship diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This is a placeholder that will be implemented by renderers
        return file_path 