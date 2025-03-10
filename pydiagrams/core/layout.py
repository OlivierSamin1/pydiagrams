"""
Layout module for PyDiagrams.

This module provides layout algorithms for arranging diagram elements.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum, auto


class LayoutDirection(Enum):
    """Enum for layout direction."""
    TOP_TO_BOTTOM = "TB"
    BOTTOM_TO_TOP = "BT"
    LEFT_TO_RIGHT = "LR"
    RIGHT_TO_LEFT = "RL"


class LayoutType(Enum):
    """Types of layout algorithms available."""
    NONE = auto()
    HIERARCHICAL = auto()
    CIRCULAR = auto()
    FORCE_DIRECTED = auto()
    GRID = auto()
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    AUTO = "auto"


class Layout(ABC):
    """Abstract base class for layout algorithms."""
    
    def __init__(self, layout_type: LayoutType):
        """Initialize the layout with a specific type."""
        self.layout_type = layout_type
        self.padding = 40
        self.element_spacing = 20
        self.rank_spacing = 60
        self.direction = LayoutDirection.TOP_TO_BOTTOM
        self.custom_settings: Dict[str, Any] = {}
        
    def set_padding(self, padding: int) -> 'Layout':
        """
        Set the diagram padding.
        
        Args:
            padding: Padding in pixels
            
        Returns:
            Self for method chaining
        """
        self.padding = padding
        return self
        
    def set_element_spacing(self, spacing: int) -> 'Layout':
        """
        Set the spacing between elements.
        
        Args:
            spacing: Spacing in pixels
            
        Returns:
            Self for method chaining
        """
        self.element_spacing = spacing
        return self
        
    def set_rank_spacing(self, spacing: int) -> 'Layout':
        """
        Set the spacing between ranks in hierarchical layouts.
        
        Args:
            spacing: Spacing in pixels
            
        Returns:
            Self for method chaining
        """
        self.rank_spacing = spacing
        return self
        
    def set_direction(self, direction: LayoutDirection) -> 'Layout':
        """
        Set the layout direction.
        
        Args:
            direction: Direction enum value
            
        Returns:
            Self for method chaining
        """
        self.direction = direction
        return self
        
    def add_custom_setting(self, key: str, value: Any) -> 'Layout':
        """
        Add a custom layout setting.
        
        Args:
            key: Setting name
            value: Setting value
            
        Returns:
            Self for method chaining
        """
        self.custom_settings[key] = value
        return self
        
    @abstractmethod
    def apply(self, elements: List[Any], relationships: List[Any]) -> Dict[str, Tuple[float, float]]:
        """
        Apply the layout algorithm to the given elements and relationships.
        
        Args:
            elements: List of diagram elements to layout
            relationships: List of relationships between elements
            
        Returns:
            Dictionary mapping element IDs to their (x, y) positions
        """
        pass
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert layout to a dictionary.
        
        Returns:
            Dictionary representation of the layout
        """
        result = {
            "type": self.__class__.__name__,
            "padding": self.padding,
            "element_spacing": self.element_spacing,
            "rank_spacing": self.rank_spacing,
            "direction": self.direction.value
        }
        
        # Add custom settings
        result.update(self.custom_settings)
        
        return result


