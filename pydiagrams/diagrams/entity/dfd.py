#!/usr/bin/env python3
"""
Data Flow Diagram module for PyDiagrams.

This module provides the implementation for Data Flow Diagrams (DFD),
used to visualize how data moves through a system, including processes,
data stores, external entities, and data flows.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Any
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class ElementType(Enum):
    """Types of elements in a Data Flow Diagram."""
    PROCESS = auto()          # Represents a process that transforms data
    DATA_STORE = auto()       # Represents a data store (e.g., database, file)
    EXTERNAL_ENTITY = auto()  # Represents an external entity (source or sink of data)
    TRUST_BOUNDARY = auto()   # Represents a trust boundary (security context)


class FlowType(Enum):
    """Types of data flows in a Data Flow Diagram."""
    DATA = auto()             # Regular data flow
    CONTROL = auto()          # Control flow (signals or triggers)
    EVENT = auto()            # Event flow
    RESPONSE = auto()         # Response flow
    BIDIRECTIONAL = auto()    # Bidirectional flow


@dataclass
class DFDElement:
    """
    Base class for elements in a Data Flow Diagram.
    
    Elements include processes, data stores, and external entities.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    element_type: ElementType = ElementType.PROCESS
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Element_{self.id[:8]}"


@dataclass
class Process(DFDElement):
    """
    Represents a process in a Data Flow Diagram.
    
    A process transforms data inputs into outputs.
    """
    process_number: Optional[str] = None  # Process numbering (e.g., "1.0", "2.1")
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        process_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a process element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=ElementType.PROCESS,
            tags=tags or [],
            properties=properties or {}
        )
        self.process_number = process_number


@dataclass
class DataStore(DFDElement):
    """
    Represents a data store in a Data Flow Diagram.
    
    A data store holds data for later use (e.g., a database, file, or memory).
    """
    store_number: Optional[str] = None  # Store numbering (e.g., "D1", "D2")
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        store_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a data store element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=ElementType.DATA_STORE,
            tags=tags or [],
            properties=properties or {}
        )
        self.store_number = store_number


@dataclass
class ExternalEntity(DFDElement):
    """
    Represents an external entity in a Data Flow Diagram.
    
    An external entity is a source or sink of data outside the system.
    """
    entity_number: Optional[str] = None  # Entity numbering (e.g., "E1", "E2")
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        entity_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize an external entity element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=ElementType.EXTERNAL_ENTITY,
            tags=tags or [],
            properties=properties or {}
        )
        self.entity_number = entity_number


@dataclass
class TrustBoundary(DFDElement):
    """
    Represents a trust boundary in a Data Flow Diagram.
    
    A trust boundary separates areas of differing security levels or domains.
    """
    element_ids: List[str] = field(default_factory=list)  # IDs of elements within this boundary
    
    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "",
        description: str = "",
        element_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ):
        """Initialize a trust boundary element."""
        super().__init__(
            id=id or str(uuid.uuid4()),
            name=name,
            description=description,
            element_type=ElementType.TRUST_BOUNDARY,
            tags=tags or [],
            properties=properties or {}
        )
        self.element_ids = element_ids or []
    
    def add_element_id(self, element_id: str) -> None:
        """Add an element to this trust boundary."""
        if element_id not in self.element_ids:
            self.element_ids.append(element_id)


