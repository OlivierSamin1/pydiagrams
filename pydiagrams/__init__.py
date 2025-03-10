"""
PyDiagrams - A Python library for creating various types of diagrams.

This library provides tools for creating and rendering different types of diagrams:
- UML Diagrams (Class, Sequence, Activity, etc.)
- Architectural Diagrams (Deployment, Network, etc.)
- Text-based Diagram formats (Mermaid, PlantUML)
- And more...
"""

from . import diagrams
from . import renderers
from . import core
from . import parsers

__version__ = "0.1.0"

__all__ = [
    'diagrams',
    'renderers',
    'core',
    'parsers'
]

# Import core diagram classes for easier access
from pydiagrams.diagrams.uml.class_diagram import ClassDiagram
from pydiagrams.diagrams.uml.sequence_diagram import SequenceDiagram
from pydiagrams.diagrams.uml.activity_diagram import ActivityDiagram
from pydiagrams.diagrams.uml.usecase_diagram import UseCaseDiagram
from pydiagrams.diagrams.uml.state_diagram import StateDiagram

from pydiagrams.diagrams.entity.erd import EntityRelationshipDiagram
from pydiagrams.diagrams.entity.dfd import DataFlowDiagram

from pydiagrams.diagrams.architectural.deployment_diagram import DeploymentDiagram
from pydiagrams.diagrams.architectural.network_diagram import NetworkDiagram
from pydiagrams.diagrams.architectural.context_diagram import SystemContextDiagram
from pydiagrams.diagrams.architectural.container_diagram import ContainerDiagram
from pydiagrams.diagrams.architectural.component_diagram import ComponentDiagram

from pydiagrams.diagrams.code.code_diagram import CodeDiagram

# Import parser classes and utilities
from pydiagrams.parsers.mermaid_parser import MermaidParser
from pydiagrams.parsers.plantuml_parser import PlantUMLParser
from pydiagrams.parsers.diagram_utils import (
    detect_diagram_file_type,
    parse_diagram_file,
    generate_diagram_from_file,
    is_diagram_file
)

# Add convenience functions to the top-level package
def create_diagram_from_file(file_path, output_path=None, output_format='svg'):
    """
    Create a diagram from a Mermaid or PlantUML file.

    Args:
        file_path: Path to the diagram file
        output_path: Path where to save the generated diagram (optional)
        output_format: Output format ('svg', 'png')

    Returns:
        Path to the generated diagram file
    """
    return generate_diagram_from_file(file_path, output_path, output_format) 