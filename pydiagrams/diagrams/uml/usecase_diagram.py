"""
Use Case Diagram module for UML use case diagrams.

This module provides classes for creating and manipulating UML Use Case Diagrams.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union, Set

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import Layout


class UseCaseRelationshipType(Enum):
    """Types of relationships in a use case diagram."""
    ASSOCIATION = "association"
    INCLUDE = "include"
    EXTEND = "extend"
    GENERALIZATION = "generalization"


class Actor(DiagramElement):
    """
    Represents an actor in a UML Use Case Diagram.
    
    An actor is a role that a user or external system plays when interacting
    with the system under design.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an actor.
        
        Args:
            name: The name of the actor.
            element_id: Optional unique identifier for the actor.
        """
        super().__init__(name, element_id)
        self.is_primary = True  # Default to primary actor
        self.description = ""
        self.parent: Optional['Actor'] = None
        self.children: List['Actor'] = []
        self.associations: List['UseCaseRelationship'] = []
    
    def set_primary(self, is_primary: bool) -> None:
        """
        Set whether this is a primary actor.
        
        Args:
            is_primary: True if this is a primary actor, False otherwise.
        """
        self.is_primary = is_primary
    
    def set_description(self, description: str) -> None:
        """
        Set the description of the actor.
        
        Args:
            description: The description of the actor.
        """
        self.description = description
    
    def add_child(self, child: 'Actor') -> None:
        """
        Add a child actor (specialization).
        
        Args:
            child: The child actor to add.
        """
        child.parent = self
        self.children.append(child)
    
    def add_association(self, association: 'UseCaseRelationship') -> None:
        """
        Add an association to this actor.
        
        Args:
            association: The association to add.
        """
        self.associations.append(association)
    
    def render(self) -> Dict:
        """
        Render the actor as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the actor.
        """
        data = {
            "id": self.id,
            "type": "actor",
            "name": self.name,
            "is_primary": self.is_primary,
            "description": self.description
        }
        
        return data


class UseCase(DiagramElement):
    """
    Represents a use case in a UML Use Case Diagram.
    
    A use case represents a unit of functionality or a goal that a user
    can achieve with the system.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a use case.
        
        Args:
            name: The name of the use case.
            element_id: Optional unique identifier for the use case.
        """
        super().__init__(name, element_id)
        self.description = ""
        self.preconditions: List[str] = []
        self.postconditions: List[str] = []
        self.main_flow: List[str] = []
        self.alt_flows: Dict[str, List[str]] = {}
        self.includes: List['UseCaseRelationship'] = []
        self.extends: List['UseCaseRelationship'] = []
        self.parent: Optional['UseCase'] = None
        self.children: List['UseCase'] = []
        self.associations: List['UseCaseRelationship'] = []
    
    def set_description(self, description: str) -> None:
        """
        Set the description of the use case.
        
        Args:
            description: The description of the use case.
        """
        self.description = description
    
    def add_precondition(self, precondition: str) -> None:
        """
        Add a precondition to the use case.
        
        Args:
            precondition: The precondition to add.
        """
        self.preconditions.append(precondition)
    
    def add_postcondition(self, postcondition: str) -> None:
        """
        Add a postcondition to the use case.
        
        Args:
            postcondition: The postcondition to add.
        """
        self.postconditions.append(postcondition)
    
    def add_main_flow_step(self, step: str) -> None:
        """
        Add a step to the main flow of the use case.
        
        Args:
            step: The step to add.
        """
        self.main_flow.append(step)
    
    def add_alt_flow(self, name: str, steps: List[str]) -> None:
        """
        Add an alternative flow to the use case.
        
        Args:
            name: The name of the alternative flow.
            steps: The steps in the alternative flow.
        """
        self.alt_flows[name] = steps
    
    def add_include(self, include: 'UseCaseRelationship') -> None:
        """
        Add an include relationship to this use case.
        
        Args:
            include: The include relationship to add.
        """
        self.includes.append(include)
    
    def add_extend(self, extend: 'UseCaseRelationship') -> None:
        """
        Add an extend relationship to this use case.
        
        Args:
            extend: The extend relationship to add.
        """
        self.extends.append(extend)
    
    def add_child(self, child: 'UseCase') -> None:
        """
        Add a child use case (specialization).
        
        Args:
            child: The child use case to add.
        """
        child.parent = self
        self.children.append(child)
    
    def add_association(self, association: 'UseCaseRelationship') -> None:
        """
        Add an association to this use case.
        
        Args:
            association: The association to add.
        """
        self.associations.append(association)
    
    def render(self) -> Dict:
        """
        Render the use case as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the use case.
        """
        data = {
            "id": self.id,
            "type": "usecase",
            "name": self.name,
            "description": self.description,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "main_flow": self.main_flow,
            "alt_flows": self.alt_flows
        }
        
        return data


class System(DiagramElement):
    """
    Represents a system boundary in a UML Use Case Diagram.
    
    A system boundary defines the scope of the system being modeled.
    """
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize a system boundary.
        
        Args:
            name: The name of the system.
            element_id: Optional unique identifier for the system boundary.
        """
        super().__init__(name, element_id)
        self.use_cases: List[UseCase] = []
    
    def add_use_case(self, use_case: UseCase) -> None:
        """
        Add a use case to the system.
        
        Args:
            use_case: The use case to add to the system.
        """
        self.use_cases.append(use_case)
    
    def render(self) -> Dict:
        """
        Render the system boundary as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the system boundary.
        """
        data = {
            "id": self.id,
            "type": "system",
            "name": self.name,
            "use_cases": [uc.id for uc in self.use_cases]
        }
        
        return data


