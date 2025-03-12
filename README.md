# PyDiagrams

[![PyPI version](https://img.shields.io/pypi/v/pydiagrams.svg)](https://pypi.org/project/pydiagrams/)
[![Python versions](https://img.shields.io/pypi/pyversions/pydiagrams.svg)](https://pypi.org/project/pydiagrams/)
[![License](https://img.shields.io/pypi/l/pydiagrams.svg)](https://github.com/yourusername/pydiagrams/blob/main/LICENSE)

A powerful Python library for generating and rendering Mermaid diagrams with support for multiple output formats and interactive features.

## 🚀 Features

- **Multiple Output Formats**: Generate diagrams as SVG, PNG, or interactive HTML
- **Rich Interactive HTML**: Create web-based diagrams with zoom, pan, and export capabilities
- **Theming Support**: Choose from 6 built-in themes with dark mode options
- **Accessibility Features**: High-contrast theme and responsive design
- **Portable Outputs**: Option to inline resources for standalone HTML files
- **Simple API**: Easy-to-use Python API and command-line interface
- **Comprehensive Diagram Support**: Works with various diagram types:
  - **UML Diagrams**: Class, Sequence, Activity, State, Component, Use Case
  - **Architectural Diagrams**: Context, Container, Component, Deployment, Network
  - **Entity Diagrams**: Entity-Relationship Diagrams (ERD), Data Flow Diagrams (DFD)
  - **Flowcharts**: Process flows and decision trees

## 📦 Installation

```bash
pip install pydiagrams
```

### Requirements

- Python 3.6+
- For SVG/PNG output: [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (optional but recommended)

## 🔧 Quick Start

### Python API

```python
from pydiagrams import create_diagram_from_file

# Basic SVG generation
create_diagram_from_file("my_diagram.mmd", "output.svg")

# PNG output
create_diagram_from_file(
    "my_diagram.mmd", 
    "output.png", 
    output_format="png"
)

# Interactive HTML with theming and dark mode
create_diagram_from_file(
    "my_diagram.mmd", 
    "output.html", 
    output_format="html", 
    theme="blue", 
    dark_mode=True,
    inline_resources=True  # For portable HTML files
)
```

### Command Line Interface

```bash
# Generate SVG (default format)
pydiagrams my_diagram.mmd -o output.svg

# Generate PNG
pydiagrams my_diagram.mmd -o output.png -f png

# Generate interactive HTML with theme and dark mode
pydiagrams my_diagram.mmd -o output.html -f html --theme blue --dark-mode

# Generate portable HTML with inline resources
pydiagrams my_diagram.mmd -o output.html -f html --inline-resources
```

## 🎨 Themes and Customization

PyDiagrams supports the following themes:

| Theme | Description |
|-------|-------------|
| `default` | Clean, professional look with balanced colors |
| `forest` | Nature-inspired green theme |
| `dark` | Dark background with light elements |
| `neutral` | Balanced, muted colors for professional documents |
| `blue` | Blue-focused color scheme |
| `high-contrast` | High contrast for accessibility |

Each theme can be combined with dark mode for different visual styles.

## 🖥️ Interactive HTML Features

The HTML output includes several interactive features:

- **Zoom and Pan**: Navigate large diagrams with intuitive controls
- **Theme Selection**: Switch between themes directly in the browser
- **Dark Mode Toggle**: Easily switch between light and dark modes
- **Export Options**: Download the diagram as SVG or PNG
- **Responsive Design**: Adapts to different screen sizes and devices

## 📊 Supported Diagram Types

PyDiagrams supports all standard Mermaid diagram types:

### UML Diagrams
- Class Diagrams
- Sequence Diagrams
- Activity Diagrams
- State Diagrams
- Component Diagrams
- Use Case Diagrams

### Architectural Diagrams
- Context Diagrams
- Container Diagrams
- Component Diagrams
- Deployment Diagrams
- Network Diagrams

### Entity Diagrams
- Entity-Relationship Diagrams (ERD)
- Data Flow Diagrams (DFD)

### Other Diagrams
- Flowcharts
- Gantt Charts
- Pie Charts

## 📚 Examples

The library includes comprehensive examples in the `examples` directory:

```
examples/
├── mermaid_comprehensive_example.py  # Demonstrates all features
├── generate_all_examples.py          # Generates HTML for all examples
├── mermaid_examples/                 # Basic Mermaid examples
├── uml/                              # UML diagram examples
├── architectural/                    # Architectural diagram examples
├── entity/                           # Entity diagram examples
└── code/                             # Code-related diagram examples
```

To run the comprehensive example:

```bash
python examples/mermaid_comprehensive_example.py
```

To generate HTML for all examples:

```bash
python examples/generate_all_examples.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Documentation

For full documentation, visit [docs.pydiagrams.org](https://docs.pydiagrams.org).

## 🙏 Acknowledgements

- [Mermaid](https://mermaid-js.github.io/mermaid/) - The JavaScript-based diagramming and charting tool
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) - Command-line interface for Mermaid
