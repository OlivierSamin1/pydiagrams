"""
Tests for the Class Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams import ClassDiagram
from pydiagrams.diagrams.uml.class_diagram import Class, Interface, Enumeration, ClassRelationship


class TestClassDiagram(unittest.TestCase):
    """Test cases for the ClassDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = ClassDiagram("Test Class Diagram")
        
    def test_class_creation(self):
        """Test that a class can be created and added to the diagram."""
        test_class = Class("TestClass")
        test_class.add_attribute("attr1", "int", "private")
        test_class.add_method("method1", "void")
        
        self.diagram.add_class(test_class)
        
        # Check that the class was added to the diagram
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertEqual(self.diagram.elements[0].name, "TestClass")
        
    def test_interface_creation(self):
        """Test that an interface can be created and added to the diagram."""
        test_interface = Interface("TestInterface")
        test_interface.add_method("method1", "void")
        
        self.diagram.add_interface(test_interface)
        
        # Check that the interface was added to the diagram
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertEqual(self.diagram.elements[0].name, "TestInterface")
        self.assertEqual(self.diagram.elements[0].stereotype, "«interface»")
        self.assertTrue(self.diagram.elements[0].is_abstract)
        
    def test_enumeration_creation(self):
        """Test that an enumeration can be created and added to the diagram."""
        test_enum = Enumeration("TestEnum")
        test_enum.add_value("VALUE1")
        test_enum.add_value("VALUE2")
        
        self.diagram.add_enumeration(test_enum)
        
        # Check that the enumeration was added to the diagram
        self.assertEqual(len(self.diagram.elements), 1)
        self.assertEqual(self.diagram.elements[0].name, "TestEnum")
        self.assertEqual(len(self.diagram.elements[0].values), 2)
        
    def test_relationship_creation(self):
        """Test that relationships can be created between classes."""
        class1 = Class("Class1")
        class2 = Class("Class2")
        
        self.diagram.add_class(class1)
        self.diagram.add_class(class2)
        
        # Add an association relationship
        relation = self.diagram.add_association(class1, class2, "1", "*", "owns")
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertEqual(self.diagram.relationships[0].source, class1)
        self.assertEqual(self.diagram.relationships[0].target, class2)
        self.assertEqual(self.diagram.relationships[0].source_label, "1")
        self.assertEqual(self.diagram.relationships[0].target_label, "*")
        self.assertEqual(self.diagram.relationships[0].name, "owns")
        
    def test_inheritance_relationship(self):
        """Test that inheritance relationships can be created."""
        parent = Class("Parent")
        child = Class("Child")
        
        self.diagram.add_class(parent)
        self.diagram.add_class(child)
        
        # Add an inheritance relationship
        relation = self.diagram.add_inheritance(child, parent)
        
        # Check that the relationship was added
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertEqual(self.diagram.relationships[0].source, child)
        self.assertEqual(self.diagram.relationships[0].target, parent)
        self.assertEqual(self.diagram.relationships[0].relationship_type, "inheritance")
        
    def test_implementation_relationship(self):
        """Test that implementation relationships can be created."""
        interface = Interface("TestInterface")
        implementer = Class("Implementer")
        
        self.diagram.add_interface(interface)
        self.diagram.add_class(implementer)
        
        # Add an implementation relationship
        relation = self.diagram.add_implementation(implementer, interface)
        
        # Check that the relationship was added
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertEqual(self.diagram.relationships[0].source, implementer)
        self.assertEqual(self.diagram.relationships[0].target, interface)
        self.assertEqual(self.diagram.relationships[0].relationship_type, "implementation")
        
    def test_to_dict(self):
        """Test that the diagram can be converted to a dictionary."""
        test_class = Class("TestClass")
        self.diagram.add_class(test_class)
        
        # Convert to dictionary
        diagram_dict = self.diagram.to_dict()
        
        # Check dictionary contents
        self.assertEqual(diagram_dict["name"], "Test Class Diagram")
        self.assertEqual(len(diagram_dict["elements"]), 1)
        self.assertEqual(diagram_dict["elements"][0]["name"], "TestClass")


if __name__ == "__main__":
    unittest.main() 