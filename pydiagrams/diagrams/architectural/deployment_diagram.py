#!/usr/bin/env python3
"""
Deployment Diagram module for PyDiagrams.

This module provides the implementation for Deployment Diagrams, which show how
software artifacts are deployed on hardware nodes in a system's architecture.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
import uuid

from pydiagrams.core.base import BaseDiagram, DiagramElement, Relationship
from pydiagrams.core.style import Style
from pydiagrams.core.layout import HierarchicalLayout


class NodeType(Enum):
    """Types of nodes in a Deployment Diagram."""
    DEVICE = auto()  # Physical computing device
    EXECUTION_ENVIRONMENT = auto()  # Software execution environment
    NODE = auto()  # Generic processing resource


class CommunicationType(Enum):
    """Types of communication paths in a Deployment Diagram."""
    NETWORK = auto()  # Network connection
    BUS = auto()  # Hardware bus
    CUSTOM = auto()  # Custom communication type


@dataclass
class DeploymentNode:
    """
    Represents a node in a Deployment Diagram.
    
    A node can be a device (e.g., server, workstation), an execution environment
    (e.g., operating system, container), or a generic processing resource.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    node_type: NodeType = NodeType.NODE
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    artifacts: List['DeploymentArtifact'] = field(default_factory=list)
    nested_nodes: List['DeploymentNode'] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Node_{self.id[:8]}"
    
    def add_artifact(self, artifact: 'DeploymentArtifact') -> None:
        """Add an artifact to this node."""
        self.artifacts.append(artifact)
    
    def add_nested_node(self, node: 'DeploymentNode') -> None:
        """Add a nested node to this node."""
        self.nested_nodes.append(node)


@dataclass
class DeploymentArtifact:
    """
    Represents a deployable artifact in a Deployment Diagram.
    
    Artifacts are physical pieces of information that are used or produced
    by a deployment process (e.g., executables, libraries, data files).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    artifact_type: str = "file"  # e.g., "executable", "library", "configuration"
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Artifact_{self.id[:8]}"


@dataclass
class CommunicationPath:
    """
    Represents a communication path between nodes in a Deployment Diagram.
    
    Communication paths show how nodes interact with each other through
    various means like network connections or hardware buses.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    source_id: str = ""  # ID of source node
    target_id: str = ""  # ID of target node
    communication_type: CommunicationType = CommunicationType.NETWORK
    protocol: Optional[str] = None  # e.g., "HTTP", "TCP/IP"
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Path_{self.id[:8]}"


@dataclass
class Manifest:
    """
    Represents a manifest relationship in a Deployment Diagram.
    
    A manifest relationship shows how an artifact is deployed to a specific node.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    artifact_id: str = ""  # ID of the artifact
    node_id: str = ""  # ID of the node
    stereotype: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            self.name = f"Manifest_{self.id[:8]}"


class DeploymentDiagram(BaseDiagram):
    """
    Deployment Diagram model.
    
    Deployment Diagrams show how software artifacts are deployed on hardware
    nodes in a system's architecture, including the relationships between
    nodes and the communication paths that connect them.
    """
    def __init__(self, name: str, description: str = ""):
        """Initialize a deployment diagram."""
        super().__init__(name, description)
        self.nodes: List[DeploymentNode] = []
        self.artifacts: List[DeploymentArtifact] = []
        self.communication_paths: List[CommunicationPath] = []
        self.manifests: List[Manifest] = []
        self.layout = HierarchicalLayout()
    
    def add_node(self, node: DeploymentNode) -> None:
        """Add a node to the diagram."""
        self.nodes.append(node)
    
    def add_artifact(self, artifact: DeploymentArtifact) -> None:
        """Add an artifact to the diagram."""
        self.artifacts.append(artifact)
    
    def add_communication_path(self, path: CommunicationPath) -> None:
        """Add a communication path to the diagram."""
        self.communication_paths.append(path)
    
    def add_manifest(self, manifest: Manifest) -> None:
        """Add a manifest relationship to the diagram."""
        self.manifests.append(manifest)
    
    def create_node(
        self,
        name: str,
        description: str = "",
        node_type: NodeType = NodeType.NODE,
        stereotype: Optional[str] = None
    ) -> DeploymentNode:
        """Create and add a new node to the diagram."""
        node = DeploymentNode(
            name=name,
            description=description,
            node_type=node_type,
            stereotype=stereotype
        )
        self.nodes.append(node)
        return node
    
    def create_artifact(
        self,
        name: str,
        description: str = "",
        artifact_type: str = "file",
        stereotype: Optional[str] = None
    ) -> DeploymentArtifact:
        """Create and add a new artifact to the diagram."""
        artifact = DeploymentArtifact(
            name=name,
            description=description,
            artifact_type=artifact_type,
            stereotype=stereotype
        )
        self.artifacts.append(artifact)
        return artifact
    
    def create_communication_path(
        self,
        source_id: str,
        target_id: str,
        name: str = "",
        communication_type: CommunicationType = CommunicationType.NETWORK,
        protocol: Optional[str] = None,
        stereotype: Optional[str] = None
    ) -> CommunicationPath:
        """Create and add a new communication path to the diagram."""
        path = CommunicationPath(
            name=name,
            source_id=source_id,
            target_id=target_id,
            communication_type=communication_type,
            protocol=protocol,
            stereotype=stereotype
        )
        self.communication_paths.append(path)
        return path
    
    def create_manifest(
        self,
        artifact_id: str,
        node_id: str,
        name: str = "",
        stereotype: Optional[str] = None
    ) -> Manifest:
        """Create and add a new manifest relationship to the diagram."""
        manifest = Manifest(
            name=name,
            artifact_id=artifact_id,
            node_id=node_id,
            stereotype=stereotype
        )
        self.manifests.append(manifest)
        return manifest

    def render(self, file_path: str, format: str = "svg") -> str:
        """
        Render the diagram to a file.
        
        Args:
            file_path: Path where the diagram should be saved
            format: Output format (currently only 'svg' is fully implemented)
            
        Returns:
            Path to the rendered file
        """
        # This is a stub implementation
        raise NotImplementedError("Deployment Diagram rendering is not yet implemented.") 