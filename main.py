#!/usr/bin/env python3
"""
ASCII Art Viewer - Extract and display ASCII art from Google Docs

This script downloads published Google Docs content, parses ASCII art 
coordinate data, and renders the art in the terminal.

Usage:
    python main.py --url <google-docs-pub-url>

Example:
    python main.py --url "https://docs.google.com/document/d/e/2PACX-1vSmVmKxyqWZ-piMuUS251weVuIABoqm7tSyFP-GqpM9atKcV2ShZMmt5mA2-uDg_9kVFS7Q1jeB84m0/pub"
"""

from ascii_art.presentation.cli import run_cli

if __name__ == "__main__":
    run_cli()