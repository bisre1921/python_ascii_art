from dataclasses import dataclass
from typing import Dict, Tuple, List

@dataclass(frozen=True)
class Cell:
    x: int
    y: int
    char: str

    def __str__(self) -> str:
        return f"Cell({self.x}, {self.y}, '{self.char}')"


class ArtGrid:
    def __init__(self, cells: List[Cell]):
        self.cells = cells

    def to_matrix(self, fill_char: str = ' ') -> List[str]:
        if not self.cells:
            return []

        xs = [c.x for c in self.cells]
        ys = [c.y for c in self.cells]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        lookup: Dict[Tuple[int, int], str] = {(c.x, c.y): c.char for c in self.cells}

        rows = []
        for y in range(max_y, min_y - 1, -1):
            row = ''.join(lookup.get((x, y), fill_char) for x in range(min_x, max_x + 1))
            rows.append(row.rstrip())
        
        return rows

    def get_bounds(self) -> Tuple[int, int, int, int]:
        if not self.cells:
            return (0, 0, 0, 0)
        
        xs = [c.x for c in self.cells]
        ys = [c.y for c in self.cells]
        return (min(xs), max(xs), min(ys), max(ys))

    def get_cell_count(self) -> int:
        return len(self.cells)