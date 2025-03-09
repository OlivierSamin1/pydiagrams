"""
Layout module for PyDiagrams.

This module provides layout algorithms for positioning diagram elements.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum


class LayoutDirection(Enum):
    """Enum for layout direction."""
    TOP_TO_BOTTOM = "TB"
    BOTTOM_TO_TOP = "BT"
    LEFT_TO_RIGHT = "LR"
    RIGHT_TO_LEFT = "RL"


class LayoutType(Enum):
    """Enum for layout type."""
    HIERARCHICAL = "hierarchical"
    CIRCULAR = "circular"
    FORCE_DIRECTED = "force_directed"
    GRID = "grid"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    AUTO = "auto"


class Layout(ABC):
    """Base class for layout algorithms."""
    
    def __init__(self):
        """Initialize layout with default values."""
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
    def apply(self, diagram_data: Dict) -> Dict:
        """
        Apply layout to diagram data.
        
        Args:
            diagram_data: Dictionary with diagram elements and relationships
            
        Returns:
            Updated diagram data with positions
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
    Hierarchical layout algorithm for diagrams with parent-child relationships.
    Organizes elements in levels/ranks.
    """
    
    def __init__(self):
        """Initialize hierarchical layout."""
        super().__init__()
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
        
    def apply(self, diagram_data: Dict) -> Dict:
        """
        Apply hierarchical layout to diagram data.
        
        Args:
            diagram_data: Dictionary with diagram elements and relationships
            
        Returns:
            Updated diagram data with positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # based on the hierarchy implied by the relationships
        
        # For now, we'll just return the input data with a note
        diagram_data["layout_applied"] = True
        diagram_data["layout_type"] = "hierarchical"
        return diagram_data


class CircularLayout(Layout):
    """
    Circular layout algorithm that arranges elements in a circle.
    """
    
    def __init__(self):
        """Initialize circular layout."""
        super().__init__()
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
        
    def apply(self, diagram_data: Dict) -> Dict:
        """
        Apply circular layout to diagram data.
        
        Args:
            diagram_data: Dictionary with diagram elements and relationships
            
        Returns:
            Updated diagram data with positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # in a circular arrangement
        
        # For now, we'll just return the input data with a note
        diagram_data["layout_applied"] = True
        diagram_data["layout_type"] = "circular"
        return diagram_data


class GridLayout(Layout):
    """
    Grid layout algorithm that arranges elements in a grid.
    """
    
    def __init__(self):
        """Initialize grid layout."""
        super().__init__()
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
        
    def apply(self, diagram_data: Dict) -> Dict:
        """
        Apply grid layout to diagram data.
        
        Args:
            diagram_data: Dictionary with diagram elements and relationships
            
        Returns:
            Updated diagram data with positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # in a grid arrangement
        
        # For now, we'll just return the input data with a note
        diagram_data["layout_applied"] = True
        diagram_data["layout_type"] = "grid"
        return diagram_data


class ForceDirectedLayout(Layout):
    """
    Force-directed layout algorithm that positions elements based on simulated forces.
    Good for showing clusters and minimizing crossing edges.
    """
    
    def __init__(self):
        """Initialize force-directed layout."""
        super().__init__()
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
        
    def apply(self, diagram_data: Dict) -> Dict:
        """
        Apply force-directed layout to diagram data.
        
        Args:
            diagram_data: Dictionary with diagram elements and relationships
            
        Returns:
            Updated diagram data with positions
        """
        # This is a placeholder for the actual layout algorithm
        # In a real implementation, this would calculate positions
        # using a force-directed algorithm
        
        # For now, we'll just return the input data with a note
        diagram_data["layout_applied"] = True
        diagram_data["layout_type"] = "force_directed"
        return diagram_data 