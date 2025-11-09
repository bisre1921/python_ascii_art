from html.parser import HTMLParser
import re
from typing import List, Set
from ascii_art.core.models import Cell
import logging

logger = logging.getLogger(__name__)

class TextCollector(HTMLParser):
    """HTML parser that collects all text content from HTML tags."""
    
    def __init__(self):
        super().__init__()
        self.texts: List[str] = []
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        """Handle opening tags - ignore script and style content."""
        if tag.lower() in ('script', 'style'):
            self.in_script_or_style = True

    def handle_endtag(self, tag):
        """Handle closing tags."""
        if tag.lower() in ('script', 'style'):
            self.in_script_or_style = False

    def handle_data(self, data):
        """Extract text data, skipping script and style content."""
        if not self.in_script_or_style:
            text = data.strip()
            if text:
                self.texts.append(text)

    def get_items(self) -> List[str]:
        """
        Returns all text items, split by lines and cleaned.
        
        Returns:
            List of non-empty text strings
        """
        items = []
        for text in self.texts:
            # Split by newlines and clean each part
            for part in text.splitlines():
                part = part.strip()
                if part:
                    items.append(part)
        return items


class GoogleDocParser:
    """Parser for extracting ASCII art data from Google Docs HTML."""
    
    # Pattern for detecting integers (including negative)
    INT_PATTERN = re.compile(r'^-?\d+$')
    
    @staticmethod
    def parse_ascii_art(html: str) -> List[Cell]:
        """
        Parses HTML content to extract ASCII art cell data.
        
        The parser looks for patterns of: x-coordinate, character, y-coordinate
        in the text content of the HTML document.
        
        Args:
            html: HTML content from Google Docs
            
        Returns:
            List of Cell objects representing the ASCII art
        """
        collector = TextCollector()
        collector.feed(html)
        items = collector.get_items()
        
        logger.debug(f"Collected {len(items)} text items from HTML")
        
        # Try to find the start of the coordinate data
        items = GoogleDocParser._skip_preamble(items)
        
        # Extract coordinate triples (x, char, y)
        cells = GoogleDocParser._extract_coordinate_triples(items)
        
        # Apply additional filtering and validation
        cells = GoogleDocParser._filter_and_validate_cells(cells)
        
        logger.info(f"Successfully parsed {len(cells)} ASCII art cells")
        return cells

    @staticmethod
    def _skip_preamble(items: List[str]) -> List[str]:
        """
        Skips any preamble text before the coordinate data.
        
        Args:
            items: List of text items
            
        Returns:
            List starting from coordinate data
        """
        # Look for common headers that indicate start of coordinate data
        header_patterns = [
            "x-coordinate",
            "x coordinate", 
            "character",
            "y-coordinate",
            "y coordinate"
        ]
        
        for i, item in enumerate(items):
            item_lower = item.lower()
            for pattern in header_patterns:
                if pattern in item_lower:
                    logger.debug(f"Found header '{item}' at position {i}, skipping preamble")
                    # Skip the header and start from the next item
                    return items[i + 1:]
        
        # If no header found, assume data starts from beginning
        logger.debug("No header found, processing all items")
        return items

    @staticmethod
    def _extract_coordinate_triples(items: List[str]) -> List[Cell]:
        """
        Extracts coordinate triples (x, character, y) from text items.
        
        Args:
            items: List of text items
            
        Returns:
            List of Cell objects
        """
        cells = []
        
        # Look for patterns of: integer, character(s), integer
        for i in range(len(items) - 2):
            x_str, char_str, y_str = items[i:i+3]
            
            if (GoogleDocParser._is_integer(x_str) and 
                GoogleDocParser._is_integer(y_str) and 
                GoogleDocParser._is_valid_character(char_str)):
                
                try:
                    x = int(x_str)
                    y = int(y_str)
                    cell = Cell(x, y, char_str)
                    cells.append(cell)
                    logger.debug(f"Found cell: {cell}")
                except ValueError as e:
                    logger.warning(f"Failed to parse coordinates ({x_str}, {y_str}): {e}")
        
        logger.debug(f"Extracted {len(cells)} coordinate triples")
        return cells

    @staticmethod
    def _filter_and_validate_cells(cells: List[Cell]) -> List[Cell]:
        """
        Applies additional filtering and validation to cells.
        
        Args:
            cells: List of Cell objects
            
        Returns:
            Filtered list of Cell objects
        """
        if not cells:
            return cells
        
        # Remove duplicates while preserving order
        seen_positions: Set[tuple] = set()
        unique_cells = []
        
        for cell in cells:
            position = (cell.x, cell.y)
            if position not in seen_positions:
                seen_positions.add(position)
                unique_cells.append(cell)
            else:
                logger.debug(f"Removing duplicate cell at position {position}")
        
        # Log some statistics
        if unique_cells:
            xs = [c.x for c in unique_cells]
            ys = [c.y for c in unique_cells]
            logger.debug(f"Grid bounds: X[{min(xs)}..{max(xs)}], Y[{min(ys)}..{max(ys)}]")
        
        return unique_cells

    @staticmethod
    def _is_integer(text: str) -> bool:
        """
        Checks if text represents an integer (including negative).
        
        Args:
            text: Text to check
            
        Returns:
            True if text is an integer
        """
        return GoogleDocParser.INT_PATTERN.match(text) is not None

    @staticmethod
    def _is_valid_character(text: str) -> bool:
        """
        Checks if text is a valid character for ASCII art.
        
        Args:
            text: Text to check
            
        Returns:
            True if text is a valid character
        """
        # Allow single characters or short strings (up to 3 chars for unicode symbols)
        if len(text) == 0 or len(text) > 3:
            return False
        
        # Allow printable characters and common Unicode block characters
        valid_chars = set(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
        unicode_blocks = set('█░▒▓▀▄▌▐■□▪▫▬▭▮▯°∙·‿⁀⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞')
        
        # Check if all characters in the text are valid
        for char in text:
            if char not in valid_chars and char not in unicode_blocks:
                # Allow other printable Unicode characters
                if not char.isprintable():
                    return False
        
        return True