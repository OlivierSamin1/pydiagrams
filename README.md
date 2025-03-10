# PyDiagrams

A comprehensive Python library for generating various types of diagrams programmatically.

## Overview

PyDiagrams is a versatile library designed to create professional diagrams through Python code. It supports multiple diagram types commonly used in software engineering, system design, and data modeling.

## Supported Diagram Types

### UML Diagrams
- Class Diagrams
- Sequence Diagrams
- Activity Diagrams
- Use Case Diagrams
- State Diagrams

### Entity and Data Diagrams
- Entity-Relationship Diagrams (ERD)
- Data Flow Diagrams (DFD)

### Architectural Diagrams
- Deployment Diagrams
- Network Diagrams
- System Context Diagrams
- Container Diagrams
- Component Diagrams

### Code Diagrams
- Code structure visualization
- Dependency graphs

### Text-Based Diagrams
- Mermaid syntax
- PlantUML syntax

## Features

- Intuitive, Pythonic API for diagram creation
- Multiple output formats (SVG, PNG, PDF)
- Customizable styling and theming
- Extensible architecture for custom diagram types
- Integration with documentation tools
- Support for Mermaid and PlantUML files

## Installation

```bash
pip install pydiagrams
```

## Quick Example

```python
from pydiagrams import ClassDiagram
from pydiagrams.elements import Class, Relationship

# Create a class diagram
diagram = ClassDiagram("Sample Class Diagram")

# Add classes
class1 = Class("Customer")
class1.add_attribute("name: str")
class1.add_attribute("email: str")
class1.add_method("register()")

class2 = Class("Order")
class2.add_attribute("order_id: int")
class2.add_attribute("date: datetime")
class2.add_method("place_order()")

# Add relationship
diagram.add_relationship(Relationship(class1, class2, "1", "*", "places"))

# Render the diagram
diagram.render("class_diagram.svg")
```

## Generating Diagrams from Mermaid or PlantUML Files

### Using Python

```python
from pydiagrams import create_diagram_from_file

# Generate a diagram from a Mermaid file
create_diagram_from_file("my_diagram.mmd", "output.svg")

# Generate a diagram from a PlantUML file
create_diagram_from_file("my_diagram.puml", "output.png", output_format="png")
```

### Using the Command Line

PyDiagrams includes a command-line interface for quick diagram generation:

```bash
# Generate SVG from a Mermaid file
pydiagrams my_diagram.mmd -o output.svg

# Generate PNG from a PlantUML file
pydiagrams my_diagram.puml -o output.png -f png

# Get help
pydiagrams --help
```

## Documentation

For full documentation, visit [docs.pydiagrams.org](https://docs.pydiagrams.org).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 