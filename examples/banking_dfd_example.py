#!/usr/bin/env python3
"""
Banking System Data Flow Diagram Example

This example creates a Data Flow Diagram (DFD) for a banking system,
showing how data flows between users, processes, and data stores.
"""

import os
import sys
from pathlib import Path

from pydiagrams.diagrams.entity.dfd import (
    DataFlowDiagram,
    Process,
    DataStore,
    ExternalEntity,
    TrustBoundary,
    DataFlow,
    ElementType,
    FlowType
)
from pydiagrams.renderers.dfd_renderer import render_dfd


def create_banking_dfd():
    """
    Create a Data Flow Diagram for a banking system.
    
    This function creates a DFD showing the data flows in a banking application
    including authentication, transaction processing, and reporting components.
    
    Returns:
        DataFlowDiagram: The created banking system DFD
    """
    # Create the main diagram
    dfd = DataFlowDiagram(
        name="Banking System Data Flow",
        description="Data Flow Diagram for a Banking System",
        level=0  # Context level diagram
    )
    
    # Create external entities (users and external systems)
    customer = dfd.create_external_entity(
        name="Customer",
        description="Bank customer using the online banking system",
        entity_number="E1"
    )
    
    bank_staff = dfd.create_external_entity(
        name="Bank Staff",
        description="Bank employees that manage the system",
        entity_number="E2"
    )
    
    payment_gateway = dfd.create_external_entity(
        name="Payment Gateway",
        description="External payment processing service",
        entity_number="E3"
    )
    
    email_service = dfd.create_external_entity(
        name="Email Service",
        description="Email notification service",
        entity_number="E4"
    )
    
    # Create processes
    auth_process = dfd.create_process(
        name="Authentication",
        description="Verifies user identity and manages sessions",
        process_number="1.0"
    )
    
    account_mgmt = dfd.create_process(
        name="Account Management",
        description="Handles account creation, updates and queries",
        process_number="2.0"
    )
    
    transaction_process = dfd.create_process(
        name="Transaction Processing",
        description="Processes financial transactions",
        process_number="3.0"
    )
    
    reporting = dfd.create_process(
        name="Reporting",
        description="Generates reports and statements",
        process_number="4.0"
    )
    
    notification = dfd.create_process(
        name="Notification Service",
        description="Sends notifications to users",
        process_number="5.0"
    )
    
    # Create data stores
    user_db = dfd.create_data_store(
        name="User Database",
        description="Stores user credentials and profile information",
        store_number="D1"
    )
    
    account_db = dfd.create_data_store(
        name="Account Database",
        description="Stores account information and balances",
        store_number="D2"
    )
    
    transaction_db = dfd.create_data_store(
        name="Transaction Database",
        description="Stores transaction records",
        store_number="D3"
    )
    
    session_store = dfd.create_data_store(
        name="Session Store",
        description="Stores active user sessions",
        store_number="D4"
    )
    
    audit_log = dfd.create_data_store(
        name="Audit Log",
        description="Records system activities for security and compliance",
        store_number="D5"
    )
    
    # Create trust boundaries
    secure_zone = dfd.create_trust_boundary(
        name="Secure Banking Zone",
        description="High security zone for financial data",
        element_ids=[
            account_mgmt.id,
            transaction_process.id,
            account_db.id,
            transaction_db.id
        ]
    )
    
    user_facing_zone = dfd.create_trust_boundary(
        name="User-Facing Zone",
        description="Zone that interacts with external users",
        element_ids=[
            auth_process.id,
            reporting.id,
            notification.id,
            session_store.id
        ]
    )
    
    # Create data flows
    
    # Authentication flows
    dfd.create_data_flow(
        source_id=customer.id,
        target_id=auth_process.id,
        name="Login Request",
        data_items=["username", "password"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=auth_process.id,
        target_id=customer.id,
        name="Auth Response",
        data_items=["session_token", "status"],
        flow_type=FlowType.RESPONSE
    )
    
    dfd.create_data_flow(
        source_id=auth_process.id,
        target_id=user_db.id,
        name="Verify Credentials",
        data_items=["username", "password_hash"],
        flow_type=FlowType.BIDIRECTIONAL
    )
    
    dfd.create_data_flow(
        source_id=auth_process.id,
        target_id=session_store.id,
        name="Store Session",
        data_items=["session_id", "user_id", "expiry"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=auth_process.id,
        target_id=audit_log.id,
        name="Log Auth Event",
        data_items=["timestamp", "user_id", "event_type", "ip_address"],
        flow_type=FlowType.DATA
    )
    
    # Account management flows
    dfd.create_data_flow(
        source_id=customer.id,
        target_id=account_mgmt.id,
        name="Account Request",
        data_items=["action", "account_details"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=account_mgmt.id,
        target_id=customer.id,
        name="Account Response",
        data_items=["status", "account_info"],
        flow_type=FlowType.RESPONSE
    )
    
    dfd.create_data_flow(
        source_id=account_mgmt.id,
        target_id=account_db.id,
        name="Manage Accounts",
        data_items=["account_id", "customer_id", "balance", "status"],
        flow_type=FlowType.BIDIRECTIONAL
    )
    
    dfd.create_data_flow(
        source_id=account_mgmt.id,
        target_id=user_db.id,
        name="Get User Info",
        data_items=["user_id", "profile_info"],
        flow_type=FlowType.BIDIRECTIONAL
    )
    
    # Transaction flows
    dfd.create_data_flow(
        source_id=customer.id,
        target_id=transaction_process.id,
        name="Transaction Request",
        data_items=["transaction_type", "amount", "account_id", "recipient"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=customer.id,
        name="Transaction Result",
        data_items=["status", "confirmation_id"],
        flow_type=FlowType.RESPONSE
    )
    
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=account_db.id,
        name="Update Balance",
        data_items=["account_id", "new_balance"],
        flow_type=FlowType.BIDIRECTIONAL
    )
    
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=transaction_db.id,
        name="Store Transaction",
        data_items=["transaction_id", "details", "timestamp"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=payment_gateway.id,
        name="External Payment",
        data_items=["payment_details", "auth_token"],
        flow_type=FlowType.BIDIRECTIONAL
    )
    
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=notification.id,
        name="Transaction Alert",
        data_items=["user_id", "message", "channel"],
        flow_type=FlowType.DATA
    )
    
    # Reporting flows
    dfd.create_data_flow(
        source_id=customer.id,
        target_id=reporting.id,
        name="Report Request",
        data_items=["report_type", "time_period", "format"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=reporting.id,
        target_id=customer.id,
        name="Report Data",
        data_items=["report_content"],
        flow_type=FlowType.RESPONSE
    )
    
    dfd.create_data_flow(
        source_id=reporting.id,
        target_id=transaction_db.id,
        name="Get Transactions",
        data_items=["user_id", "time_period", "filters"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=reporting.id,
        target_id=account_db.id,
        name="Get Account Info",
        data_items=["account_id"],
        flow_type=FlowType.DATA
    )
    
    # Bank staff flows
    dfd.create_data_flow(
        source_id=bank_staff.id,
        target_id=auth_process.id,
        name="Staff Login",
        data_items=["staff_id", "password", "mfa_code"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=bank_staff.id,
        target_id=reporting.id,
        name="Admin Report Request",
        data_items=["report_type", "parameters"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=bank_staff.id,
        target_id=account_mgmt.id,
        name="Admin Actions",
        data_items=["action_type", "customer_id"],
        flow_type=FlowType.DATA
    )
    
    # Notification flows
    dfd.create_data_flow(
        source_id=notification.id,
        target_id=customer.id,
        name="Customer Notification",
        data_items=["notification_content"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=notification.id,
        target_id=email_service.id,
        name="Send Email",
        data_items=["recipient", "subject", "body"],
        flow_type=FlowType.DATA
    )
    
    # Audit logging
    dfd.create_data_flow(
        source_id=transaction_process.id,
        target_id=audit_log.id,
        name="Transaction Audit",
        data_items=["timestamp", "user_id", "action", "status"],
        flow_type=FlowType.DATA
    )
    
    dfd.create_data_flow(
        source_id=account_mgmt.id,
        target_id=audit_log.id,
        name="Account Audit",
        data_items=["timestamp", "user_id", "action", "status"],
        flow_type=FlowType.DATA
    )
    
    return dfd


def main():
    """Run the example."""
    # Create the diagram
    dfd = create_banking_dfd()
    
    # Define the output directory and ensure it exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Define the output file path
    output_path = str(output_dir / "banking_system_dfd.svg")
    
    # Render the diagram
    rendered_path = render_dfd(dfd, output_path)
    print(f"Data Flow Diagram rendered to: {rendered_path}")


if __name__ == "__main__":
    main() 