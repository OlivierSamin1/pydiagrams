"""
Style module for PyDiagrams.

This module provides styling capabilities for diagrams and their elements.
"""

from typing import Dict, Any, Optional
import copy


class Style:
    """Class for styling diagram elements."""
    
    def __init__(self):
        """Initialize style with default values."""
        self.fill_color = "#FFFFFF"
        self.stroke_color = "#000000"
        self.stroke_width = 1
        self.text_color = "#000000"
        self.font_family = "Arial, Helvetica, sans-serif"
        self.font_size = 12
        self.font_weight = "normal"
        self.opacity = 1.0
        self.padding = 10
        self.corner_radius = 0
        self.dash_array = ""
        self.shadow = False
        self.shadow_color = "rgba(0, 0, 0, 0.3)"
        self.shadow_offset_x = 3
        self.shadow_offset_y = 3
        self.shadow_blur = 5
        self.custom_styles: Dict[str, Any] = {}
        
    def set_fill_color(self, color: str) -> 'Style':
        """
        Set the fill color.
        
        Args:
            color: Color in any CSS-compatible format
            
        Returns:
            Self for method chaining
        """
        self.fill_color = color
        return self
        
    def set_stroke_color(self, color: str) -> 'Style':
        """
        Set the stroke color.
        
        Args:
            color: Color in any CSS-compatible format
            
        Returns:
            Self for method chaining
        """
        self.stroke_color = color
        return self
        
    def set_stroke_width(self, width: float) -> 'Style':
        """
        Set the stroke width.
        
        Args:
            width: Width in pixels
            
        Returns:
            Self for method chaining
        """
        self.stroke_width = width
        return self
        
    def set_text_color(self, color: str) -> 'Style':
        """
        Set the text color.
        
        Args:
            color: Color in any CSS-compatible format
            
        Returns:
            Self for method chaining
        """
        self.text_color = color
        return self
        
    def set_font(self, family: str, size: int, weight: str = "normal") -> 'Style':
        """
        Set font properties.
        
        Args:
            family: Font family name
            size: Font size in points
            weight: Font weight (normal, bold, etc.)
            
        Returns:
            Self for method chaining
        """
        self.font_family = family
        self.font_size = size
        self.font_weight = weight
        return self
        
    def set_opacity(self, opacity: float) -> 'Style':
        """
        Set the opacity.
        
        Args:
            opacity: Opacity value between 0 and 1
            
        Returns:
            Self for method chaining
        """
        self.opacity = max(0, min(1, opacity))  # Clamp between 0 and 1
        return self
        
    def set_padding(self, padding: int) -> 'Style':
        """
        Set the padding.
        
        Args:
            padding: Padding in pixels
            
        Returns:
            Self for method chaining
        """
        self.padding = padding
        return self
        
    def set_corner_radius(self, radius: int) -> 'Style':
        """
        Set the corner radius for rounded rectangles.
        
        Args:
            radius: Corner radius in pixels
            
        Returns:
            Self for method chaining
        """
        self.corner_radius = radius
        return self
        
    def set_dash_array(self, dash_array: str) -> 'Style':
        """
        Set the stroke dash array.
        
        Args:
            dash_array: SVG dash array format (e.g., "5,5" for dashed line)
            
        Returns:
            Self for method chaining
        """
        self.dash_array = dash_array
        return self
        
    def enable_shadow(self, 
                     enable: bool = True, 
                     color: Optional[str] = None,
                     offset_x: Optional[int] = None,
                     offset_y: Optional[int] = None,
                     blur: Optional[int] = None) -> 'Style':
        """
        Enable or configure shadow.
        
        Args:
            enable: Whether to enable shadow
            color: Shadow color
            offset_x: Horizontal offset in pixels
            offset_y: Vertical offset in pixels
            blur: Blur radius in pixels
            
        Returns:
            Self for method chaining
        """
        self.shadow = enable
        if color is not None:
            self.shadow_color = color
        if offset_x is not None:
            self.shadow_offset_x = offset_x
        if offset_y is not None:
            self.shadow_offset_y = offset_y
        if blur is not None:
            self.shadow_blur = blur
        return self
        
    def add_custom_style(self, key: str, value: Any) -> 'Style':
        """
        Add a custom style property.
        
        Args:
            key: Style property name
            value: Style property value
            
        Returns:
            Self for method chaining
        """
        self.custom_styles[key] = value
        return self
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert style to a dictionary.
        
        Returns:
            Dictionary representation of the style
        """
        result = {
            "fill_color": self.fill_color,
            "stroke_color": self.stroke_color,
            "stroke_width": self.stroke_width,
            "text_color": self.text_color,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "opacity": self.opacity,
            "padding": self.padding,
            "corner_radius": self.corner_radius,
            "dash_array": self.dash_array,
            "shadow": self.shadow,
            "shadow_color": self.shadow_color,
            "shadow_offset_x": self.shadow_offset_x,
            "shadow_offset_y": self.shadow_offset_y,
            "shadow_blur": self.shadow_blur
        }
        
        # Add custom styles
        result.update(self.custom_styles)
        
        return result
        
    def clone(self) -> 'Style':
        """
        Create a deep copy of this style.
        
        Returns:
            A new Style instance with the same properties
        """
        new_style = Style()
        new_style.fill_color = self.fill_color
        new_style.stroke_color = self.stroke_color
        new_style.stroke_width = self.stroke_width
        new_style.text_color = self.text_color
        new_style.font_family = self.font_family
        new_style.font_size = self.font_size
        new_style.font_weight = self.font_weight
        new_style.opacity = self.opacity
        new_style.padding = self.padding
        new_style.corner_radius = self.corner_radius
        new_style.dash_array = self.dash_array
        new_style.shadow = self.shadow
        new_style.shadow_color = self.shadow_color
        new_style.shadow_offset_x = self.shadow_offset_x
        new_style.shadow_offset_y = self.shadow_offset_y
        new_style.shadow_blur = self.shadow_blur
        new_style.custom_styles = copy.deepcopy(self.custom_styles)
        return new_style


class Theme:
    """Class for managing diagram themes."""
    
    def __init__(self, name: str = "default"):
        """
        Initialize a theme.
        
        Args:
            name: Theme name
        """
        self.name = name
        self.diagram_style = Style()
        self.element_styles: Dict[str, Style] = {}
        self.relationship_styles: Dict[str, Style] = {}
        
    def set_diagram_style(self, style: Style) -> None:
        """
        Set the base style for diagrams using this theme.
        
        Args:
            style: Style to apply to diagrams
        """
        self.diagram_style = style
        
    def set_element_style(self, element_type: str, style: Style) -> None:
        """
        Set the style for a specific element type.
        
        Args:
            element_type: Type of element to style
            style: Style to apply to elements of this type
        """
        self.element_styles[element_type] = style
        
    def set_relationship_style(self, relationship_type: str, style: Style) -> None:
        """
        Set the style for a specific relationship type.
        
        Args:
            relationship_type: Type of relationship to style
            style: Style to apply to relationships of this type
        """
        self.relationship_styles[relationship_type] = style
        
    def get_element_style(self, element_type: str) -> Style:
        """
        Get the style for a specific element type.
        
        Args:
            element_type: Type of element
            
        Returns:
            Style for this element type, or a default style if not found
        """
        return self.element_styles.get(element_type, Style())
        
    def get_relationship_style(self, relationship_type: str) -> Style:
        """
        Get the style for a specific relationship type.
        
        Args:
            relationship_type: Type of relationship
            
        Returns:
            Style for this relationship type, or a default style if not found
        """
        return self.relationship_styles.get(relationship_type, Style()) 