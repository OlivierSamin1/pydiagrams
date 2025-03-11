# PyDiagrams

A Python library for generating Mermaid diagrams with support for SVG, PNG, and interactive HTML outputs.

## Features

- Generate diagrams from Mermaid files
- Output formats: SVG, PNG, and interactive HTML
- Theme customization with 6 built-in themes
- Dark mode support
- Interactive features in HTML output:
  - Zoom and pan
  - Theme switching
  - Dark mode toggle
  - Export options
  - Responsive design

## Installation

```bash
pip install pydiagrams
```

## Quick Start

### Python API

```python
from pydiagrams import create_diagram_from_file

# Generate SVG from a Mermaid file
create_diagram_from_file("my_diagram.mmd", "output.svg")

# Generate PNG from a Mermaid file
create_diagram_from_file("my_diagram.mmd", "output.png", output_format="png")

# Generate interactive HTML with a theme and dark mode
create_diagram_from_file(
    "my_diagram.mmd", 
    "output.html", 
    output_format="html", 
    theme="blue", 
    dark_mode=True
)
```

### Command Line Interface

```bash
# Generate SVG from a Mermaid file (default)
pydiagrams my_diagram.mmd -o output.svg

# Generate PNG from a Mermaid file
pydiagrams my_diagram.mmd -o output.png -f png

# Generate interactive HTML with a theme and dark mode
pydiagrams my_diagram.mmd -o output.html -f html --theme blue --dark-mode

# Generate HTML with inline resources for better portability
pydiagrams my_diagram.mmd -o output.html -f html --inline-resources
```

## Interactive HTML Features

The HTML output includes several interactive features:

- **Zoom and Pan**: Easily zoom in/out and navigate large diagrams
- **Theme Selection**: Choose from 6 built-in themes (default, forest, dark, neutral, blue, high-contrast)
- **Dark Mode**: Toggle between light and dark modes for better readability
- **Export Options**: Export the diagram as SVG or PNG directly from the browser
- **Responsive Design**: Adapts to different screen sizes and devices

## Themes

PyDiagrams supports the following themes:

- `default`: Clean, professional look
- `forest`: Nature-inspired green theme
- `dark`: Dark background with light elements
- `neutral`: Balanced, muted colors
- `blue`: Blue-focused color scheme
- `high-contrast`: High contrast for accessibility

## Examples

Check out the `examples` directory for comprehensive examples:

- `examples/mermaid_comprehensive_example.py`: Demonstrates all features
- `examples/mermaid_examples/`: Contains sample Mermaid diagram files

## Requirements

- Python 3.6+
- For SVG/PNG output: [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (optional but recommended)

## License

MIT

## Documentation

For full documentation, visit [docs.pydiagrams.org](https://docs.pydiagrams.org).
