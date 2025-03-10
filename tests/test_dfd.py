"""
Tests for the Data Flow Diagram implementation.
"""

import os
import sys
import unittest

# Add the parent directory to the sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pydiagrams.diagrams.entity.dfd import (
    DataFlowDiagram,
    Process,
    DataStore,
    ExternalEntity,
    TrustBoundary,
    DataFlow,
    ElementType,
    FlowType,
    DFDElement
)


class TestDataFlowDiagram(unittest.TestCase):
    """Test cases for the DataFlowDiagram class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.diagram = DataFlowDiagram(
            name="Test DFD",
            description="Test Data Flow Diagram",
            level=0  # Context level diagram
        )
    
    def test_process_creation(self):
        """Test that a process can be created and added to the diagram."""
        process = self.diagram.create_process(
            name="Test Process",
            description="Test process description",
            process_number="1.0"
        )
        
        # Check that the process was added to the diagram
        self.assertEqual(len(self.diagram.processes), 1)
        self.assertIsInstance(self.diagram.processes[0], Process)
        self.assertEqual(self.diagram.processes[0].name, "Test Process")
        self.assertEqual(self.diagram.processes[0].description, "Test process description")
        self.assertEqual(self.diagram.processes[0].process_number, "1.0")
        self.assertEqual(self.diagram.processes[0].element_type, ElementType.PROCESS)
    
    def test_data_store_creation(self):
        """Test that a data store can be created and added to the diagram."""
        data_store = self.diagram.create_data_store(
            name="Test Data Store",
            description="Test data store description",
            store_number="D1"
        )
        
        # Check that the data store was added to the diagram
        self.assertEqual(len(self.diagram.data_stores), 1)
        self.assertIsInstance(self.diagram.data_stores[0], DataStore)
        self.assertEqual(self.diagram.data_stores[0].name, "Test Data Store")
        self.assertEqual(self.diagram.data_stores[0].description, "Test data store description")
        self.assertEqual(self.diagram.data_stores[0].store_number, "D1")
        self.assertEqual(self.diagram.data_stores[0].element_type, ElementType.DATA_STORE)
    
    def test_external_entity_creation(self):
        """Test that an external entity can be created and added to the diagram."""
        external_entity = self.diagram.create_external_entity(
            name="Test External Entity",
            description="Test external entity description",
            entity_number="E1"
        )
        
        # Check that the external entity was added to the diagram
        self.assertEqual(len(self.diagram.external_entities), 1)
        self.assertIsInstance(self.diagram.external_entities[0], ExternalEntity)
        self.assertEqual(self.diagram.external_entities[0].name, "Test External Entity")
        self.assertEqual(self.diagram.external_entities[0].description, "Test external entity description")
        self.assertEqual(self.diagram.external_entities[0].entity_number, "E1")
        self.assertEqual(self.diagram.external_entities[0].element_type, ElementType.EXTERNAL_ENTITY)
    
    def test_trust_boundary_creation(self):
        """Test that a trust boundary can be created and added to the diagram."""
        # Create some elements to include in the boundary
        process1 = self.diagram.create_process(name="Process1")
        process2 = self.diagram.create_process(name="Process2")
        
        # Create a trust boundary containing the processes
        trust_boundary = self.diagram.create_trust_boundary(
            name="Secure Zone",
            description="Secure processing zone",
            element_ids=[process1.id, process2.id]
        )
        
        # Check that the trust boundary was added to the diagram
        self.assertEqual(len(self.diagram.trust_boundaries), 1)
        self.assertIsInstance(self.diagram.trust_boundaries[0], TrustBoundary)
        self.assertEqual(self.diagram.trust_boundaries[0].name, "Secure Zone")
        self.assertEqual(self.diagram.trust_boundaries[0].description, "Secure processing zone")
        self.assertEqual(len(self.diagram.trust_boundaries[0].element_ids), 2)
        self.assertIn(process1.id, self.diagram.trust_boundaries[0].element_ids)
        self.assertIn(process2.id, self.diagram.trust_boundaries[0].element_ids)
        self.assertEqual(self.diagram.trust_boundaries[0].element_type, ElementType.TRUST_BOUNDARY)
    
    def test_add_element_to_trust_boundary(self):
        """Test that elements can be added to an existing trust boundary."""
        # Create a trust boundary
        trust_boundary = self.diagram.create_trust_boundary(name="Secure Zone")
        
        # Create a process
        process = self.diagram.create_process(name="Process")
        
        # Add the process to the trust boundary
        trust_boundary.add_element_id(process.id)
        
        # Check that the process was added to the trust boundary
        self.assertEqual(len(trust_boundary.element_ids), 1)
        self.assertEqual(trust_boundary.element_ids[0], process.id)
    
    def test_data_flow_creation(self):
        """Test that a data flow can be created and added to the diagram."""
        # Create a source and target for the flow
        source = self.diagram.create_external_entity(name="User")
        target = self.diagram.create_process(name="Login Process")
        
        # Create a data flow from source to target
        data_flow = self.diagram.create_data_flow(
            source_id=source.id,
            target_id=target.id,
            name="Login Request",
            description="User sends login credentials",
            flow_type=FlowType.DATA,
            data_items=["username", "password"]
        )
        
        # Check that the data flow was added to the diagram
        self.assertEqual(len(self.diagram.data_flows), 1)
        self.assertIsInstance(self.diagram.data_flows[0], DataFlow)
        self.assertEqual(self.diagram.data_flows[0].name, "Login Request")
        self.assertEqual(self.diagram.data_flows[0].description, "User sends login credentials")
        self.assertEqual(self.diagram.data_flows[0].source_id, source.id)
        self.assertEqual(self.diagram.data_flows[0].target_id, target.id)
        self.assertEqual(self.diagram.data_flows[0].flow_type, FlowType.DATA)
        self.assertEqual(len(self.diagram.data_flows[0].data_items), 2)
        self.assertIn("username", self.diagram.data_flows[0].data_items)
        self.assertIn("password", self.diagram.data_flows[0].data_items)
    
    def test_find_element_by_id(self):
        """Test that elements can be found by their IDs."""
        # Create different element types
        process = self.diagram.create_process(name="Process")
        data_store = self.diagram.create_data_store(name="Data Store")
        external_entity = self.diagram.create_external_entity(name="External Entity")
        trust_boundary = self.diagram.create_trust_boundary(name="Trust Boundary")
        
        # Find each element by ID
        found_process = self.diagram.find_element_by_id(process.id)
        found_data_store = self.diagram.find_element_by_id(data_store.id)
        found_external_entity = self.diagram.find_element_by_id(external_entity.id)
        found_trust_boundary = self.diagram.find_element_by_id(trust_boundary.id)
        
        # Check that the correct elements were found
        self.assertIsNotNone(found_process)
        self.assertIsNotNone(found_data_store)
        self.assertIsNotNone(found_external_entity)
        self.assertIsNotNone(found_trust_boundary)
        
        self.assertEqual(found_process.name, "Process")
        self.assertEqual(found_data_store.name, "Data Store")
        self.assertEqual(found_external_entity.name, "External Entity")
        self.assertEqual(found_trust_boundary.name, "Trust Boundary")
    
    def test_find_element_by_id_not_found(self):
        """Test that find_element_by_id returns None for non-existent ID."""
        # Try to find an element with a non-existent ID
        found_element = self.diagram.find_element_by_id("non_existent_id")
        
        # Check that None was returned
        self.assertIsNone(found_element)
    
    def test_data_flow_with_different_flow_types(self):
        """Test that data flows can have different flow types."""
        # Create elements for the flows
        source = self.diagram.create_process(name="Source Process")
        target = self.diagram.create_process(name="Target Process")
        
        # Create flows with different types
        data_flow = self.diagram.create_data_flow(
            source_id=source.id, 
            target_id=target.id,
            name="Data Flow",
            flow_type=FlowType.DATA
        )
        
        control_flow = self.diagram.create_data_flow(
            source_id=source.id,
            target_id=target.id,
            name="Control Flow",
            flow_type=FlowType.CONTROL
        )
        
        event_flow = self.diagram.create_data_flow(
            source_id=source.id,
            target_id=target.id,
            name="Event Flow",
            flow_type=FlowType.EVENT
        )
        
        response_flow = self.diagram.create_data_flow(
            source_id=source.id,
            target_id=target.id,
            name="Response Flow",
            flow_type=FlowType.RESPONSE
        )
        
        bidirectional_flow = self.diagram.create_data_flow(
            source_id=source.id,
            target_id=target.id,
            name="Bidirectional Flow",
            flow_type=FlowType.BIDIRECTIONAL
        )
        
        # Check that the flows have the correct types
        self.assertEqual(self.diagram.data_flows[0].flow_type, FlowType.DATA)
        self.assertEqual(self.diagram.data_flows[1].flow_type, FlowType.CONTROL)
        self.assertEqual(self.diagram.data_flows[2].flow_type, FlowType.EVENT)
        self.assertEqual(self.diagram.data_flows[3].flow_type, FlowType.RESPONSE)
        self.assertEqual(self.diagram.data_flows[4].flow_type, FlowType.BIDIRECTIONAL)
    
    def test_complex_dfd_creation(self):
        """Test the creation of a more complex DFD with multiple elements and flows."""
        # Create external entities
        user = self.diagram.create_external_entity(name="User", entity_number="E1")
        external_system = self.diagram.create_external_entity(name="External System", entity_number="E2")
        
        # Create processes
        auth_process = self.diagram.create_process(name="Authentication", process_number="1.0")
        business_process = self.diagram.create_process(name="Business Logic", process_number="2.0")
        
        # Create data stores
        user_db = self.diagram.create_data_store(name="User Database", store_number="D1")
        data_db = self.diagram.create_data_store(name="Data Database", store_number="D2")
        
        # Create trust boundaries
        secure_zone = self.diagram.create_trust_boundary(
            name="Secure Zone",
            element_ids=[auth_process.id, business_process.id, user_db.id]
        )
        
        # Create data flows
        # User -> Authentication
        login_flow = self.diagram.create_data_flow(
            source_id=user.id,
            target_id=auth_process.id,
            name="Login",
            data_items=["credentials"]
        )
        
        # Authentication -> User Database
        verify_flow = self.diagram.create_data_flow(
            source_id=auth_process.id,
            target_id=user_db.id,
            name="Verify Credentials"
        )
        
        # Authentication -> User
        auth_response = self.diagram.create_data_flow(
            source_id=auth_process.id,
            target_id=user.id,
            name="Auth Response",
            flow_type=FlowType.RESPONSE
        )
        
        # User -> Business Logic
        request_flow = self.diagram.create_data_flow(
            source_id=user.id,
            target_id=business_process.id,
            name="Request"
        )
        
        # Business Logic -> Data Database
        data_access = self.diagram.create_data_flow(
            source_id=business_process.id,
            target_id=data_db.id,
            name="Data Access",
            flow_type=FlowType.BIDIRECTIONAL
        )
        
        # Business Logic -> External System
        external_flow = self.diagram.create_data_flow(
            source_id=business_process.id,
            target_id=external_system.id,
            name="External Request"
        )
        
        # External System -> Business Logic
        external_response = self.diagram.create_data_flow(
            source_id=external_system.id,
            target_id=business_process.id,
            name="External Response",
            flow_type=FlowType.RESPONSE
        )
        
        # Business Logic -> User
        response_flow = self.diagram.create_data_flow(
            source_id=business_process.id,
            target_id=user.id,
            name="Response",
            flow_type=FlowType.RESPONSE
        )
        
        # Check overall diagram structure
        self.assertEqual(len(self.diagram.external_entities), 2)
        self.assertEqual(len(self.diagram.processes), 2)
        self.assertEqual(len(self.diagram.data_stores), 2)
        self.assertEqual(len(self.diagram.trust_boundaries), 1)
        self.assertEqual(len(self.diagram.data_flows), 8)
        
        # Check that the trust boundary contains the correct elements
        self.assertEqual(len(secure_zone.element_ids), 3)
        self.assertIn(auth_process.id, secure_zone.element_ids)
        self.assertIn(business_process.id, secure_zone.element_ids)
        self.assertIn(user_db.id, secure_zone.element_ids)
        
        # Check the flows between elements
        flows_from_user = [flow for flow in self.diagram.data_flows if flow.source_id == user.id]
        self.assertEqual(len(flows_from_user), 2)  # Login and Request
        
        flows_to_user = [flow for flow in self.diagram.data_flows if flow.target_id == user.id]
        self.assertEqual(len(flows_to_user), 2)  # Auth Response and Response


if __name__ == "__main__":
    unittest.main() 