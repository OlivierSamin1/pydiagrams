"""
Class Diagram module for PyDiagrams.

This module provides the implementation for UML Class Diagrams.
"""

from typing import Dict, List, Optional, Union, Any, Tuple
import os

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style, Theme
from pydiagrams.core.layout import Layout, HierarchicalLayout
from pydiagrams.renderers.svg_renderer import SVGRenderer


class Attribute:
    """Class for representing class attributes in a class diagram."""
    
    def __init__(self, name: str, type_name: str = "", visibility: str = "public"):
        """
        Initialize a class attribute.
        
        Args:
            name: Attribute name
            type_name: Data type of the attribute
            visibility: Visibility (public, private, protected, package)
        """
        self.name = name
        self.type_name = type_name
        self.visibility = visibility
        
    def __str__(self) -> str:
        """
        String representation of the attribute.
        
        Returns:
            String representation with visibility prefix and type
        """
        visibility_sign = ""
        if self.visibility == "private":
            visibility_sign = "-"
        elif self.visibility == "protected":
            visibility_sign = "#"
        elif self.visibility == "package":
            visibility_sign = "~"
        else:  # public
            visibility_sign = "+"
            
        type_suffix = f": {self.type_name}" if self.type_name else ""
        return f"{visibility_sign} {self.name}{type_suffix}"


class Method:
    """Class for representing class methods in a class diagram."""
    
    def __init__(
        self, 
        name: str, 
        return_type: str = "", 
        parameters: List[Tuple[str, str]] = None, 
        visibility: str = "public"
    ):
        """
        Initialize a class method.
        
        Args:
            name: Method name
            return_type: Return type of the method
            parameters: List of parameter tuples (name, type)
            visibility: Visibility (public, private, protected, package)
        """
        self.name = name
        self.return_type = return_type
        self.parameters = parameters or []
        self.visibility = visibility
        
    def __str__(self) -> str:
        """
        String representation of the method.
        
        Returns:
            String representation with visibility prefix, parameters and return type
        """
        visibility_sign = ""
        if self.visibility == "private":
            visibility_sign = "-"
        elif self.visibility == "protected":
            visibility_sign = "#"
        elif self.visibility == "package":
            visibility_sign = "~"
        else:  # public
            visibility_sign = "+"
            
        params_str = ", ".join([f"{name}: {type_name}" if type_name else name for name, type_name in self.parameters])
        return_suffix = f": {self.return_type}" if self.return_type else ""
        return f"{visibility_sign} {self.name}({params_str}){return_suffix}"


class Class(DiagramElement):
    """Class for representing classes in a class diagram."""
    
    def __init__(self, name: str, stereotype: str = "", is_abstract: bool = False, element_id: Optional[str] = None):
        """
        Initialize a class element.
        
        Args:
            name: Class name
            stereotype: Optional stereotype
            is_abstract: Whether the class is abstract
            element_id: Optional unique identifier
        """
        super().__init__(name, element_id)
        self.attributes: List[Attribute] = []
        self.methods: List[Method] = []
        self.stereotype = stereotype
        self.is_abstract = is_abstract
        
    def add_attribute(
        self, 
        name: str, 
        type_name: str = "", 
        visibility: str = "public"
    ) -> 'Class':
        """
        Add an attribute to the class.
        
        Args:
            name: Attribute name
            type_name: Data type of the attribute
            visibility: Visibility (public, private, protected, package)
            
        Returns:
            Self for method chaining
        """
        self.attributes.append(Attribute(name, type_name, visibility))
        return self
        
    def add_method(
        self, 
        name: str, 
        return_type: str = "", 
        parameters: List[Tuple[str, str]] = None, 
        visibility: str = "public"
    ) -> 'Class':
        """
        Add a method to the class.
        
        Args:
            name: Method name
            return_type: Return type of the method
            parameters: List of parameter tuples (name, type)
            visibility: Visibility (public, private, protected, package)
            
        Returns:
            Self for method chaining
        """
        self.methods.append(Method(name, return_type, parameters, visibility))
        return self
        
    def render(self) -> Dict:
        """
        Render the class to a dictionary representation.
        
        Returns:
            Dict containing the class's properties for rendering
        """
        attributes_str = [str(attr) for attr in self.attributes]
        methods_str = [str(method) for method in self.methods]
        
        result = {
            "id": self.id,
            "name": self.name,
            "type": "class",
            "stereotype": self.stereotype,
            "is_abstract": self.is_abstract,
            "attributes": attributes_str,
            "methods": methods_str,
            "style": self.style.to_dict(),
            "properties": self.properties
        }
        
        return result


class Interface(Class):
    """Class for representing interfaces in a class diagram."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an interface element.
        
        Args:
            name: Interface name
            element_id: Optional unique identifier
        """
        super().__init__(name, "«interface»", True, element_id)


