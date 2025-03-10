#!/usr/bin/env python3
"""
Python Code Diagram Example

This example creates a Code Diagram representing a simple Python application
with modules, classes, functions, and their relationships.
"""

import os
import sys
from pathlib import Path

from pydiagrams.diagrams.code import (
    CodeDiagram, 
    Module, 
    Class, 
    Interface, 
    Function, 
    Variable, 
    Enum,
    CodeElementType,
    RelationshipType,
    AccessModifier
)
from pydiagrams.renderers.code_renderer import render_code_diagram


def create_python_code_diagram():
    """
    Create a code diagram for a simple Python application.
    
    This function creates a diagram showing a Flask-based web application
    with modules, classes, and their relationships.
    
    Returns:
        CodeDiagram: The created code diagram
    """
    # Create the main diagram
    diagram = CodeDiagram(
        name="Python Web Application",
        description="Code structure of a Flask-based web application",
        language="Python"
    )
    
    # Create the main application module
    app_module = diagram.create_module(
        name="app",
        description="Main application module",
        source_file="app.py",
        imports=["flask", "config", "models", "routes"]
    )
    
    # Create the models module
    models_module = diagram.create_module(
        name="models",
        description="Database models",
        source_file="models.py",
        imports=["flask_sqlalchemy", "app"]
    )
    
    # Create the routes module
    routes_module = diagram.create_module(
        name="routes",
        description="Application routes and views",
        source_file="routes.py",
        imports=["flask", "app", "models", "forms"]
    )
    
    # Create the forms module
    forms_module = diagram.create_module(
        name="forms",
        description="Form definitions",
        source_file="forms.py",
        imports=["flask_wtf", "wtforms"]
    )
    
    # Create the config module
    config_module = diagram.create_module(
        name="config",
        description="Application configuration",
        source_file="config.py",
        imports=["os"]
    )
    
    # Create the Flask application class
    flask_app = diagram.create_class(
        name="Flask",
        description="Flask application class",
        source_file="flask/__init__.py"
    )
    
    # Create the SQLAlchemy class
    sqlalchemy = diagram.create_class(
        name="SQLAlchemy",
        description="SQLAlchemy ORM",
        source_file="flask_sqlalchemy/__init__.py"
    )
    
    # Create application classes
    
    # Configuration class
    config_class = diagram.create_class(
        name="Config",
        description="Application configuration class",
        source_file="config.py"
    )
    
    # Add configuration variables
    secret_key = diagram.create_variable(
        name="SECRET_KEY",
        var_type="str",
        initial_value="'your-secret-key'",
        is_constant=True,
        source_file="config.py"
    )
    
    database_uri = diagram.create_variable(
        name="SQLALCHEMY_DATABASE_URI",
        var_type="str",
        initial_value="'sqlite:///app.db'",
        is_constant=True,
        source_file="config.py"
    )
    
    # Add variables to the Config class
    config_class.add_child(secret_key)
    config_class.add_child(database_uri)
    
    # Add Config class to the config module
    config_module.add_child(config_class)
    
    # Create User model class
    user_class = diagram.create_class(
        name="User",
        description="User model class",
        source_file="models.py"
    )
    
    # Add User attributes
    user_id = diagram.create_variable(
        name="id",
        var_type="Integer",
        description="User ID",
        source_file="models.py"
    )
    
    username = diagram.create_variable(
        name="username",
        var_type="String(64)",
        description="Username",
        source_file="models.py"
    )
    
    email = diagram.create_variable(
        name="email",
        var_type="String(120)",
        description="Email address",
        source_file="models.py"
    )
    
    password_hash = diagram.create_variable(
        name="password_hash",
        var_type="String(128)",
        description="Hashed password",
        source_file="models.py"
    )
    
    # Add User methods
    set_password = diagram.create_function(
        name="set_password",
        parameters=[("self", ""), ("password", "str")],
        return_type=None,
        source_file="models.py"
    )
    
    check_password = diagram.create_function(
        name="check_password",
        parameters=[("self", ""), ("password", "str")],
        return_type="bool",
        source_file="models.py"
    )
    
    # Add attributes and methods to User class
    user_class.add_child(user_id)
    user_class.add_child(username)
    user_class.add_child(email)
    user_class.add_child(password_hash)
    user_class.add_child(set_password)
    user_class.add_child(check_password)
    
    # Add User class to the models module
    models_module.add_child(user_class)
    
    # Create Post model class
    post_class = diagram.create_class(
        name="Post",
        description="Post model class",
        source_file="models.py"
    )
    
    # Add Post attributes
    post_id = diagram.create_variable(
        name="id",
        var_type="Integer",
        description="Post ID",
        source_file="models.py"
    )
    
    title = diagram.create_variable(
        name="title",
        var_type="String(100)",
        description="Post title",
        source_file="models.py"
    )
    
    content = diagram.create_variable(
        name="content",
        var_type="Text",
        description="Post content",
        source_file="models.py"
    )
    
    timestamp = diagram.create_variable(
        name="timestamp",
        var_type="DateTime",
        description="Post timestamp",
        source_file="models.py"
    )
    
    user_id_fk = diagram.create_variable(
        name="user_id",
        var_type="Integer",
        description="Foreign key to User table",
        source_file="models.py"
    )
    
    # Add attributes to Post class
    post_class.add_child(post_id)
    post_class.add_child(title)
    post_class.add_child(content)
    post_class.add_child(timestamp)
    post_class.add_child(user_id_fk)
    
    # Add Post class to the models module
    models_module.add_child(post_class)
    
    # Create form classes
    login_form = diagram.create_class(
        name="LoginForm",
        description="Login form class",
        source_file="forms.py"
    )
    
    # Add Login form fields
    username_field = diagram.create_variable(
        name="username",
        var_type="StringField",
        source_file="forms.py"
    )
    
    password_field = diagram.create_variable(
        name="password",
        var_type="PasswordField",
        source_file="forms.py"
    )
    
    submit_field = diagram.create_variable(
        name="submit",
        var_type="SubmitField",
        source_file="forms.py"
    )
    
    # Add fields to the LoginForm class
    login_form.add_child(username_field)
    login_form.add_child(password_field)
    login_form.add_child(submit_field)
    
    # Add LoginForm class to the forms module
    forms_module.add_child(login_form)
    
    # Create a registration form class
    registration_form = diagram.create_class(
        name="RegistrationForm",
        description="User registration form",
        source_file="forms.py"
    )
    
    # Add Registration form fields
    reg_username = diagram.create_variable(
        name="username",
        var_type="StringField",
        source_file="forms.py"
    )
    
    reg_email = diagram.create_variable(
        name="email",
        var_type="EmailField",
        source_file="forms.py"
    )
    
    reg_password = diagram.create_variable(
        name="password",
        var_type="PasswordField",
        source_file="forms.py"
    )
    
    reg_password2 = diagram.create_variable(
        name="password2",
        var_type="PasswordField",
        source_file="forms.py"
    )
    
    reg_submit = diagram.create_variable(
        name="submit",
        var_type="SubmitField",
        source_file="forms.py"
    )
    
    # Add fields to the RegistrationForm class
    registration_form.add_child(reg_username)
    registration_form.add_child(reg_email)
    registration_form.add_child(reg_password)
    registration_form.add_child(reg_password2)
    registration_form.add_child(reg_submit)
    
    # Add RegistrationForm class to the forms module
    forms_module.add_child(registration_form)
    
    # Create route functions
    index_route = diagram.create_function(
        name="index",
        description="Home page route",
        source_file="routes.py"
    )
    
    login_route = diagram.create_function(
        name="login",
        description="Login route",
        source_file="routes.py"
    )
    
    logout_route = diagram.create_function(
        name="logout",
        description="Logout route",
        source_file="routes.py"
    )
    
    register_route = diagram.create_function(
        name="register",
        description="Registration route",
        source_file="routes.py"
    )
    
    # Add route functions to the routes module
    routes_module.add_child(index_route)
    routes_module.add_child(login_route)
    routes_module.add_child(logout_route)
    routes_module.add_child(register_route)
    
    # Create main app creation function
    create_app = diagram.create_function(
        name="create_app",
        description="Application factory function",
        parameters=[("config_class", "object")],
        return_type="Flask",
        source_file="app.py"
    )
    
    # Add create_app function to the app module
    app_module.add_child(create_app)
    
    # Create an instance of the app
    app_instance = diagram.create_variable(
        name="app",
        var_type="Flask",
        description="Flask application instance",
        source_file="app.py"
    )
    
    # Add app instance to the app module
    app_module.add_child(app_instance)
    
    # Create db instance
    db_instance = diagram.create_variable(
        name="db",
        var_type="SQLAlchemy",
        description="SQLAlchemy database instance",
        source_file="models.py"
    )
    
    # Add db instance to the models module
    models_module.add_child(db_instance)
    
    # Create relationships
    
    # Module dependencies
    diagram.create_relationship(
        source_id=app_module.id,
        target_id=config_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=app_module.id,
        target_id=models_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=app_module.id,
        target_id=routes_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=models_module.id,
        target_id=app_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=routes_module.id,
        target_id=app_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=routes_module.id,
        target_id=models_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    diagram.create_relationship(
        source_id=routes_module.id,
        target_id=forms_module.id,
        relationship_type=RelationshipType.IMPORT
    )
    
    # Class relationships
    diagram.create_relationship(
        source_id=app_instance.id,
        target_id=flask_app.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    diagram.create_relationship(
        source_id=db_instance.id,
        target_id=sqlalchemy.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    diagram.create_relationship(
        source_id=user_class.id,
        target_id=db_instance.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    diagram.create_relationship(
        source_id=post_class.id,
        target_id=db_instance.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    diagram.create_relationship(
        source_id=post_class.id,
        target_id=user_class.id,
        relationship_type=RelationshipType.DEPENDENCY,
        name="belongs to"
    )
    
    diagram.create_relationship(
        source_id=login_route.id,
        target_id=login_form.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    diagram.create_relationship(
        source_id=register_route.id,
        target_id=registration_form.id,
        relationship_type=RelationshipType.DEPENDENCY
    )
    
    return diagram


def main():
    """Run the example."""
    # Create the diagram
    diagram = create_python_code_diagram()
    
    # Define the output directory and ensure it exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Define the output file path
    output_path = str(output_dir / "python_code_diagram.svg")
    
    # Render the diagram
    rendered_path = render_code_diagram(diagram, output_path)
    print(f"Code Diagram rendered to: {rendered_path}")


if __name__ == "__main__":
    main() 