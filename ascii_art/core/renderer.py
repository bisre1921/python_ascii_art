from typing import List
import sys

class Renderer:
    """Handles the display of ASCII art to the terminal."""

    @staticmethod
    def render(lines: List[str]) -> None:
        """
        Renders ASCII art lines to the terminal.
        
        Args:
            lines: List of strings representing the ASCII art rows
        """
        if not lines:
            print("No ASCII art to display.")
            return
        
        # Print each line of the ASCII art
        for line in lines:
            print(line)

    @staticmethod
    def render_with_border(lines: List[str], title: str = "ASCII Art") -> None:
        """
        Renders ASCII art with a decorative border.
        
        Args:
            lines: List of strings representing the ASCII art rows
            title: Optional title to display above the art
        """
        if not lines:
            print("No ASCII art to display.")
            return

        # Calculate the maximum width needed
        max_width = max(len(line) for line in lines) if lines else 0
        border_width = max(max_width + 4, len(title) + 4)
        
        # Print title and top border
        print("=" * border_width)
        print(f"| {title.center(border_width - 4)} |")
        print("=" * border_width)
        
        # Print the ASCII art with side borders
        for line in lines:
            print(f"| {line.ljust(border_width - 4)} |")
        
        # Print bottom border
        print("=" * border_width)

    @staticmethod
    def render_debug_info(lines: List[str], cell_count: int, bounds: tuple) -> None:
        """
        Renders ASCII art along with debug information.
        
        Args:
            lines: List of strings representing the ASCII art rows
            cell_count: Number of cells parsed
            bounds: Tuple of (min_x, max_x, min_y, max_y)
        """
        min_x, max_x, min_y, max_y = bounds
        
        print(f"Debug Info:")
        print(f"  Cells parsed: {cell_count}")
        print(f"  Grid bounds: X[{min_x}..{max_x}], Y[{min_y}..{max_y}]")
        print(f"  Grid size: {max_x - min_x + 1}x{max_y - min_y + 1}")
        print(f"  Output lines: {len(lines)}")
        print()
        
        Renderer.render(lines)