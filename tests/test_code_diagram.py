"""
Tests for the Code Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams.diagrams.code import (
    CodeDiagram,
    Module,
    Class,
    Interface,
    Function,
    Variable,
    Enum,
    CodeRelationship,
    CodeElementType,
    RelationshipType,
    AccessModifier
)


class TestCodeDiagram(unittest.TestCase):
    """Test cases for the CodeDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = CodeDiagram(
            name="Test Code Diagram",
            description="Test Code Diagram Description",
            language="Python"
        )
    
    def test_module_creation(self):
        """Test that a module can be created and added to the diagram."""
        module = self.diagram.create_module(
            name="test_module",
            description="Test module description",
            source_file="test_module.py",
            imports=["os", "sys"]
        )
        
        # Check that the module was added to the diagram
        self.assertEqual(len(self.diagram.modules), 1)
        self.assertEqual(self.diagram.modules[0].name, "test_module")
        self.assertEqual(self.diagram.modules[0].description, "Test module description")
        self.assertEqual(self.diagram.modules[0].source_file, "test_module.py")
        self.assertEqual(self.diagram.modules[0].imports, ["os", "sys"])
        self.assertEqual(self.diagram.modules[0].element_type, CodeElementType.MODULE)
    
    def test_class_creation(self):
        """Test that a class can be created and added to the diagram."""
        class_obj = self.diagram.create_class(
            name="TestClass",
            description="Test class description",
            access_modifier=AccessModifier.PUBLIC,
            is_abstract=True,
            superclasses=["BaseClass"],
            interfaces=["Serializable"]
        )
        
        # Check that the class was added to the diagram
        self.assertEqual(len(self.diagram.classes), 1)
        self.assertEqual(self.diagram.classes[0].name, "TestClass")
        self.assertEqual(self.diagram.classes[0].description, "Test class description")
        self.assertEqual(self.diagram.classes[0].access_modifier, AccessModifier.PUBLIC)
        self.assertTrue(self.diagram.classes[0].is_abstract)
        self.assertEqual(self.diagram.classes[0].superclasses, ["BaseClass"])
        self.assertEqual(self.diagram.classes[0].interfaces, ["Serializable"])
        self.assertEqual(self.diagram.classes[0].element_type, CodeElementType.CLASS)
    
    def test_interface_creation(self):
        """Test that an interface can be created and added to the diagram."""
        interface = self.diagram.create_interface(
            name="TestInterface",
            description="Test interface description",
            access_modifier=AccessModifier.PUBLIC,
            superinterfaces=["BaseInterface"]
        )
        
        # Check that the interface was added to the diagram
        self.assertEqual(len(self.diagram.interfaces), 1)
        self.assertEqual(self.diagram.interfaces[0].name, "TestInterface")
        self.assertEqual(self.diagram.interfaces[0].description, "Test interface description")
        self.assertEqual(self.diagram.interfaces[0].access_modifier, AccessModifier.PUBLIC)
        self.assertEqual(self.diagram.interfaces[0].superinterfaces, ["BaseInterface"])
        self.assertEqual(self.diagram.interfaces[0].element_type, CodeElementType.INTERFACE)
        self.assertTrue(self.diagram.interfaces[0].is_abstract)  # Interfaces are always abstract
    
    def test_function_creation(self):
        """Test that a function can be created and added to the diagram."""
        function = self.diagram.create_function(
            name="test_function",
            description="Test function description",
            parameters=[("param1", "str"), ("param2", "int")],
            return_type="bool",
            is_static=True
        )
        
        # Check that the function was added to the diagram
        self.assertEqual(len(self.diagram.functions), 1)
        self.assertEqual(self.diagram.functions[0].name, "test_function")
        self.assertEqual(self.diagram.functions[0].description, "Test function description")
        self.assertEqual(self.diagram.functions[0].parameters, [("param1", "str"), ("param2", "int")])
        self.assertEqual(self.diagram.functions[0].return_type, "bool")
        self.assertTrue(self.diagram.functions[0].is_static)
        self.assertEqual(self.diagram.functions[0].element_type, CodeElementType.FUNCTION)
    
    def test_variable_creation(self):
        """Test that a variable can be created and added to the diagram."""
        variable = self.diagram.create_variable(
            name="test_variable",
            description="Test variable description",
            var_type="int",
            initial_value="42",
            is_constant=True
        )
        
        # Check that the variable was added to the diagram
        self.assertEqual(len(self.diagram.variables), 1)
        self.assertEqual(self.diagram.variables[0].name, "test_variable")
        self.assertEqual(self.diagram.variables[0].description, "Test variable description")
        self.assertEqual(self.diagram.variables[0].var_type, "int")
        self.assertEqual(self.diagram.variables[0].initial_value, "42")
        self.assertTrue(self.diagram.variables[0].is_constant)
        self.assertEqual(self.diagram.variables[0].element_type, CodeElementType.VARIABLE)
    
    def test_enum_creation(self):
        """Test that an enum can be created and added to the diagram."""
        enum = self.diagram.create_enum(
            name="TestEnum",
            description="Test enum description",
            values=["VALUE1", "VALUE2", "VALUE3"]
        )
        
        # Check that the enum was added to the diagram
        self.assertEqual(len(self.diagram.enums), 1)
        self.assertEqual(self.diagram.enums[0].name, "TestEnum")
        self.assertEqual(self.diagram.enums[0].description, "Test enum description")
        self.assertEqual(self.diagram.enums[0].values, ["VALUE1", "VALUE2", "VALUE3"])
        self.assertEqual(self.diagram.enums[0].element_type, CodeElementType.ENUM)
    
    def test_relationship_creation(self):
        """Test that relationships can be created between elements."""
        class1 = self.diagram.create_class(name="Class1")
        class2 = self.diagram.create_class(name="Class2")
        
        # Create an inheritance relationship
        relationship = self.diagram.create_relationship(
            source_id=class2.id,
            target_id=class1.id,
            name="Inheritance",
            relationship_type=RelationshipType.INHERITANCE
        )
        
        # Check that the relationship was added to the diagram
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertEqual(self.diagram.relationships[0].name, "Inheritance")
        self.assertEqual(self.diagram.relationships[0].source_id, class2.id)
        self.assertEqual(self.diagram.relationships[0].target_id, class1.id)
        self.assertEqual(self.diagram.relationships[0].relationship_type, RelationshipType.INHERITANCE)
    
    def test_module_with_classes(self):
        """Test that classes can be added as children of a module."""
        module = self.diagram.create_module(name="test_module")
        class1 = self.diagram.create_class(name="Class1")
        class2 = self.diagram.create_class(name="Class2")
        
        # Add classes as children of the module
        module.add_child(class1)
        module.add_child(class2)
        
        # Check that the classes were added as children of the module
        self.assertEqual(len(module.children), 2)
        self.assertIn(class1, module.children)
        self.assertIn(class2, module.children)
    
    def test_class_with_members(self):
        """Test that methods and attributes can be added as children of a class."""
        class_obj = self.diagram.create_class(name="TestClass")
        method1 = self.diagram.create_function(name="method1", return_type="void")
        method2 = self.diagram.create_function(name="method2", return_type="int")
        attribute1 = self.diagram.create_variable(name="attribute1", var_type="string")
        attribute2 = self.diagram.create_variable(name="attribute2", var_type="boolean")
        
        # Add methods and attributes as children of the class
        class_obj.add_child(method1)
        class_obj.add_child(method2)
        class_obj.add_child(attribute1)
        class_obj.add_child(attribute2)
        
        # Check that the methods and attributes were added as children of the class
        self.assertEqual(len(class_obj.children), 4)
        self.assertIn(method1, class_obj.children)
        self.assertIn(method2, class_obj.children)
        self.assertIn(attribute1, class_obj.children)
        self.assertIn(attribute2, class_obj.children)
    
    def test_find_element_by_id(self):
        """Test that an element can be found by its ID."""
        class_obj = self.diagram.create_class(name="TestClass")
        
        # Find the class by ID
        found_element = self.diagram.find_element_by_id(class_obj.id)
        
        # Check that the correct element was found
        self.assertIsNotNone(found_element)
        self.assertEqual(found_element.name, "TestClass")
        self.assertEqual(found_element.element_type, CodeElementType.CLASS)
    
    def test_find_element_by_name(self):
        """Test that an element can be found by its name."""
        self.diagram.create_class(name="Class1")
        self.diagram.create_class(name="Class2")
        
        # Find the class by name
        found_element = self.diagram.find_element_by_name("Class2", CodeElementType.CLASS)
        
        # Check that the correct element was found
        self.assertIsNotNone(found_element)
        self.assertEqual(found_element.name, "Class2")
        self.assertEqual(found_element.element_type, CodeElementType.CLASS)
    
    def test_find_element_by_name_no_type(self):
        """Test that an element can be found by its name without specifying a type."""
        self.diagram.create_class(name="TestClass")
        self.diagram.create_function(name="TestFunction")
        
        # Find elements by name without specifying a type
        found_class = self.diagram.find_element_by_name("TestClass")
        found_function = self.diagram.find_element_by_name("TestFunction")
        
        # Check that the correct elements were found
        self.assertIsNotNone(found_class)
        self.assertEqual(found_class.name, "TestClass")
        self.assertEqual(found_class.element_type, CodeElementType.CLASS)
        
        self.assertIsNotNone(found_function)
        self.assertEqual(found_function.name, "TestFunction")
        self.assertEqual(found_function.element_type, CodeElementType.FUNCTION)
    
    def test_find_relationship_by_id(self):
        """Test that a relationship can be found by its ID."""
        class1 = self.diagram.create_class(name="Class1")
        class2 = self.diagram.create_class(name="Class2")
        relationship = self.diagram.create_relationship(
            source_id=class1.id,
            target_id=class2.id,
            name="TestRelationship"
        )
        
        # Find the relationship by ID
        found_relationship = self.diagram.find_relationship_by_id(relationship.id)
        
        # Check that the correct relationship was found
        self.assertIsNotNone(found_relationship)
        self.assertEqual(found_relationship.name, "TestRelationship")
        self.assertEqual(found_relationship.source_id, class1.id)
        self.assertEqual(found_relationship.target_id, class2.id)
    
    def test_get_relationships_for_element(self):
        """Test that relationships for a specific element can be retrieved."""
        class1 = self.diagram.create_class(name="Class1")
        class2 = self.diagram.create_class(name="Class2")
        class3 = self.diagram.create_class(name="Class3")
        
        # Create relationships involving class1
        rel1 = self.diagram.create_relationship(
            source_id=class1.id,
            target_id=class2.id,
            name="Class1ToClass2"
        )
        rel2 = self.diagram.create_relationship(
            source_id=class3.id,
            target_id=class1.id,
            name="Class3ToClass1"
        )
        
        # Create a relationship not involving class1
        rel3 = self.diagram.create_relationship(
            source_id=class2.id,
            target_id=class3.id,
            name="Class2ToClass3"
        )
        
        # Get relationships for class1
        relationships = self.diagram.get_relationships_for_element(class1.id)
        
        # Check that only relationships involving class1 were retrieved
        self.assertEqual(len(relationships), 2)
        relationship_names = [r.name for r in relationships]
        self.assertIn("Class1ToClass2", relationship_names)
        self.assertIn("Class3ToClass1", relationship_names)
        self.assertNotIn("Class2ToClass3", relationship_names)
    
    def test_add_import_to_module(self):
        """Test that an import can be added to a module."""
        module = self.diagram.create_module(name="test_module")
        
        # Add imports to the module
        module.add_import("os")
        module.add_import("sys")
        
        # Check that the imports were added
        self.assertEqual(len(module.imports), 2)
        self.assertIn("os", module.imports)
        self.assertIn("sys", module.imports)
    
    def test_add_superclass_to_class(self):
        """Test that a superclass can be added to a class."""
        class_obj = self.diagram.create_class(name="TestClass")
        
        # Add superclasses to the class
        class_obj.add_superclass("BaseClass1")
        class_obj.add_superclass("BaseClass2")
        
        # Check that the superclasses were added
        self.assertEqual(len(class_obj.superclasses), 2)
        self.assertIn("BaseClass1", class_obj.superclasses)
        self.assertIn("BaseClass2", class_obj.superclasses)
    
    def test_add_interface_to_class(self):
        """Test that an interface can be added to a class."""
        class_obj = self.diagram.create_class(name="TestClass")
        
        # Add interfaces to the class
        class_obj.add_interface("Interface1")
        class_obj.add_interface("Interface2")
        
        # Check that the interfaces were added
        self.assertEqual(len(class_obj.interfaces), 2)
        self.assertIn("Interface1", class_obj.interfaces)
        self.assertIn("Interface2", class_obj.interfaces)
    
    def test_add_superinterface_to_interface(self):
        """Test that a superinterface can be added to an interface."""
        interface = self.diagram.create_interface(name="TestInterface")
        
        # Add superinterfaces to the interface
        interface.add_superinterface("BaseInterface1")
        interface.add_superinterface("BaseInterface2")
        
        # Check that the superinterfaces were added
        self.assertEqual(len(interface.superinterfaces), 2)
        self.assertIn("BaseInterface1", interface.superinterfaces)
        self.assertIn("BaseInterface2", interface.superinterfaces)
    
    def test_add_parameter_to_function(self):
        """Test that a parameter can be added to a function."""
        function = self.diagram.create_function(name="test_function")
        
        # Add parameters to the function
        function.add_parameter("param1", "int")
        function.add_parameter("param2", "string")
        
        # Check that the parameters were added
        self.assertEqual(len(function.parameters), 2)
        self.assertIn(("param1", "int"), function.parameters)
        self.assertIn(("param2", "string"), function.parameters)
    
    def test_add_value_to_enum(self):
        """Test that a value can be added to an enum."""
        enum = self.diagram.create_enum(name="TestEnum")
        
        # Add values to the enum
        enum.add_value("VALUE1")
        enum.add_value("VALUE2")
        
        # Check that the values were added
        self.assertEqual(len(enum.values), 2)
        self.assertIn("VALUE1", enum.values)
        self.assertIn("VALUE2", enum.values)


if __name__ == "__main__":
    unittest.main() 