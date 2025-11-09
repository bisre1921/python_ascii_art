# ASCII Art Viewer 🎨

A Python tool that extracts and displays ASCII art from published Google Docs documents. The tool parses coordinate-based ASCII art data and renders it beautifully in the terminal with proper orientation and Unicode character support.

## ✨ Features

- 🌐 **Google Docs Integration** - Works with published Google Docs URLs (`/pub` format)
- 🎯 **Smart Parsing** - Automatically detects coordinate patterns (x, char, y) in document text
- 🔄 **Correct Orientation** - Handles coordinate system conversion for proper display
- 🎭 **Unicode Support** - Supports special characters like █, ░, ▀, and more
- 🖼️ **Multiple Display Modes** - Plain, bordered, and debug information views
- 🏗️ **Clean Architecture** - Modular design with separation of concerns
- 🚀 **Robust Error Handling** - Comprehensive validation and user-friendly error messages

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- `requests` library

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd TEST
```

2. Set up virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install requests
```

### Usage

Basic usage:
```bash
python main.py --url "https://docs.google.com/document/d/e/2PACX-.../pub"
```

With options:
```bash
# Display with decorative border
python main.py --url "<google-docs-url>" --border

# Show debug information
python main.py --url "<google-docs-url>" --info

# Use custom fill character
python main.py --url "<google-docs-url>" --fill "."

# Enable debug logging
python main.py --url "<google-docs-url>" --debug
```

## 📋 Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--url` | `-u` | Published Google Docs URL (required) | - |
| `--fill` | `-f` | Character for empty cells | `" "` (space) |
| `--border` | - | Display with decorative border | `False` |
| `--info` | - | Show grid statistics | `False` |
| `--debug` | - | Enable debug logging | `False` |
| `--quiet` | `-q` | Suppress info messages | `False` |
| `--timeout` | - | Request timeout in seconds | `15` |

## 📁 Project Structure

```
TEST/
├── ascii_art/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py      # Data structures (Cell, ArtGrid)
│   │   └── renderer.py    # Display logic
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── html_fetcher.py # HTTP client for Google Docs
│   │   └── html_parser.py  # HTML parsing & coordinate extraction
│   └── presentation/
│       ├── __init__.py
│       └── cli.py         # Command-line interface
├── main.py               # Entry point
└── README.md            # This file
```

## 🔧 How It Works

1. **Fetch HTML**: Downloads the published Google Docs content using the `/pub` URL
2. **Extract Text**: Parses HTML to collect all text nodes, ignoring scripts and styles
3. **Find Coordinates**: Identifies patterns of (x-coordinate, character, y-coordinate) triples
4. **Build Grid**: Constructs a 2D coordinate map with proper Y-axis orientation
5. **Render Output**: Displays the ASCII art with optional formatting and borders

### Coordinate System

The tool correctly handles Google Docs' coordinate system where Y=0 is at the bottom (mathematical coordinates) and converts it to display coordinates (Y=0 at top) for proper visual orientation.

## 📝 Examples

### Test Case 1: Simple "F" Shape
```bash
python main.py --url "https://docs.google.com/document/d/e/2PACX-1vSmVmKxyqWZ-piMuUS251weVuIABoqm7tSyFP-GqpM9atKcV2ShZMmt5mA2-uDg_9kVFS7Q1jeB84m0/pub"
```

Output:
```
█▀▀▀
█▀▀
█
```

### Test Case 2: Complex "HELLO" Art
```bash
python main.py --url "https://docs.google.com/document/d/e/2PACX-1vRCzUup1R8CGy3zk7DkdzJyMRvJRPI75Vl3s_9HelL7pr49bzi7-cBxg0zSKwxcWiEvNPxi4Wjj8c0n/pub" --border
```

Displays a large "HELLO" ASCII art with decorative border.

## 🏗️ Architecture

The project follows a clean 3-layer architecture:

- **Core Layer**: Domain models and business logic (`Cell`, `ArtGrid`, `Renderer`)
- **Infrastructure Layer**: External services and data access (`HTMLFetcher`, `GoogleDocParser`)  
- **Presentation Layer**: User interfaces and CLI (`ArgumentParser`, `CLI`)

## 🛠️ Development

### Key Components

- **`Cell`**: Immutable data class representing a single character at coordinates
- **`ArtGrid`**: Manages collection of cells and converts to 2D display matrix
- **`HTMLFetcher`**: Handles HTTP requests with proper headers and error handling
- **`GoogleDocParser`**: Extracts coordinate triples from HTML text nodes
- **`Renderer`**: Provides multiple display formats (plain, bordered, debug)

### Error Handling

- URL validation for Google Docs format
- HTTP error handling with descriptive messages
- Coordinate parsing validation
- Graceful handling of malformed data

## 🔍 Debugging

Enable debug mode to see detailed parsing information:

```bash
python main.py --url "<url>" --debug --info
```

This shows:
- HTTP request details
- Text extraction process
- Coordinate parsing steps
- Grid construction statistics

## 📋 Requirements

- Python 3.7+
- requests>=2.25.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Docs for providing the published document format
- Unicode Consortium for block character standards
- Python community for excellent built-in libraries

---

**Made with ❤️ for the ASCII Art Challenge**