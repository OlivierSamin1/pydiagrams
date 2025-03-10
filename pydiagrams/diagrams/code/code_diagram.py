#!/usr/bin/env python3
"""
Code Diagram module for PyDiagrams.

This module provides the implementation for Code Diagrams which visualize
code structures such as modules, classes, functions, and dependencies.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Any
import os
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class CodeElementType(Enum):
    """Types of elements in a Code Diagram."""
    MODULE = auto()      # Represents a module or package
    CLASS = auto()       # Represents a class
    FUNCTION = auto()    # Represents a function or method
    VARIABLE = auto()    # Represents a variable or constant
    INTERFACE = auto()   # Represents an interface
    ENUM = auto()        # Represents an enumeration


class RelationshipType(Enum):
    """Types of relationships between code elements."""
    IMPORT = auto()          # Import relationship between modules
    INHERITANCE = auto()     # Class inheritance
    IMPLEMENTATION = auto()  # Interface implementation
    DEPENDENCY = auto()      # Usage/dependency relationship
    COMPOSITION = auto()     # Composition relationship (strong whole-part)
    AGGREGATION = auto()     # Aggregation relationship (weak whole-part)
    CALL = auto()            # Function/method call
    ACCESS = auto()          # Variable/attribute access
    REFERENCE = auto()       # General reference


class AccessModifier(Enum):
    """Access modifiers for code elements."""
    PUBLIC = auto()      # Public access
    PRIVATE = auto()     # Private access
    PROTECTED = auto()   # Protected access
    PACKAGE = auto()     # Package/default access
    INTERNAL = auto()    # Internal access (e.g., C# internal)


@dataclass
class CodeElement:
    """
    Base class for elements in a Code Diagram.
    
    Represents a code element like a module, class, function, or variable.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    element_type: CodeElementType = CodeElementType.MODULE
    access_modifier: Optional[AccessModifier] = None
    is_static: bool = False
    is_abstract: bool = False
    is_final: bool = False
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    language: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    children: List['CodeElement'] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Element_{self.id[:8]}"
    
    def add_child(self, child: 'CodeElement') -> None:
        """Add a child element to this element."""
        self.children.append(child)


@dataclass
class Module(CodeElement):
    """
    Represents a module or package in a code base.
    
    A module can contain classes, functions, variables, and submodules.
    """
    imports: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        source_file: Optional[str] = None,
        language: Optional[str] = None,
        imports: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a module element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.MODULE,
            source_file=source_file,
            language=language,
            tags=tags or [],
            properties=properties or {}
        )
        self.imports = imports or []
    
    def add_import(self, import_name: str) -> None:
        """Add an import to this module."""
        if import_name not in self.imports:
            self.imports.append(import_name)


@dataclass
class Class(CodeElement):
    """
    Represents a class in a code base.
    
    A class can contain methods, attributes, and inner classes.
    """
    superclasses: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_abstract: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        superclasses: Optional[List[str]] = None,
        interfaces: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a class element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.CLASS,
            access_modifier=access_modifier,
            is_static=is_static,
            is_abstract=is_abstract,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language,
            tags=tags or [],
            properties=properties or []
        )
        self.superclasses = superclasses or []
        self.interfaces = interfaces or []
    
    def add_superclass(self, superclass_name: str) -> None:
        """Add a superclass to this class."""
        if superclass_name not in self.superclasses:
            self.superclasses.append(superclass_name)
    
    def add_interface(self, interface_name: str) -> None:
        """Add an implemented interface to this class."""
        if interface_name not in self.interfaces:
            self.interfaces.append(interface_name)


@dataclass
class Interface(CodeElement):
    """
    Represents an interface in a code base.
    
    An interface can contain method signatures and constants.
    """
    superinterfaces: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        superinterfaces: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize an interface element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.INTERFACE,
            access_modifier=access_modifier,
            is_abstract=True,  # Interfaces are always abstract
            source_file=source_file,
            line_number=line_number,
            language=language,
            tags=tags or [],
            properties=properties or []
        )
        self.superinterfaces = superinterfaces or []
    
    def add_superinterface(self, interface_name: str) -> None:
        """Add a superinterface to this interface."""
        if interface_name not in self.superinterfaces:
            self.superinterfaces.append(interface_name)


