#!/usr/bin/env python3
"""
Tests for UML Component Diagram.

This module contains unit tests for the UML Component Diagram implementation.
"""

import unittest
import os
import tempfile
from pathlib import Path

from pydiagrams.diagrams.uml.component_diagram import (
    ComponentDiagram, Component, Interface, Port, 
    Connector, Artifact, InterfaceType, ConnectorType, ComponentType
)
from pydiagrams.renderers.component_renderer import ComponentDiagramRenderer


class TestComponentDiagram(unittest.TestCase):
    """Test case for UML Component Diagram."""
    
    def setUp(self):
        """Set up test cases."""
        self.diagram = ComponentDiagram(
            name="Test Component Diagram",
            description="Test description"
        )
    
    def test_create_component(self):
        """Test creating a component."""
        component = self.diagram.create_component(
            name="TestComponent",
            description="Test component description",
            stereotype="service",
            component_type=ComponentType.COMPONENT
        )
        
        self.assertEqual(component.name, "TestComponent")
        self.assertEqual(component.description, "Test component description")
        self.assertEqual(component.stereotype, "service")
        self.assertEqual(component.component_type, ComponentType.COMPONENT)
        self.assertIn(component, self.diagram.components)
    
    def test_create_interface(self):
        """Test creating an interface."""
        operations = ["operation1()", "operation2()"]
        interface = self.diagram.create_interface(
            name="TestInterface",
            operations=operations,
            interface_type=InterfaceType.PROVIDED
        )
        
        self.assertEqual(interface.name, "TestInterface")
        self.assertEqual(interface.operations, operations)
        self.assertEqual(interface.interface_type, InterfaceType.PROVIDED)
    
    def test_add_provided_interface(self):
        """Test adding a provided interface to a component."""
        component = self.diagram.create_component(name="TestComponent")
        interface = self.diagram.create_interface(
            name="TestInterface",
            interface_type=InterfaceType.REQUIRED  # Initially required
        )
        
        component.add_provided_interface(interface)
        
        self.assertIn(interface, component.provided_interfaces)
        self.assertEqual(interface.interface_type, InterfaceType.PROVIDED)
    
    def test_add_required_interface(self):
        """Test adding a required interface to a component."""
        component = self.diagram.create_component(name="TestComponent")
        interface = self.diagram.create_interface(
            name="TestInterface",
            interface_type=InterfaceType.PROVIDED  # Initially provided
        )
        
        component.add_required_interface(interface)
        
        self.assertIn(interface, component.required_interfaces)
        self.assertEqual(interface.interface_type, InterfaceType.REQUIRED)
    
    def test_create_connector(self):
        """Test creating a connector between components."""
        component1 = self.diagram.create_component(name="Component1")
        component2 = self.diagram.create_component(name="Component2")
        
        connector = self.diagram.create_connector(
            source_id=component1.id,
            target_id=component2.id,
            name="TestConnector",
            connector_type=ConnectorType.DEPENDENCY
        )
        
        self.assertEqual(connector.name, "TestConnector")
        self.assertEqual(connector.source_id, component1.id)
        self.assertEqual(connector.target_id, component2.id)
        self.assertEqual(connector.connector_type, ConnectorType.DEPENDENCY)
        self.assertIn(connector, self.diagram.connectors)
    
    def test_create_artifact(self):
        """Test creating an artifact."""
        artifact = self.diagram.create_artifact(
            name="test.jar",
            description="Test artifact",
            stereotype="artifact"
        )
        
        self.assertEqual(artifact.name, "test.jar")
        self.assertEqual(artifact.description, "Test artifact")
        self.assertEqual(artifact.stereotype, "artifact")
        self.assertIn(artifact, self.diagram.artifacts)
    
    def test_nested_components(self):
        """Test adding nested components."""
        parent = self.diagram.create_component(name="ParentComponent")
        child = self.diagram.create_component(name="ChildComponent")
        
        parent.add_nested_component(child)
        
        self.assertIn(child, parent.nested_components)
    
    def test_render_diagram(self):
        """Test rendering a component diagram."""
        # Create a simple diagram
        component1 = self.diagram.create_component(name="Component1")
        component2 = self.diagram.create_component(name="Component2")
        
        interface = self.diagram.create_interface(name="Interface1")
        component1.add_provided_interface(interface)
        component2.add_required_interface(self.diagram.create_interface(name="Interface2"))
        
        self.diagram.create_connector(
            source_id=component2.id,
            target_id=component1.id,
            connector_type=ConnectorType.DEPENDENCY
        )
        
        self.diagram.create_artifact(name="test.jar")
        
        # Create a temporary file for the rendered diagram
        with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Render the diagram
            renderer = ComponentDiagramRenderer()
            output_path = renderer.render(self.diagram, tmp_path)
            
            # Check if the file exists and has content
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == "__main__":
    unittest.main() 