class HierarchicalLayout(Layout):
    """
    Hierarchical layout implementation.
    
    This layout arranges elements in a hierarchical tree-like structure,
    with elements placed in layers based on their relationships.
    """
    
    def __init__(self):
        """Initialize the hierarchical layout."""
        super().__init__(LayoutType.HIERARCHICAL)
        self.layer_spacing = 100
        self.node_spacing = 50
        self.align_rank = "center"  # center, left, right
        self.min_layer_distance = 50
        
    def set_align_rank(self, align: str) -> 'HierarchicalLayout':
        """
        Set the alignment of elements within a rank.
        
        Args:
            align: Alignment ("center", "left", "right")
            
        Returns:
            Self for method chaining
        """
        self.align_rank = align
        return self
        
    def set_min_layer_distance(self, distance: int) -> 'HierarchicalLayout':
        """
        Set the minimum distance between layers.
        
        Args:
            distance: Distance in pixels
            
        Returns:
            Self for method chaining
        """
        self.min_layer_distance = distance
        return self
        
    def apply(self, elements: List[Any], relationships: List[Any]) -> Dict[str, Tuple[float, float]]:
        """
        Apply hierarchical layout to the elements.
        
        This is a simple implementation that:
        1. Assigns elements to layers based on relationship depth
        2. Positions elements within each layer horizontally
        3. Returns the calculated positions
        
        Args:
            elements: List of diagram elements to layout
            relationships: List of relationships between elements
            
        Returns:
            Dictionary mapping element IDs to their (x, y) positions
        """
        # Create a map of element IDs to their objects for easy lookup
        element_map = {element.id: element for element in elements}
        
        # Create adjacency lists for the graph
        outgoing = {element.id: set() for element in elements}
        incoming = {element.id: set() for element in elements}
        
        # Build the graph from relationships
        for rel in relationships:
            outgoing[rel.source_id].add(rel.target_id)
            incoming[rel.target_id].add(rel.source_id)
        
        # Assign layers to elements
        layers = self._assign_layers(element_map, outgoing, incoming)
        
        # Calculate positions based on layers
        positions = {}
        max_elements = max(len(layer) for layer in layers)
        total_width = max_elements * self.node_spacing
        
        for layer_idx, layer in enumerate(layers):
            y = layer_idx * self.layer_spacing + 50
            if len(layer) == 1:
                # Center single elements
                positions[layer[0]] = (total_width / 2, y)
            else:
                # Distribute elements evenly in the layer
                spacing = total_width / (len(layer) + 1)
                for idx, element_id in enumerate(layer, 1):
                    x = idx * spacing
                    positions[element_id] = (x, y)
        
        return positions
    
    def _assign_layers(
        self,
        element_map: Dict[str, Any],
        outgoing: Dict[str, set],
        incoming: Dict[str, set]
    ) -> List[List[str]]:
        """
        Assign elements to layers based on their relationships.
        
        Args:
            element_map: Dictionary mapping element IDs to their objects
            outgoing: Dictionary mapping element IDs to their outgoing connections
            incoming: Dictionary mapping element IDs to their incoming connections
            
        Returns:
            List of layers, where each layer is a list of element IDs
        """
        # Find root elements (those with no incoming connections)
        roots = [eid for eid, ins in incoming.items() if not ins]
        if not roots:
            # If no roots found, use any element as root
            roots = [next(iter(element_map.keys()))]
        
        # Initialize layers with root elements
        layers = [roots]
        processed = set(roots)
        
        # Process remaining elements
        while True:
            next_layer = []
            for parent_id in layers[-1]:
                # Add all unprocessed children to the next layer
                children = outgoing[parent_id] - processed
                next_layer.extend(children)
                processed.update(children)
            
            if not next_layer:
                # If no more elements to process in the next layer
                # Add any remaining unprocessed elements
                remaining = set(element_map.keys()) - processed
                if remaining:
                    next_layer.extend(remaining)
                    processed.update(remaining)
                
                if not remaining:
                    break
            
            layers.append(sorted(next_layer))  # Sort for consistent layout
        
        return layers