@dataclass
class Function(CodeElement):
    """
    Represents a function or method in a code base.
    
    A function can have parameters and return values.
    """
    parameters: List[Tuple[str, str]] = field(default_factory=list)  # (name, type)
    return_type: Optional[str] = None
    is_constructor: bool = False
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_abstract: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        parameters: Optional[List[Tuple[str, str]]] = None,
        return_type: Optional[str] = None,
        is_constructor: bool = False,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a function element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.FUNCTION,
            access_modifier=access_modifier,
            is_static=is_static,
            is_abstract=is_abstract,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language,
            tags=tags or [],
            properties=properties or []
        )
        self.parameters = parameters or []
        self.return_type = return_type
        self.is_constructor = is_constructor
    
    def add_parameter(self, name: str, param_type: str) -> None:
        """Add a parameter to this function."""
        self.parameters.append((name, param_type))


@dataclass
class Variable(CodeElement):
    """
    Represents a variable or constant in a code base.
    
    A variable has a type and can have an initial value.
    """
    var_type: Optional[str] = None
    initial_value: Optional[str] = None
    is_constant: bool = False
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        var_type: Optional[str] = None,
        initial_value: Optional[str] = None,
        is_constant: bool = False,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a variable element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.VARIABLE,
            access_modifier=access_modifier,
            is_static=is_static,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language,
            tags=tags or [],
            properties=properties or []
        )
        self.var_type = var_type
        self.initial_value = initial_value
        self.is_constant = is_constant


@dataclass
class Enum(CodeElement):
    """
    Represents an enumeration in a code base.
    
    An enum contains a set of constant values.
    """
    values: List[str] = field(default_factory=list)
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        values: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize an enum element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=CodeElementType.ENUM,
            access_modifier=access_modifier,
            source_file=source_file,
            line_number=line_number,
            language=language,
            tags=tags or [],
            properties=properties or []
        )
        self.values = values or []
    
    def add_value(self, value: str) -> None:
        """Add a value to this enum."""
        if value not in self.values:
            self.values.append(value)