@dataclass
class DataFlow:
    """
    Represents a data flow in a Data Flow Diagram.
    
    Data flows show the movement of data between processes, data stores,
    and external entities.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    source_id: str = ""  # ID of source element
    target_id: str = ""  # ID of target element
    flow_type: FlowType = FlowType.DATA
    data_items: List[str] = field(default_factory=list)  # Data items being transferred
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Flow_{self.id[:8]}"


class DataFlowDiagram(BaseDiagram):
    """
    Data Flow Diagram model.
    
    Data Flow Diagrams show how data moves through a system, including processes
    that transform data, data stores, external entities, and the flows between them.
    """
    
    def __init__(self, name: str, description: str = "", level: int = 0):
        """
        Initialize a data flow diagram.
        
        Args:
            name: Diagram name
            description: Optional description
            level: DFD level (0 for context diagram, 1+ for detailed levels)
        """
        super().__init__(name, description)
        self.processes: List[Process] = []
        self.data_stores: List[DataStore] = []
        self.external_entities: List[ExternalEntity] = []
        self.trust_boundaries: List[TrustBoundary] = []
        self.data_flows: List[DataFlow] = []
        self.level = level
        self.layout = HierarchicalLayout()
    
    def add_process(self, process: Process) -> None:
        """Add a process to the diagram."""
        self.processes.append(process)
    
    def add_data_store(self, data_store: DataStore) -> None:
        """Add a data store to the diagram."""
        self.data_stores.append(data_store)
    
    def add_external_entity(self, external_entity: ExternalEntity) -> None:
        """Add an external entity to the diagram."""
        self.external_entities.append(external_entity)
    
    def add_trust_boundary(self, trust_boundary: TrustBoundary) -> None:
        """Add a trust boundary to the diagram."""
        self.trust_boundaries.append(trust_boundary)
    
    def add_data_flow(self, data_flow: DataFlow) -> None:
        """Add a data flow to the diagram."""
        self.data_flows.append(data_flow)
    
    def create_process(
        self,
        name: str,
        description: str = "",
        process_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> Process:
        """
        Create and add a process to the diagram.
        
        Args:
            name: Name of the process
            description: Description of the process
            process_number: Process numbering (e.g., "1.0", "2.1")
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created Process object
        """
        process = Process(
            name=name,
            description=description,
            process_number=process_number,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_process(process)
        return process
    
    def create_data_store(
        self,
        name: str,
        description: str = "",
        store_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> DataStore:
        """
        Create and add a data store to the diagram.
        
        Args:
            name: Name of the data store
            description: Description of the data store
            store_number: Store numbering (e.g., "D1", "D2")
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created DataStore object
        """
        data_store = DataStore(
            name=name,
            description=description,
            store_number=store_number,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_data_store(data_store)
        return data_store
    
    def create_external_entity(
        self,
        name: str,
        description: str = "",
        entity_number: Optional[str] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> ExternalEntity:
        """
        Create and add an external entity to the diagram.
        
        Args:
            name: Name of the external entity
            description: Description of the external entity
            entity_number: Entity numbering (e.g., "E1", "E2")
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created ExternalEntity object
        """
        external_entity = ExternalEntity(
            name=name,
            description=description,
            entity_number=entity_number,
            tags=tags or [],
            properties=properties or {}
        )
        self.add_external_entity(external_entity)
        return external_entity
    
    def create_trust_boundary(
        self,
        name: str,
        description: str = "",
        element_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> TrustBoundary:
        """
        Create and add a trust boundary to the diagram.
        
        Args:
            name: Name of the trust boundary
            description: Description of the trust boundary
            element_ids: IDs of elements within this boundary
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created TrustBoundary object
        """
        trust_boundary = TrustBoundary(
            name=name,
            description=description,
            element_ids=element_ids or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_trust_boundary(trust_boundary)
        return trust_boundary
    
    def create_data_flow(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        description: str = "",
        flow_type: FlowType = FlowType.DATA,
        data_items: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, str]] = None
    ) -> DataFlow:
        """
        Create and add a data flow to the diagram.
        
        Args:
            source_id: ID of the source element
            target_id: ID of the target element
            name: Name of the data flow
            description: Description of the data flow
            flow_type: Type of flow (data, control, etc.)
            data_items: List of data items being transferred
            tags: Optional list of tags for filtering or styling
            properties: Optional dictionary of additional properties
            
        Returns:
            The created DataFlow object
        """
        data_flow = DataFlow(
            name=name,
            description=description,
            source_id=source_id,
            target_id=target_id,
            flow_type=flow_type,
            data_items=data_items or [],
            tags=tags or [],
            properties=properties or {}
        )
        self.add_data_flow(data_flow)
        return data_flow
    
    def find_element_by_id(self, element_id: str) -> Optional[DFDElement]:
        """Find an element by its ID."""
        # Search in processes
        for process in self.processes:
            if process.id == element_id:
                return process
        
        # Search in data stores
        for data_store in self.data_stores:
            if data_store.id == element_id:
                return data_store
        
        # Search in external entities
        for external_entity in self.external_entities:
            if external_entity.id == element_id:
                return external_entity
        
        # Search in trust boundaries
        for trust_boundary in self.trust_boundaries:
            if trust_boundary.id == element_id:
                return trust_boundary
        
        return None
    
    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the data flow diagram to a file.
        
        Args:
            file_path: Path to save the rendered diagram
            format: Output format (svg, png, etc.)
            
        Returns:
            The path to the rendered file
        """
        # This is a placeholder that will be implemented by renderers
        return file_path 