"""
Base Parser for PyDiagrams.

This module provides a base class for all parsers that convert different diagram syntax formats
into PyDiagrams internal representation.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Union, Optional


class BaseParser(ABC):
    """Base class for all diagram syntax parsers."""

    def __init__(self):
        """Initialize the parser."""
        self.content = ""
        self.diagram_data = {}

    @abstractmethod
    def parse(self, content: str) -> Dict[str, Any]:
        """
        Parse the diagram syntax and return a dictionary representing the diagram.

        Args:
            content: The diagram syntax content to parse

        Returns:
            A dictionary representing the parsed diagram
        """
        pass

    @classmethod
    def from_file(cls, file_path: Union[str, Path]) -> 'BaseParser':
        """
        Create a parser instance and load content from a file.

        Args:
            file_path: Path to the file containing diagram syntax

        Returns:
            A parser instance with content loaded from the file
        """
        parser = cls()
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        parser.content = file_path.read_text(encoding='utf-8')
        return parser

    @classmethod
    def from_string(cls, content: str) -> 'BaseParser':
        """
        Create a parser instance with the provided content.

        Args:
            content: The diagram syntax content

        Returns:
            A parser instance with the provided content
        """
        parser = cls()
        parser.content = content
        return parser

    @staticmethod
    def detect_file_type(file_path: Union[str, Path]) -> Optional[str]:
        """
        Detect the diagram syntax type from a file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            String identifying the diagram type ('mermaid', 'plantuml', etc.) or None if unknown
        """
        file_path = Path(file_path)
        
        # Check by extension
        if file_path.suffix.lower() == '.mmd':
            return 'mermaid'
        elif file_path.suffix.lower() in ('.puml', '.plantuml', '.iuml'):
            return 'plantuml'
        
        # Check by content
        content = file_path.read_text(encoding='utf-8')
        
        # Check for Mermaid syntax
        if content.strip().startswith('```mermaid') or 'graph ' in content.lower() or 'sequenceDiagram' in content:
            return 'mermaid'
        
        # Check for PlantUML syntax
        if content.strip().startswith('@startuml') or content.strip().startswith('@startmindmap'):
            return 'plantuml'
        
        return None 