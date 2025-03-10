"""
Tests for the Entity Relationship Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams.diagrams.entity.erd import (
    EntityRelationshipDiagram, 
    Entity,
    Attribute,
    EntityRelationship,
    AttributeType,
    RelationshipType,
    Cardinality
)


class TestEntityRelationshipDiagram(unittest.TestCase):
    """Test cases for the EntityRelationshipDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = EntityRelationshipDiagram(
            name="Test ERD",
            description="Test Entity Relationship Diagram",
            notation="chen"
        )
    
    def test_entity_creation(self):
        """Test that an entity can be created and added to the diagram."""
        entity = self.diagram.create_entity(
            name="TestEntity",
            description="Test entity description",
            is_weak=False
        )
        
        # Check that the entity was added to the diagram
        self.assertEqual(len(self.diagram.entities), 1)
        self.assertIsInstance(self.diagram.entities[0], Entity)
        self.assertEqual(self.diagram.entities[0].name, "TestEntity")
        self.assertEqual(self.diagram.entities[0].description, "Test entity description")
        self.assertFalse(self.diagram.entities[0].is_weak)
    
    def test_weak_entity_creation(self):
        """Test that a weak entity can be created."""
        weak_entity = self.diagram.create_entity(
            name="WeakEntity",
            description="Weak entity description",
            is_weak=True
        )
        
        # Check that the weak entity was created properly
        self.assertEqual(len(self.diagram.entities), 1)
        self.assertTrue(self.diagram.entities[0].is_weak)
    
    def test_attribute_creation(self):
        """Test that attributes can be added to entities."""
        entity = self.diagram.create_entity(name="TestEntity")
        
        # Add a primary key attribute
        pk_attr = entity.create_attribute(
            name="id",
            description="Primary key",
            attribute_type=AttributeType.NUMBER,
            data_type="INTEGER",
            is_primary_key=True,
            is_nullable=False
        )
        
        # Add a regular attribute
        attr = entity.create_attribute(
            name="name",
            description="Entity name",
            attribute_type=AttributeType.TEXT,
            data_type="VARCHAR",
            length=100,
            is_nullable=False
        )
        
        # Check that the attributes were added
        self.assertEqual(len(entity.attributes), 2)
        self.assertEqual(entity.attributes[0].name, "id")
        self.assertEqual(entity.attributes[1].name, "name")
        self.assertTrue(entity.attributes[0].is_primary_key)
        self.assertFalse(entity.attributes[1].is_primary_key)
        self.assertEqual(entity.attributes[1].attribute_type, AttributeType.TEXT)
        self.assertEqual(entity.attributes[1].length, 100)
    
    def test_get_primary_keys(self):
        """Test that primary keys can be retrieved from an entity."""
        entity = self.diagram.create_entity(name="TestEntity")
        
        # Add a primary key
        pk = entity.create_attribute(
            name="id",
            attribute_type=AttributeType.NUMBER,
            is_primary_key=True
        )
        
        # Add a non-primary key
        non_pk = entity.create_attribute(
            name="name",
            attribute_type=AttributeType.TEXT
        )
        
        # Check that get_primary_keys returns only the primary key
        primary_keys = entity.get_primary_keys()
        self.assertEqual(len(primary_keys), 1)
        self.assertEqual(primary_keys[0].name, "id")
    
    def test_get_foreign_keys(self):
        """Test that foreign keys can be retrieved from an entity."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        
        # Add a primary key to entity1
        pk = entity1.create_attribute(
            name="id",
            attribute_type=AttributeType.NUMBER,
            is_primary_key=True
        )
        
        # Add a foreign key to entity2 referencing entity1
        fk = entity2.create_attribute(
            name="entity1_id",
            attribute_type=AttributeType.NUMBER,
            is_foreign_key=True,
            reference_entity_id=entity1.id,
            reference_attribute_id=pk.id
        )
        
        # Check that get_foreign_keys returns only the foreign key
        foreign_keys = entity2.get_foreign_keys()
        self.assertEqual(len(foreign_keys), 1)
        self.assertEqual(foreign_keys[0].name, "entity1_id")
        self.assertEqual(foreign_keys[0].reference_entity_id, entity1.id)
    
    def test_relationship_creation(self):
        """Test that relationships can be created between entities."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        
        # Create a one-to-many relationship
        relationship = self.diagram.create_relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            name="HasMany",
            description="Entity1 has many Entity2",
            relationship_type=RelationshipType.ONE_TO_MANY,
            source_cardinality=Cardinality.EXACTLY_ONE,
            target_cardinality=Cardinality.ZERO_OR_MANY
        )
        
        # Check that the relationship was created correctly
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertEqual(self.diagram.relationships[0].name, "HasMany")
        self.assertEqual(self.diagram.relationships[0].source_entity_id, entity1.id)
        self.assertEqual(self.diagram.relationships[0].target_entity_id, entity2.id)
        self.assertEqual(self.diagram.relationships[0].relationship_type, RelationshipType.ONE_TO_MANY)
        self.assertEqual(self.diagram.relationships[0].source_cardinality, Cardinality.EXACTLY_ONE)
        self.assertEqual(self.diagram.relationships[0].target_cardinality, Cardinality.ZERO_OR_MANY)
    
    def test_identifying_relationship_creation(self):
        """Test that identifying relationships for weak entities can be created."""
        strong_entity = self.diagram.create_entity(name="StrongEntity")
        weak_entity = self.diagram.create_entity(name="WeakEntity", is_weak=True)
        
        # Create an identifying relationship
        relationship = self.diagram.create_relationship(
            source_entity_id=strong_entity.id,
            target_entity_id=weak_entity.id,
            name="Identifies",
            relationship_type=RelationshipType.ONE_TO_MANY,
            identifying=True
        )
        
        # Check that the relationship was created correctly
        self.assertEqual(len(self.diagram.relationships), 1)
        self.assertTrue(self.diagram.relationships[0].identifying)
    
    def test_find_entity_by_id(self):
        """Test that an entity can be found by its ID."""
        entity = self.diagram.create_entity(name="TestEntity")
        
        # Find the entity by ID
        found_entity = self.diagram.find_entity_by_id(entity.id)
        
        # Check that the correct entity was found
        self.assertIsNotNone(found_entity)
        self.assertEqual(found_entity.name, "TestEntity")
    
    def test_find_entity_by_name(self):
        """Test that an entity can be found by its name."""
        self.diagram.create_entity(name="Entity1")
        self.diagram.create_entity(name="Entity2")
        
        # Find the entity by name
        found_entity = self.diagram.find_entity_by_name("Entity2")
        
        # Check that the correct entity was found
        self.assertIsNotNone(found_entity)
        self.assertEqual(found_entity.id, self.diagram.entities[1].id)
    
    def test_find_relationship_by_id(self):
        """Test that a relationship can be found by its ID."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        relationship = self.diagram.create_relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            name="TestRelationship"
        )
        
        # Find the relationship by ID
        found_relationship = self.diagram.find_relationship_by_id(relationship.id)
        
        # Check that the correct relationship was found
        self.assertIsNotNone(found_relationship)
        self.assertEqual(found_relationship.name, "TestRelationship")
    
    def test_get_relationships_for_entity(self):
        """Test that relationships involving a specific entity can be retrieved."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        entity3 = self.diagram.create_entity(name="Entity3")
        
        # Create relationships involving entity1
        rel1 = self.diagram.create_relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            name="Rel1"
        )
        rel2 = self.diagram.create_relationship(
            source_entity_id=entity3.id,
            target_entity_id=entity1.id,
            name="Rel2"
        )
        
        # Create a relationship not involving entity1
        rel3 = self.diagram.create_relationship(
            source_entity_id=entity2.id,
            target_entity_id=entity3.id,
            name="Rel3"
        )
        
        # Get relationships for entity1
        relationships = self.diagram.get_relationships_for_entity(entity1.id)
        
        # Check that only relationships involving entity1 were retrieved
        self.assertEqual(len(relationships), 2)
        relationship_names = [r.name for r in relationships]
        self.assertIn("Rel1", relationship_names)
        self.assertIn("Rel2", relationship_names)
        self.assertNotIn("Rel3", relationship_names)
    
    def test_custom_cardinality(self):
        """Test that custom cardinality can be used in relationships."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        
        # Create a relationship with custom cardinality
        relationship = self.diagram.create_relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            name="CustomCard",
            source_cardinality=Cardinality.CUSTOM,
            target_cardinality=Cardinality.CUSTOM,
            custom_source_cardinality="2..5",
            custom_target_cardinality="3..7"
        )
        
        # Check that the custom cardinality was set correctly
        self.assertEqual(relationship.source_cardinality, Cardinality.CUSTOM)
        self.assertEqual(relationship.target_cardinality, Cardinality.CUSTOM)
        self.assertEqual(relationship.custom_source_cardinality, "2..5")
        self.assertEqual(relationship.custom_target_cardinality, "3..7")
    
    def test_role_names(self):
        """Test that role names can be set on relationships."""
        entity1 = self.diagram.create_entity(name="Entity1")
        entity2 = self.diagram.create_entity(name="Entity2")
        
        # Create a relationship with role names
        relationship = self.diagram.create_relationship(
            source_entity_id=entity1.id,
            target_entity_id=entity2.id,
            name="HasRoles",
            source_role="parent",
            target_role="child"
        )
        
        # Check that the role names were set correctly
        self.assertEqual(relationship.source_role, "parent")
        self.assertEqual(relationship.target_role, "child")


if __name__ == "__main__":
    unittest.main() 