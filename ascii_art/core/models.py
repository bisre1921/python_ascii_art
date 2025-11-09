from dataclasses import dataclass
from typing import Dict, Tuple, List

@dataclass(frozen=True)
class Cell:
    """Represents a single character cell in ASCII art with coordinates."""
    x: int
    y: int
    char: str

    def __str__(self) -> str:
        return f"Cell({self.x}, {self.y}, '{self.char}')"


class ArtGrid:
    """Manages a collection of ASCII art cells and converts them to a 2D grid."""
    
    def __init__(self, cells: List[Cell]):
        self.cells = cells

    def to_matrix(self, fill_char: str = ' ') -> List[str]:
        """
        Converts the cells to a list of strings representing rows of the ASCII art.
        
        Args:
            fill_char: Character to use for empty positions (default: space)
            
        Returns:
            List of strings, each representing a row in the ASCII art
        """
        if not self.cells:
            return []

        # Find the bounds of the grid
        xs = [c.x for c in self.cells]
        ys = [c.y for c in self.cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Create lookup table for fast access
        lookup: Dict[Tuple[int, int], str] = {(c.x, c.y): c.char for c in self.cells}

        # Build the grid row by row (reverse Y-axis to flip vertically)
        rows = []
        for y in range(max_y, min_y - 1, -1):  # Count down from max_y to min_y
            row = ''.join(lookup.get((x, y), fill_char) for x in range(min_x, max_x + 1))
            # Remove trailing spaces to avoid unnecessary whitespace
            rows.append(row.rstrip())
        
        return rows

    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Returns (min_x, max_x, min_y, max_y) bounds of the grid."""
        if not self.cells:
            return (0, 0, 0, 0)
        
        xs = [c.x for c in self.cells]
        ys = [c.y for c in self.cells]
        return (min(xs), max(xs), min(ys), max(ys))

    def get_cell_count(self) -> int:
        """Returns the number of cells in the grid."""
        return len(self.cells)