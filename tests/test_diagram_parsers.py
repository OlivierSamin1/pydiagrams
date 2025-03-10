"""
Tests for the diagram parsers (Mermaid and PlantUML).
"""

import os
import tempfile
from pathlib import Path

import pytest

from pydiagrams.parsers.base_parser import BaseParser
from pydiagrams.parsers.mermaid_parser import MermaidParser
from pydiagrams.parsers.plantuml_parser import PlantUMLParser
from pydiagrams.parsers.diagram_utils import (
    detect_diagram_file_type,
    parse_diagram_file,
    generate_diagram_from_file,
    is_diagram_file
)


class TestMermaidParser:
    """Tests for the MermaidParser class."""

    def test_detect_mermaid_by_extension(self):
        """Test detection of Mermaid files by extension."""
        with tempfile.NamedTemporaryFile(suffix=".mmd") as temp:
            assert BaseParser.detect_file_type(temp.name) == "mermaid"
    
    def test_parse_class_diagram(self):
        """Test parsing a Mermaid class diagram."""
        content = """
        classDiagram
            class User {
                +String username
                +String email
                +login()
                +logout()
            }
            class Product {
                +String name
                +Float price
                +getDetails()
            }
            User --> Product : views
        """
        
        parser = MermaidParser()
        data = parser.parse(content)
        
        assert data["type"] == "class"
        assert len(data["classes"]) == 2
        assert len(data["relationships"]) == 1
    
    def test_parse_flowchart(self):
        """Test parsing a Mermaid flowchart."""
        content = """
        graph TD
            A[Start] --> B{Is it valid?}
            B -- Yes --> C[Process]
            B -- No --> D[Reject]
            C --> E[End]
            D --> E
        """
        
        parser = MermaidParser()
        data = parser.parse(content)
        
        assert data["type"] == "flowchart"
        assert data["direction"] == "TD"


class TestPlantUMLParser:
    """Tests for the PlantUMLParser class."""

    def test_detect_plantuml_by_extension(self):
        """Test detection of PlantUML files by extension."""
        with tempfile.NamedTemporaryFile(suffix=".puml") as temp:
            assert BaseParser.detect_file_type(temp.name) == "plantuml"
    
    def test_parse_sequence_diagram(self):
        """Test parsing a PlantUML sequence diagram."""
        content = """
        @startuml
        Alice -> Bob: Authentication Request
        Bob --> Alice: Authentication Response
        
        Alice -> Bob: Another request
        Alice <-- Bob: Another response
        @enduml
        """
        
        parser = PlantUMLParser()
        data = parser.parse(content)
        
        assert data["type"] == "sequence"
    
    def test_parse_class_diagram(self):
        """Test parsing a PlantUML class diagram."""
        content = """
        @startuml
        class User {
          +String username
          +String email
          +login()
          +logout()
        }
        
        class Product {
          +String name
          +Float price
          +getDetails()
        }
        
        User --> Product : views
        @enduml
        """
        
        parser = PlantUMLParser()
        data = parser.parse(content)
        
        assert data["type"] == "class"


class TestDiagramUtils:
    """Tests for the diagram utility functions."""

    def test_is_diagram_file(self):
        """Test the is_diagram_file function."""
        with tempfile.NamedTemporaryFile(suffix=".mmd") as mermaid_file, \
             tempfile.NamedTemporaryFile(suffix=".puml") as plantuml_file, \
             tempfile.NamedTemporaryFile(suffix=".txt") as text_file:
            
            assert is_diagram_file(mermaid_file.name) is True
            assert is_diagram_file(plantuml_file.name) is True
            assert is_diagram_file(text_file.name) is False
    
    def test_parse_diagram_file(self):
        """Test the parse_diagram_file function."""
        with tempfile.NamedTemporaryFile(suffix=".mmd") as temp:
            # Write a simple Mermaid diagram
            content = "graph TD\nA[Start] --> B[End]"
            with open(temp.name, "w") as f:
                f.write(content)
            
            data, parser = parse_diagram_file(temp.name)
            assert data["type"] == "flowchart"
            assert isinstance(parser, MermaidParser)
    
    def test_generate_diagram_from_file(self):
        """Test the generate_diagram_from_file function."""
        with tempfile.NamedTemporaryFile(suffix=".mmd") as temp_in, \
             tempfile.NamedTemporaryFile(suffix=".svg") as temp_out:
            
            # Write a simple Mermaid diagram
            content = "graph TD\nA[Start] --> B[End]"
            with open(temp_in.name, "w") as f:
                f.write(content)
            
            output_path = generate_diagram_from_file(temp_in.name, temp_out.name)
            assert os.path.exists(output_path)
            
            # Check that the output file contains some SVG content
            with open(output_path, "r") as f:
                svg_content = f.read()
                assert "<svg" in svg_content 