class UseCaseRelationship(Relationship):
    """
    Represents a relationship between elements in a UML Use Case Diagram.
    
    This can be an association, include, extend, or generalization relationship.
    """
    
    def __init__(
        self,
        source: DiagramElement,
        target: DiagramElement,
        relationship_type: UseCaseRelationshipType = UseCaseRelationshipType.ASSOCIATION,
        description: str = "",
        element_id: Optional[str] = None
    ):
        """
        Initialize a relationship between use case elements.
        
        Args:
            source: The source element of the relationship.
            target: The target element of the relationship.
            relationship_type: The type of relationship.
            description: Optional description of the relationship.
            element_id: Optional unique identifier for the relationship.
        """
        # For the base class, we need to convert our specific types to strings
        rel_type_value = relationship_type.value if relationship_type else "association"
        
        # For include and extend, set appropriate labels
        source_label = ""
        target_label = ""
        label = description
        
        super().__init__(
            source, 
            target, 
            source_label, 
            target_label, 
            label, 
            rel_type_value, 
            element_id
        )
        
        self.relationship_type = relationship_type
        self.description = description
        
        # Register with source and target based on relationship type
        if relationship_type == UseCaseRelationshipType.ASSOCIATION:
            if isinstance(source, Actor):
                source.add_association(self)
            elif isinstance(source, UseCase):
                source.add_association(self)
            
            if isinstance(target, Actor):
                target.add_association(self)
            elif isinstance(target, UseCase):
                target.add_association(self)
        
        elif relationship_type == UseCaseRelationshipType.INCLUDE:
            if isinstance(source, UseCase):
                source.add_include(self)
        
        elif relationship_type == UseCaseRelationshipType.EXTEND:
            if isinstance(source, UseCase):
                source.add_extend(self)
        
        elif relationship_type == UseCaseRelationshipType.GENERALIZATION:
            if isinstance(source, Actor) and isinstance(target, Actor):
                target.add_child(source)
            elif isinstance(source, UseCase) and isinstance(target, UseCase):
                target.add_child(source)
    
    def render(self) -> Dict:
        """
        Render the relationship as a dictionary for rendering engines.
        
        Returns:
            A dictionary representation of the relationship.
        """
        data = super().render()
        data.update({
            "relationship_type": self.relationship_type.value,
            "description": self.description
        })
        
        return data


