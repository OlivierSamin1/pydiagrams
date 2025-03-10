#!/usr/bin/env python3
"""
E-commerce System Entity Relationship Diagram Example

This example creates an Entity Relationship Diagram (ERD) for an e-commerce system,
showing entities like customers, products, orders, and their relationships.
"""

import os
import sys
from pathlib import Path

from pydiagrams.diagrams.entity.erd import (
    EntityRelationshipDiagram,
    Entity,
    Attribute,
    EntityRelationship,
    AttributeType,
    RelationshipType,
    Cardinality
)
from pydiagrams.renderers.erd_renderer import render_erd


def create_ecommerce_erd():
    """
    Create an Entity Relationship Diagram for an e-commerce system.
    
    This function creates an ERD showing the database schema for an e-commerce 
    application with customers, products, orders, and related entities.
    
    Returns:
        EntityRelationshipDiagram: The created e-commerce system ERD
    """
    # Create the main diagram
    erd = EntityRelationshipDiagram(
        name="E-commerce System Entity Relationship Diagram",
        description="Database schema for an e-commerce system",
        notation="chen"  # Use Chen notation
    )
    
    # Create entities
    
    # Customer entity
    customer = erd.create_entity(
        name="Customer",
        description="Registered users who can place orders"
    )
    
    customer.create_attribute(
        name="customer_id",
        description="Unique identifier for the customer",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    customer.create_attribute(
        name="email",
        description="Customer's email address",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=255,
        is_nullable=False,
        is_unique=True
    )
    
    customer.create_attribute(
        name="first_name",
        description="Customer's first name",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    customer.create_attribute(
        name="last_name",
        description="Customer's last name",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    customer.create_attribute(
        name="password_hash",
        description="Hashed password",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=255,
        is_nullable=False
    )
    
    customer.create_attribute(
        name="created_at",
        description="Account creation timestamp",
        attribute_type=AttributeType.DATE,
        data_type="TIMESTAMP",
        is_nullable=False,
        default_value="CURRENT_TIMESTAMP"
    )
    
    customer.create_attribute(
        name="last_login",
        description="Last login timestamp",
        attribute_type=AttributeType.DATE,
        data_type="TIMESTAMP",
        is_nullable=True
    )
    
    # Address entity
    address = erd.create_entity(
        name="Address",
        description="Customer shipping and billing addresses"
    )
    
    address.create_attribute(
        name="address_id",
        description="Unique identifier for the address",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    address.create_attribute(
        name="customer_id",
        description="Reference to the customer",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=customer.id,
        reference_attribute_id=customer.get_primary_keys()[0].id
    )
    
    address.create_attribute(
        name="address_type",
        description="Billing or shipping address",
        attribute_type=AttributeType.ENUM,
        data_type="VARCHAR",
        length=20,
        is_nullable=False,
        constraints=["CHECK (address_type IN ('BILLING', 'SHIPPING'))"]
    )
    
    address.create_attribute(
        name="street_address",
        description="Street address",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=255,
        is_nullable=False
    )
    
    address.create_attribute(
        name="city",
        description="City",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    address.create_attribute(
        name="state",
        description="State or province",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    address.create_attribute(
        name="postal_code",
        description="Postal or ZIP code",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=20,
        is_nullable=False
    )
    
    address.create_attribute(
        name="country",
        description="Country",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    address.create_attribute(
        name="is_default",
        description="Whether this is the default address",
        attribute_type=AttributeType.BOOLEAN,
        data_type="BOOLEAN",
        is_nullable=False,
        default_value="FALSE"
    )
    
    # Product category entity
    category = erd.create_entity(
        name="Category",
        description="Product categories"
    )
    
    category.create_attribute(
        name="category_id",
        description="Unique identifier for the category",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    category.create_attribute(
        name="parent_category_id",
        description="Reference to parent category (for hierarchical categories)",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=True,
        reference_entity_id=category.id,
        reference_attribute_id=category.get_primary_keys()[0].id
    )
    
    category.create_attribute(
        name="name",
        description="Category name",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=False
    )
    
    category.create_attribute(
        name="description",
        description="Category description",
        attribute_type=AttributeType.TEXT,
        data_type="TEXT",
        is_nullable=True
    )
    
    # Product entity
    product = erd.create_entity(
        name="Product",
        description="Products available for purchase"
    )
    
    product.create_attribute(
        name="product_id",
        description="Unique identifier for the product",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    product.create_attribute(
        name="category_id",
        description="Reference to the product category",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=category.id,
        reference_attribute_id=category.get_primary_keys()[0].id
    )
    
    product.create_attribute(
        name="name",
        description="Product name",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=255,
        is_nullable=False
    )
    
    product.create_attribute(
        name="description",
        description="Product description",
        attribute_type=AttributeType.TEXT,
        data_type="TEXT",
        is_nullable=True
    )
    
    product.create_attribute(
        name="sku",
        description="Stock Keeping Unit (SKU)",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=50,
        is_nullable=False,
        is_unique=True
    )
    
    product.create_attribute(
        name="price",
        description="Product price",
        attribute_type=AttributeType.NUMBER,
        data_type="DECIMAL",
        precision=10,
        scale=2,
        is_nullable=False
    )
    
    product.create_attribute(
        name="stock_quantity",
        description="Current inventory quantity",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_nullable=False,
        default_value="0"
    )
    
    product.create_attribute(
        name="is_active",
        description="Whether the product is active",
        attribute_type=AttributeType.BOOLEAN,
        data_type="BOOLEAN",
        is_nullable=False,
        default_value="TRUE"
    )
    
    product.create_attribute(
        name="created_at",
        description="Product creation timestamp",
        attribute_type=AttributeType.DATE,
        data_type="TIMESTAMP",
        is_nullable=False,
        default_value="CURRENT_TIMESTAMP"
    )
    
    # Order entity
    order = erd.create_entity(
        name="Order",
        description="Customer orders"
    )
    
    order.create_attribute(
        name="order_id",
        description="Unique identifier for the order",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    order.create_attribute(
        name="customer_id",
        description="Reference to the customer",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=customer.id,
        reference_attribute_id=customer.get_primary_keys()[0].id
    )
    
    order.create_attribute(
        name="shipping_address_id",
        description="Reference to the shipping address",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=address.id,
        reference_attribute_id=address.get_primary_keys()[0].id
    )
    
    order.create_attribute(
        name="billing_address_id",
        description="Reference to the billing address",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=address.id,
        reference_attribute_id=address.get_primary_keys()[0].id
    )
    
    order.create_attribute(
        name="order_date",
        description="Date and time when the order was placed",
        attribute_type=AttributeType.DATE,
        data_type="TIMESTAMP",
        is_nullable=False,
        default_value="CURRENT_TIMESTAMP"
    )
    
    order.create_attribute(
        name="order_status",
        description="Current status of the order",
        attribute_type=AttributeType.ENUM,
        data_type="VARCHAR",
        length=20,
        is_nullable=False,
        constraints=["CHECK (order_status IN ('PENDING', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED'))"]
    )
    
    order.create_attribute(
        name="total_amount",
        description="Total order amount",
        attribute_type=AttributeType.NUMBER,
        data_type="DECIMAL",
        precision=10,
        scale=2,
        is_nullable=False
    )
    
    order.create_attribute(
        name="payment_method",
        description="Payment method used",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=50,
        is_nullable=False
    )
    
    # Order Item entity (weak entity)
    order_item = erd.create_entity(
        name="OrderItem",
        description="Items within an order",
        is_weak=True
    )
    
    order_item.create_attribute(
        name="order_id",
        description="Reference to the order",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=order.id,
        reference_attribute_id=order.get_primary_keys()[0].id
    )
    
    order_item.create_attribute(
        name="product_id",
        description="Reference to the product",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=product.id,
        reference_attribute_id=product.get_primary_keys()[0].id
    )
    
    order_item.create_attribute(
        name="quantity",
        description="Quantity of the product ordered",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_nullable=False
    )
    
    order_item.create_attribute(
        name="unit_price",
        description="Price of the product at the time of order",
        attribute_type=AttributeType.NUMBER,
        data_type="DECIMAL",
        precision=10,
        scale=2,
        is_nullable=False
    )
    
    order_item.create_attribute(
        name="subtotal",
        description="Subtotal for this item (quantity * unit_price)",
        attribute_type=AttributeType.NUMBER,
        data_type="DECIMAL",
        precision=10,
        scale=2,
        is_nullable=False
    )
    
    # Payment entity
    payment = erd.create_entity(
        name="Payment",
        description="Order payments"
    )
    
    payment.create_attribute(
        name="payment_id",
        description="Unique identifier for the payment",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_primary_key=True,
        is_nullable=False
    )
    
    payment.create_attribute(
        name="order_id",
        description="Reference to the order",
        attribute_type=AttributeType.NUMBER,
        data_type="INTEGER",
        is_foreign_key=True,
        is_nullable=False,
        reference_entity_id=order.id,
        reference_attribute_id=order.get_primary_keys()[0].id
    )
    
    payment.create_attribute(
        name="payment_date",
        description="Date and time when the payment was made",
        attribute_type=AttributeType.DATE,
        data_type="TIMESTAMP",
        is_nullable=False,
        default_value="CURRENT_TIMESTAMP"
    )
    
    payment.create_attribute(
        name="payment_method",
        description="Payment method used",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=50,
        is_nullable=False
    )
    
    payment.create_attribute(
        name="amount",
        description="Payment amount",
        attribute_type=AttributeType.NUMBER,
        data_type="DECIMAL",
        precision=10,
        scale=2,
        is_nullable=False
    )
    
    payment.create_attribute(
        name="status",
        description="Payment status",
        attribute_type=AttributeType.ENUM,
        data_type="VARCHAR",
        length=20,
        is_nullable=False,
        constraints=["CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED'))"]
    )
    
    payment.create_attribute(
        name="transaction_id",
        description="External payment processor transaction ID",
        attribute_type=AttributeType.TEXT,
        data_type="VARCHAR",
        length=100,
        is_nullable=True
    )
    
    # Create relationships
    
    # Customer to Address relationship
    erd.create_relationship(
        source_entity_id=customer.id,
        target_entity_id=address.id,
        name="Has",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY
    )
    
    # Customer to Order relationship
    erd.create_relationship(
        source_entity_id=customer.id,
        target_entity_id=order.id,
        name="Places",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY
    )
    
    # Category to Product relationship
    erd.create_relationship(
        source_entity_id=category.id,
        target_entity_id=product.id,
        name="Contains",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY
    )
    
    # Category self-relationship (for hierarchical categories)
    erd.create_relationship(
        source_entity_id=category.id,
        target_entity_id=category.id,
        name="HasParent",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.ZERO_OR_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY,
        source_role="Parent",
        target_role="Child"
    )
    
    # Order to OrderItem relationship (identifying relationship)
    erd.create_relationship(
        source_entity_id=order.id,
        target_entity_id=order_item.id,
        name="Contains",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ONE_OR_MANY,
        identifying=True
    )
    
    # Product to OrderItem relationship
    erd.create_relationship(
        source_entity_id=product.id,
        target_entity_id=order_item.id,
        name="IncludedIn",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY,
        identifying=True
    )
    
    # Order to Payment relationship
    erd.create_relationship(
        source_entity_id=order.id,
        target_entity_id=payment.id,
        name="Pays",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY
    )
    
    # Address to Order relationships
    erd.create_relationship(
        source_entity_id=address.id,
        target_entity_id=order.id,
        name="ShipsTo",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY,
        source_role="ShippingAddress"
    )
    
    erd.create_relationship(
        source_entity_id=address.id,
        target_entity_id=order.id,
        name="BillsTo",
        relationship_type=RelationshipType.ONE_TO_MANY,
        source_cardinality=Cardinality.EXACTLY_ONE,
        target_cardinality=Cardinality.ZERO_OR_MANY,
        source_role="BillingAddress"
    )
    
    return erd


def main():
    """Run the example."""
    # Create the diagram
    erd = create_ecommerce_erd()
    
    # Define the output directory and ensure it exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Define the output file path
    output_path = str(output_dir / "ecommerce_erd.svg")
    
    # Render the diagram
    rendered_path = render_erd(erd, output_path)
    print(f"Entity Relationship Diagram rendered to: {rendered_path}")


if __name__ == "__main__":
    main() 