class Enumeration(DiagramElement):
    """Class for representing enumerations in a class diagram."""
    
    def __init__(self, name: str, element_id: Optional[str] = None):
        """
        Initialize an enumeration element.
        
        Args:
            name: Enumeration name
            element_id: Optional unique identifier
        """
        super().__init__(name, element_id)
        self.values: List[str] = []
        
    def add_value(self, value: str) -> 'Enumeration':
        """
        Add a value to the enumeration.
        
        Args:
            value: Enumeration value
            
        Returns:
            Self for method chaining
        """
        self.values.append(value)
        return self
        
    def render(self) -> Dict:
        """
        Render the enumeration to a dictionary representation.
        
        Returns:
            Dict containing the enumeration's properties for rendering
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": "enumeration",
            "stereotype": "«enumeration»",
            "values": self.values,
            "style": self.style.to_dict(),
            "properties": self.properties
        }


class ClassRelationship(Relationship):
    """Class for representing relationships between classes in a class diagram."""
    
    def __init__(
        self, 
        source: DiagramElement, 
        target: DiagramElement, 
        source_multiplicity: str = "", 
        target_multiplicity: str = "", 
        label: str = "",
        relationship_type: str = "association",
        element_id: Optional[str] = None
    ):
        """
        Initialize a class relationship.
        
        Args:
            source: Source class
            target: Target class
            source_multiplicity: Multiplicity at the source end
            target_multiplicity: Multiplicity at the target end
            label: Relationship label
            relationship_type: Type of relationship (association, inheritance, etc.)
            element_id: Optional unique identifier
        """
        super().__init__(
            source, 
            target, 
            source_multiplicity, 
            target_multiplicity, 
            label, 
            relationship_type, 
            element_id
        )


class ClassDiagram(BaseDiagram):
    """Class for creating and rendering UML Class Diagrams."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a class diagram.
        
        Args:
            name: Diagram name
            description: Optional description
        """
        super().__init__(name, description)
        self.layout = HierarchicalLayout()
        
    def add_class(self, class_element: Class) -> None:
        """
        Add a class to the diagram.
        
        Args:
            class_element: Class element to add
        """
        self.add_element(class_element)
        
    def add_interface(self, interface: Interface) -> None:
        """
        Add an interface to the diagram.
        
        Args:
            interface: Interface element to add
        """
        self.add_element(interface)
        
    def add_enumeration(self, enumeration: Enumeration) -> None:
        """
        Add an enumeration to the diagram.
        
        Args:
            enumeration: Enumeration element to add
        """
        self.add_element(enumeration)
        
    def add_inheritance(self, child: Class, parent: Class) -> ClassRelationship:
        """
        Add an inheritance relationship between classes.
        
        Args:
            child: Child class
            parent: Parent class
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(child, parent, relationship_type="inheritance")
        self.add_relationship(relationship)
        return relationship
        
    def add_implementation(self, implementer: Class, interface: Interface) -> ClassRelationship:
        """
        Add an implementation relationship.
        
        Args:
            implementer: Class implementing the interface
            interface: Interface being implemented
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(implementer, interface, relationship_type="implementation")
        self.add_relationship(relationship)
        return relationship
        
    def add_association(
        self, 
        source: Class, 
        target: Class, 
        source_multiplicity: str = "", 
        target_multiplicity: str = "", 
        label: str = ""
    ) -> ClassRelationship:
        """
        Add an association relationship.
        
        Args:
            source: Source class
            target: Target class
            source_multiplicity: Multiplicity at the source end
            target_multiplicity: Multiplicity at the target end
            label: Association name/label
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(
            source, 
            target, 
            source_multiplicity, 
            target_multiplicity, 
            label, 
            relationship_type="association"
        )
        self.add_relationship(relationship)
        return relationship
        
    def add_aggregation(
        self, 
        container: Class, 
        part: Class, 
        container_multiplicity: str = "", 
        part_multiplicity: str = "", 
        label: str = ""
    ) -> ClassRelationship:
        """
        Add an aggregation relationship.
        
        Args:
            container: Container class
            part: Part class
            container_multiplicity: Multiplicity at the container end
            part_multiplicity: Multiplicity at the part end
            label: Relationship label
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(
            container, 
            part, 
            container_multiplicity, 
            part_multiplicity, 
            label, 
            relationship_type="aggregation"
        )
        self.add_relationship(relationship)
        return relationship
        
    def add_composition(
        self, 
        container: Class, 
        part: Class, 
        container_multiplicity: str = "", 
        part_multiplicity: str = "", 
        label: str = ""
    ) -> ClassRelationship:
        """
        Add a composition relationship.
        
        Args:
            container: Container class
            part: Part class
            container_multiplicity: Multiplicity at the container end
            part_multiplicity: Multiplicity at the part end
            label: Relationship label
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(
            container, 
            part, 
            container_multiplicity, 
            part_multiplicity, 
            label, 
            relationship_type="composition"
        )
        self.add_relationship(relationship)
        return relationship
        
    def add_dependency(
        self, 
        dependent: Class, 
        dependency: Class, 
        label: str = ""
    ) -> ClassRelationship:
        """
        Add a dependency relationship.
        
        Args:
            dependent: Dependent class
            dependency: Class being depended on
            label: Dependency label/stereotype
            
        Returns:
            The created relationship
        """
        relationship = ClassRelationship(
            dependent, 
            dependency, 
            "", 
            "", 
            label, 
            relationship_type="dependency"
        )
        self.add_relationship(relationship)
        return relationship
        
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
            renderer = SVGRenderer()
            return renderer.render(diagram_data, file_path)
        else:
            raise ValueError(f"Unsupported format: {format}. Currently only 'svg' is fully supported.") 