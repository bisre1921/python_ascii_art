from html.parser import HTMLParser
import re
from typing import List, Set
from ascii_art.core.models import Cell
import logging

logger = logging.getLogger(__name__)

class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts: List[str] = []
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ('script', 'style'):
            self.in_script_or_style = True

    def handle_endtag(self, tag):
        if tag.lower() in ('script', 'style'):
            self.in_script_or_style = False

    def handle_data(self, data):
        if not self.in_script_or_style:
            text = data.strip()
            if text:
                self.texts.append(text)

    def get_items(self) -> List[str]:
        items = []
        for text in self.texts:
            for part in text.splitlines():
                part = part.strip()
                if part:
                    items.append(part)
        return items


class GoogleDocParser:
    INT_PATTERN = re.compile(r'^-?\d+$')
    
    @staticmethod
    def parse_ascii_art(html: str) -> List[Cell]:
        collector = TextCollector()
        collector.feed(html)
        items = collector.get_items()
        
        logger.debug(f"Collected {len(items)} text items from HTML")
        
        items = GoogleDocParser._skip_preamble(items)
        cells = GoogleDocParser._extract_coordinate_triples(items)
        cells = GoogleDocParser._filter_and_validate_cells(cells)
        
        logger.info(f"Successfully parsed {len(cells)} ASCII art cells")
        return cells

    @staticmethod
    def _skip_preamble(items: List[str]) -> List[str]:
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
                    return items[i + 1:]
        
        logger.debug("No header found, processing all items")
        return items

    @staticmethod
    def _extract_coordinate_triples(items: List[str]) -> List[Cell]:
        cells = []
        
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
        if not cells:
            return cells
        
        seen_positions: Set[tuple] = set()
        unique_cells = []
        
        for cell in cells:
            position = (cell.x, cell.y)
            if position not in seen_positions:
                seen_positions.add(position)
                unique_cells.append(cell)
            else:
                logger.debug(f"Removing duplicate cell at position {position}")
        
        if unique_cells:
            xs = [c.x for c in unique_cells]
            ys = [c.y for c in unique_cells]
            logger.debug(f"Grid bounds: X[{min(xs)}..{max(xs)}], Y[{min(ys)}..{max(ys)}]")
        
        return unique_cells

    @staticmethod
    def _is_integer(text: str) -> bool:
        return GoogleDocParser.INT_PATTERN.match(text) is not None

    @staticmethod
    def _is_valid_character(text: str) -> bool:
        if len(text) == 0 or len(text) > 3:
            return False
        
        valid_chars = set(' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
        unicode_blocks = set('█░▒▓▀▄▌▐■□▪▫▬▭▮▯°∙·‿⁀⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞')
        
        for char in text:
            if char not in valid_chars and char not in unicode_blocks:
                if not char.isprintable():
                    return False
        
        return True