@dataclass
class CodeRelationship:
    """
    Represents a relationship between code elements.
    
    Relationships can represent imports, inheritance, calls, etc.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    source_id: str = ""  # ID of source element
    target_id: str = ""  # ID of target element
    relationship_type: RelationshipType = RelationshipType.DEPENDENCY
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Relationship_{self.id[:8]}"


class CodeDiagram(BaseDiagram):
    """
    Code Diagram model.
    
    Code Diagrams visualize code structures such as modules, classes, functions,
    and their relationships like inheritance, dependencies, and calls.
    """
    
    def __init__(self, name: str, description: str = "", language: str = ""):
        """
        Initialize a code diagram.
        
        Args:
            name: Diagram name
            description: Optional description
            language: Programming language of the code being visualized
        """
        super().__init__(name, description)
        self.modules: List[Module] = []
        self.classes: List[Class] = []
        self.interfaces: List[Interface] = []
        self.functions: List[Function] = []
        self.variables: List[Variable] = []
        self.enums: List[Enum] = []
        self.relationships: List[CodeRelationship] = []
        self.language = language
        self.layout = HierarchicalLayout()
    
    def add_module(self, module: Module) -> None:
        """Add a module to the diagram."""
        self.modules.append(module)
    
    def add_class(self, class_obj: Class) -> None:
        """Add a class to the diagram."""
        self.classes.append(class_obj)
    
    def add_interface(self, interface: Interface) -> None:
        """Add an interface to the diagram."""
        self.interfaces.append(interface)
    
    def add_function(self, function: Function) -> None:
        """Add a function to the diagram."""
        self.functions.append(function)
    
    def add_variable(self, variable: Variable) -> None:
        """Add a variable to the diagram."""
        self.variables.append(variable)
    
    def add_enum(self, enum: Enum) -> None:
        """Add an enum to the diagram."""
        self.enums.append(enum)
    
    def add_relationship(self, relationship: CodeRelationship) -> None:
        """Add a relationship to the diagram."""
        self.relationships.append(relationship)
    
    def create_module(
        self,
        name: str,
        description: str = "",
        source_file: Optional[str] = None,
        language: Optional[str] = None,
        imports: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Module:
        """
        Create and add a module to the diagram.
        
        Args:
            name: Name of the module
            description: Description of the module
            source_file: Source file path
            language: Programming language
            imports: List of imports
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Module object
        """
        module = Module(
            name=name,
            description=description,
            source_file=source_file,
            language=language or self.language,
            imports=imports or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_module(module)
        return module
    
    def create_class(
        self,
        name: str,
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_abstract: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        superclasses: Optional[List[str]] = None,
        interfaces: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Class:
        """
        Create and add a class to the diagram.
        
        Args:
            name: Name of the class
            description: Description of the class
            access_modifier: Access modifier (public, private, etc.)
            is_static: Whether the class is static
            is_abstract: Whether the class is abstract
            is_final: Whether the class is final
            source_file: Source file path
            line_number: Line number in the source file
            language: Programming language
            superclasses: List of superclass names
            interfaces: List of implemented interface names
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Class object
        """
        class_obj = Class(
            name=name,
            description=description,
            access_modifier=access_modifier,
            is_static=is_static,
            is_abstract=is_abstract,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language or self.language,
            superclasses=superclasses or [],
            interfaces=interfaces or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_class(class_obj)
        return class_obj
    
    def create_interface(
        self,
        name: str,
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        superinterfaces: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Interface:
        """
        Create and add an interface to the diagram.
        
        Args:
            name: Name of the interface
            description: Description of the interface
            access_modifier: Access modifier (public, private, etc.)
            source_file: Source file path
            line_number: Line number in the source file
            language: Programming language
            superinterfaces: List of superinterface names
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Interface object
        """
        interface = Interface(
            name=name,
            description=description,
            access_modifier=access_modifier,
            source_file=source_file,
            line_number=line_number,
            language=language or self.language,
            superinterfaces=superinterfaces or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_interface(interface)
        return interface
    
    def create_function(
        self,
        name: str,
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_abstract: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        parameters: Optional[List[Tuple[str, str]]] = None,
        return_type: Optional[str] = None,
        is_constructor: bool = False,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Function:
        """
        Create and add a function to the diagram.
        
        Args:
            name: Name of the function
            description: Description of the function
            access_modifier: Access modifier (public, private, etc.)
            is_static: Whether the function is static
            is_abstract: Whether the function is abstract
            is_final: Whether the function is final
            source_file: Source file path
            line_number: Line number in the source file
            language: Programming language
            parameters: List of parameter (name, type) tuples
            return_type: Return type of the function
            is_constructor: Whether the function is a constructor
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Function object
        """
        function = Function(
            name=name,
            description=description,
            access_modifier=access_modifier,
            is_static=is_static,
            is_abstract=is_abstract,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language or self.language,
            parameters=parameters or [],
            return_type=return_type,
            is_constructor=is_constructor,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_function(function)
        return function
    
    def create_variable(
        self,
        name: str,
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        is_static: bool = False,
        is_final: bool = False,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        var_type: Optional[str] = None,
        initial_value: Optional[str] = None,
        is_constant: bool = False,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Variable:
        """
        Create and add a variable to the diagram.
        
        Args:
            name: Name of the variable
            description: Description of the variable
            access_modifier: Access modifier (public, private, etc.)
            is_static: Whether the variable is static
            is_final: Whether the variable is final
            source_file: Source file path
            line_number: Line number in the source file
            language: Programming language
            var_type: Type of the variable
            initial_value: Initial value of the variable
            is_constant: Whether the variable is a constant
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Variable object
        """
        variable = Variable(
            name=name,
            description=description,
            access_modifier=access_modifier,
            is_static=is_static,
            is_final=is_final,
            source_file=source_file,
            line_number=line_number,
            language=language or self.language,
            var_type=var_type,
            initial_value=initial_value,
            is_constant=is_constant,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_variable(variable)
        return variable
    
    def create_enum(
        self,
        name: str,
        description: str = "",
        access_modifier: Optional[AccessModifier] = AccessModifier.PUBLIC,
        source_file: Optional[str] = None,
        line_number: Optional[int] = None,
        language: Optional[str] = None,
        values: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Enum:
        """
        Create and add an enum to the diagram.
        
        Args:
            name: Name of the enum
            description: Description of the enum
            access_modifier: Access modifier (public, private, etc.)
            source_file: Source file path
            line_number: Line number in the source file
            language: Programming language
            values: List of enum values
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Enum object
        """
        enum = Enum(
            name=name,
            description=description,
            access_modifier=access_modifier,
            source_file=source_file,
            line_number=line_number,
            language=language or self.language,
            values=values or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_enum(enum)
        return enum
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        description: str = "",
        relationship_type: RelationshipType = RelationshipType.DEPENDENCY,
        properties: Optional[Dict[str, str]] = None
    ) -> CodeRelationship:
        """
        Create and add a relationship to the diagram.
        
        Args:
            source_id: ID of the source element
            target_id: ID of the target element
            name: Name of the relationship
            description: Description of the relationship
            relationship_type: Type of relationship
            properties: Optional dictionary of additional properties
            
        Returns:
            The created CodeRelationship object
        """
        relationship = CodeRelationship(
            name=name,
            description=description,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {}
        )
        self.add_relationship(relationship)
        return relationship
    
    def find_element_by_id(self, element_id: str) -> Optional[CodeElement]:
        """Find an element by its ID."""
        # Search in all element lists
        for module in self.modules:
            if module.id == element_id:
                return module
        
        for class_obj in self.classes:
            if class_obj.id == element_id:
                return class_obj
        
        for interface in self.interfaces:
            if interface.id == element_id:
                return interface
        
        for function in self.functions:
            if function.id == element_id:
                return function
        
        for variable in self.variables:
            if variable.id == element_id:
                return variable
        
        for enum in self.enums:
            if enum.id == element_id:
                return enum
        
        return None
    
    def find_element_by_name(self, name: str, element_type: Optional[CodeElementType] = None) -> Optional[CodeElement]:
        """Find an element by its name and optionally its type."""
        # If element_type is specified, search only in the corresponding list
        if element_type == CodeElementType.MODULE:
            for module in self.modules:
                if module.name == name:
                    return module
        elif element_type == CodeElementType.CLASS:
            for class_obj in self.classes:
                if class_obj.name == name:
                    return class_obj
        elif element_type == CodeElementType.INTERFACE:
            for interface in self.interfaces:
                if interface.name == name:
                    return interface
        elif element_type == CodeElementType.FUNCTION:
            for function in self.functions:
                if function.name == name:
                    return function
        elif element_type == CodeElementType.VARIABLE:
            for variable in self.variables:
                if variable.name == name:
                    return variable
        elif element_type == CodeElementType.ENUM:
            for enum in self.enums:
                if enum.name == name:
                    return enum
        else:
            # If no element_type is specified, search in all lists
            for module in self.modules:
                if module.name == name:
                    return module
            for class_obj in self.classes:
                if class_obj.name == name:
                    return class_obj
            for interface in self.interfaces:
                if interface.name == name:
                    return interface
            for function in self.functions:
                if function.name == name:
                    return function
            for variable in self.variables:
                if variable.name == name:
                    return variable
            for enum in self.enums:
                if enum.name == name:
                    return enum
        
        return None
    
    def find_relationship_by_id(self, relationship_id: str) -> Optional[CodeRelationship]:
        """Find a relationship by its ID."""
        for relationship in self.relationships:
            if relationship.id == relationship_id:
                return relationship
        return None
    
    def get_relationships_for_element(self, element_id: str) -> List[CodeRelationship]:
        """
        Get all relationships involving a specific element.
        
        Args:
            element_id: ID of the element
            
        Returns:
            List of relationships where the element is either source or target
        """
        return [r for r in self.relationships 
                if r.source_id == element_id or r.target_id == element_id]
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the code diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This will be implemented by renderers
        return file_path 