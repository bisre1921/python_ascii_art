import argparse
import logging
import sys
from typing import Optional
from ascii_art.infrastructure.html_fetcher import HTMLFetcher
from ascii_art.infrastructure.html_parser import GoogleDocParser
from ascii_art.core.models import ArtGrid
from ascii_art.core.renderer import Renderer

logger = logging.getLogger(__name__)

def setup_logging(debug: bool = False, quiet: bool = False) -> None:
    """
    Sets up logging configuration.
    
    Args:
        debug: Enable debug-level logging
        quiet: Suppress info-level logging
    """
    if quiet:
        level = logging.WARNING
    elif debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    format_string = "[%(levelname)s] %(message)s"
    if debug:
        format_string = "[%(levelname)s] %(name)s: %(message)s"
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[logging.StreamHandler(sys.stderr)]
    )

def create_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ASCII Art Viewer - Extract and display ASCII art from Google Docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url "https://docs.google.com/document/d/e/2PACX-.../pub"
  %(prog)s -u "https://docs.google.com/.../pub" --fill "."
  %(prog)s --url "https://docs.google.com/.../pub" --debug
        """
    )
    
    parser.add_argument(
        "--url", "-u",
        required=True,
        help="Published Google Docs URL ending with /pub"
    )
    
    parser.add_argument(
        "--fill", "-f",
        default=" ",
        help="Character to fill empty cells (default: space)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress info messages (only show errors)"
    )
    
    parser.add_argument(
        "--border",
        action="store_true",
        help="Display ASCII art with a decorative border"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show debug information about the parsed grid"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Request timeout in seconds (default: 15)"
    )
    
    return parser

def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validates command-line arguments.
    
    Args:
        args: Parsed arguments
        
    Raises:
        SystemExit: If validation fails
    """
    # Validate URL
    if not HTMLFetcher.validate_url(args.url):
        print("Error: Invalid Google Docs URL. Please provide a published Google Docs URL ending with /pub", 
              file=sys.stderr)
        sys.exit(1)
    
    # Validate fill character
    if len(args.fill) != 1:
        print("Error: Fill character must be exactly one character", file=sys.stderr)
        sys.exit(1)
    
    # Validate timeout
    if args.timeout <= 0:
        print("Error: Timeout must be a positive number", file=sys.stderr)
        sys.exit(1)

def run_cli() -> None:
    """Main CLI entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Set up logging first
    setup_logging(debug=args.debug, quiet=args.quiet)
    
    # Validate arguments
    validate_arguments(args)
    
    try:
        # Fetch the HTML content
        html = HTMLFetcher.fetch(args.url, timeout=args.timeout)
        
        # Parse ASCII art data
        cells = GoogleDocParser.parse_ascii_art(html)
        
        if not cells:
            print("No ASCII art data found in the document.", file=sys.stderr)
            sys.exit(1)
        
        # Create grid and render
        grid = ArtGrid(cells)
        lines = grid.to_matrix(fill_char=args.fill)
        
        if not lines:
            print("Failed to generate ASCII art grid.", file=sys.stderr)
            sys.exit(1)
        
        # Display results
        if args.info:
            bounds = grid.get_bounds()
            cell_count = grid.get_cell_count()
            Renderer.render_debug_info(lines, cell_count, bounds)
        elif args.border:
            Renderer.render_with_border(lines, "ASCII Art from Google Docs")
        else:
            Renderer.render(lines)
        
        logger.info(f"Successfully displayed ASCII art ({len(lines)} lines, {len(cells)} cells)")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        if args.debug:
            logger.exception("An error occurred:")
        else:
            logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()