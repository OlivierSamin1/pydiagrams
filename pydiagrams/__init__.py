"""
PyDiagrams - A comprehensive Python library for generating various types of diagrams.
"""

__version__ = '0.1.0'

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