class CircularLayout(Layout):
    """
    Circular layout algorithm that arranges elements in a circle.
    """
    
    def __init__(self):
        """Initialize circular layout."""
        super().__init__(LayoutType.CIRCULAR)
        self.radius = 200
        self.start_angle = 0
        self.end_angle = 360
        self.equal_spacing = True
        
    def set_radius(self, radius: int) -> 'CircularLayout':
        """
        Set the circle radius.
        
        Args:
            radius: Radius in pixels
            
        Returns:
            Self for method chaining
        """
        self.radius = radius
        return self
        
    def set_angles(self, start: int, end: int) -> 'CircularLayout':
        """
        Set the start and end angles.
        
        Args:
            start: Start angle in degrees
            end: End angle in degrees
            
        Returns:
            Self for method chaining
        """
        self.start_angle = start
        self.end_angle = end
        return self
        
    def set_equal_spacing(self, equal: bool) -> 'CircularLayout':
        """
        Set whether to space elements equally around the circle.
        
        Args:
            equal: Whether to use equal spacing
            
        Returns:
            Self for method chaining
        """
        self.equal_spacing = equal
        return self
        
    def apply(self, elements: List[Any], relationships: List[Any]) -> Dict[str, Tuple[float, float]]:
        """
        Apply circular layout to the elements.
        
        Args:
            elements: List of diagram elements to layout
            relationships: List of relationships between elements
            
        Returns:
            Dictionary mapping element IDs to their (x, y) positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # in a circular arrangement
        
        # For now, we'll just return the input data with a note
        diagram_data = {
            "layout_applied": True,
            "layout_type": "circular"
        }
        
        return diagram_data


class GridLayout(Layout):
    """
    Grid layout algorithm that arranges elements in a grid.
    """
    
    def __init__(self):
        """Initialize grid layout."""
        super().__init__(LayoutType.GRID)
        self.columns = 0  # 0 means auto-calculate
        self.rows = 0  # 0 means auto-calculate
        self.cell_width = 200
        self.cell_height = 100
        self.align = "center"  # center, left, right
        
    def set_grid_size(self, columns: int, rows: int) -> 'GridLayout':
        """
        Set the grid dimensions.
        
        Args:
            columns: Number of columns (0 for auto)
            rows: Number of rows (0 for auto)
            
        Returns:
            Self for method chaining
        """
        self.columns = columns
        self.rows = rows
        return self
        
    def set_cell_size(self, width: int, height: int) -> 'GridLayout':
        """
        Set the cell dimensions.
        
        Args:
            width: Cell width in pixels
            height: Cell height in pixels
            
        Returns:
            Self for method chaining
        """
        self.cell_width = width
        self.cell_height = height
        return self
        
    def set_align(self, align: str) -> 'GridLayout':
        """
        Set the alignment of elements within cells.
        
        Args:
            align: Alignment ("center", "left", "right")
            
        Returns:
            Self for method chaining
        """
        self.align = align
        return self
        
    def apply(self, elements: List[Any], relationships: List[Any]) -> Dict[str, Tuple[float, float]]:
        """
        Apply grid layout to the elements.
        
        Args:
            elements: List of diagram elements to layout
            relationships: List of relationships between elements
            
        Returns:
            Dictionary mapping element IDs to their (x, y) positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # in a grid arrangement
        
        # For now, we'll just return the input data with a note
        diagram_data = {
            "layout_applied": True,
            "layout_type": "grid"
        }
        
        return diagram_data


class ForceDirectedLayout(Layout):
    """
    Force-directed layout algorithm that positions elements based on simulated forces.
    Good for showing clusters and minimizing crossing edges.
    """
    
    def __init__(self):
        """Initialize force-directed layout."""
        super().__init__(LayoutType.FORCE_DIRECTED)
        self.spring_constant = 0.1
        self.repulsion_constant = 100.0
        self.damping = 0.9
        self.iterations = 100
        
    def set_spring_constant(self, constant: float) -> 'ForceDirectedLayout':
        """
        Set the spring constant for edge forces.
        
        Args:
            constant: Spring constant value
            
        Returns:
            Self for method chaining
        """
        self.spring_constant = constant
        return self
        
    def set_repulsion_constant(self, constant: float) -> 'ForceDirectedLayout':
        """
        Set the repulsion constant for node forces.
        
        Args:
            constant: Repulsion constant value
            
        Returns:
            Self for method chaining
        """
        self.repulsion_constant = constant
        return self
        
    def set_damping(self, damping: float) -> 'ForceDirectedLayout':
        """
        Set the damping factor for the simulation.
        
        Args:
            damping: Damping factor between 0 and 1
            
        Returns:
            Self for method chaining
        """
        self.damping = max(0, min(1, damping))  # Clamp between 0 and 1
        return self
        
    def set_iterations(self, iterations: int) -> 'ForceDirectedLayout':
        """
        Set the number of simulation iterations.
        
        Args:
            iterations: Number of iterations
            
        Returns:
            Self for method chaining
        """
        self.iterations = iterations
        return self
        
    def apply(self, elements: List[Any], relationships: List[Any]) -> Dict[str, Tuple[float, float]]:
        """
        Apply force-directed layout to the elements.
        
        Args:
            elements: List of diagram elements to layout
            relationships: List of relationships between elements
            
        Returns:
            Dictionary mapping element IDs to their (x, y) positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # using a force-directed algorithm
        
        # For now, we'll just return the input data with a note
        diagram_data = {
            "layout_applied": True,
            "layout_type": "force_directed"
        }
        
        return diagram_data 