class UseCaseDiagram(BaseDiagram):
    """
    Represents a UML Use Case Diagram.
    
    A use case diagram shows the interactions between actors and
    use cases within a system.
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a UML Use Case Diagram.
        
        Args:
            name: The name of the diagram.
            description: Optional description of the diagram.
        """
        super().__init__(name, description)
        self.actors: List[Actor] = []
        self.use_cases: List[UseCase] = []
        self.systems: List[System] = []
        self.relationships: List[UseCaseRelationship] = []
    
    def add_actor(self, actor: Actor) -> None:
        """
        Add an actor to the diagram.
        
        Args:
            actor: The actor to add.
        """
        self.actors.append(actor)
        self.elements.append(actor)
    
    def add_use_case(self, use_case: UseCase) -> None:
        """
        Add a use case to the diagram.
        
        Args:
            use_case: The use case to add.
        """
        self.use_cases.append(use_case)
        self.elements.append(use_case)
    
    def add_system(self, system: System) -> None:
        """
        Add a system boundary to the diagram.
        
        Args:
            system: The system boundary to add.
        """
        self.systems.append(system)
        self.elements.append(system)
    
    def add_relationship(self, relationship: UseCaseRelationship) -> None:
        """
        Add a relationship to the diagram.
        
        Args:
            relationship: The relationship to add.
        """
        self.relationships.append(relationship)
    
    def create_actor(self, name: str, is_primary: bool = True) -> Actor:
        """
        Create and add an actor to the diagram.
        
        Args:
            name: The name of the actor.
            is_primary: Whether this is a primary actor.
            
        Returns:
            The created actor.
        """
        actor = Actor(name)
        actor.set_primary(is_primary)
        self.add_actor(actor)
        return actor
    
    def create_use_case(self, name: str, description: str = "") -> UseCase:
        """
        Create and add a use case to the diagram.
        
        Args:
            name: The name of the use case.
            description: Optional description of the use case.
            
        Returns:
            The created use case.
        """
        use_case = UseCase(name)
        if description:
            use_case.set_description(description)
        self.add_use_case(use_case)
        return use_case
    
    def create_system(self, name: str) -> System:
        """
        Create and add a system boundary to the diagram.
        
        Args:
            name: The name of the system.
            
        Returns:
            The created system boundary.
        """
        system = System(name)
        self.add_system(system)
        return system
    
    def add_use_case_to_system(self, use_case: UseCase, system: System) -> None:
        """
        Add a use case to a system boundary.
        
        Args:
            use_case: The use case to add.
            system: The system to add the use case to.
        """
        system.add_use_case(use_case)
    
    def create_association(
        self, 
        source: Union[Actor, UseCase], 
        target: Union[Actor, UseCase],
        description: str = ""
    ) -> UseCaseRelationship:
        """
        Create and add an association relationship.
        
        Args:
            source: The source element.
            target: The target element.
            description: Optional description of the association.
            
        Returns:
            The created association relationship.
        """
        relationship = UseCaseRelationship(
            source, 
            target, 
            UseCaseRelationshipType.ASSOCIATION,
            description
        )
        self.add_relationship(relationship)
        return relationship
    
    def create_include(
        self, 
        base: UseCase, 
        inclusion: UseCase,
        description: str = ""
    ) -> UseCaseRelationship:
        """
        Create and add an include relationship.
        
        Args:
            base: The base use case.
            inclusion: The included use case.
            description: Optional description of the inclusion.
            
        Returns:
            The created include relationship.
        """
        relationship = UseCaseRelationship(
            base, 
            inclusion, 
            UseCaseRelationshipType.INCLUDE,
            description or "<<include>>"
        )
        self.add_relationship(relationship)
        return relationship
    
    def create_extend(
        self, 
        extension: UseCase, 
        base: UseCase,
        description: str = ""
    ) -> UseCaseRelationship:
        """
        Create and add an extend relationship.
        
        Args:
            extension: The extending use case.
            base: The base use case.
            description: Optional description of the extension.
            
        Returns:
            The created extend relationship.
        """
        relationship = UseCaseRelationship(
            extension, 
            base, 
            UseCaseRelationshipType.EXTEND,
            description or "<<extend>>"
        )
        self.add_relationship(relationship)
        return relationship
    
    def create_generalization(
        self, 
        child: Union[Actor, UseCase], 
        parent: Union[Actor, UseCase]
    ) -> UseCaseRelationship:
        """
        Create and add a generalization relationship.
        
        Args:
            child: The specialized actor or use case.
            parent: The general actor or use case.
            
        Returns:
            The created generalization relationship.
        """
        # Ensure child and parent are of the same type
        if not (isinstance(child, Actor) and isinstance(parent, Actor)) and \
           not (isinstance(child, UseCase) and isinstance(parent, UseCase)):
            raise ValueError("Child and parent must be of the same type (both Actor or both UseCase)")
        
        relationship = UseCaseRelationship(
            child, 
            parent, 
            UseCaseRelationshipType.GENERALIZATION
        )
        self.add_relationship(relationship)
        return relationship
    
    def set_layout(self, layout: Layout) -> None:
        """
        Set the layout algorithm for the diagram.
        
        Args:
            layout: The layout algorithm to use.
        """
        self.layout = layout
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the use case diagram to a file.
        
        Args:
            file_path: The path where the diagram will be saved.
            format: The format of the output file (default: 'svg').
            
        Returns:
            The path to the rendered file.
        """
        from pydiagrams.renderers.usecase_renderer import UseCaseDiagramRenderer
        
        renderer = UseCaseDiagramRenderer()
        return renderer.render(self.to_dict(), file_path) 