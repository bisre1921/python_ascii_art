from typing import List

class Renderer:
    @staticmethod
    def render(lines: List[str]) -> None:
        if not lines:
            print("No ASCII art to display.")
            return
        
        for line in lines:
            print(line)

    @staticmethod
    def render_with_border(lines: List[str], title: str = "ASCII Art") -> None:
        if not lines:
            print("No ASCII art to display.")
            return

        max_width = max(len(line) for line in lines) if lines else 0
        border_width = max(max_width + 4, len(title) + 4)
        
        print("=" * border_width)
        print(f"| {title.center(border_width - 4)} |")
        print("=" * border_width)
        
        for line in lines:
            print(f"| {line.ljust(border_width - 4)} |")
        
        print("=" * border_width)

    @staticmethod
    def render_debug_info(lines: List[str], cell_count: int, bounds: tuple) -> None:
        min_x, max_x, min_y, max_y = bounds
        
        print(f"Debug Info:")
        print(f"  Cells parsed: {cell_count}")
        print(f"  Grid bounds: X[{min_x}..{max_x}], Y[{min_y}..{max_y}]")
        print(f"  Grid size: {max_x - min_x + 1}x{max_y - min_y + 1}")
        print(f"  Output lines: {len(lines)}")
        print()
        
        Renderer.render(lines)