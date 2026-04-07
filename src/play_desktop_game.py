#!/usr/bin/env python3
"""
Memory Match Arena - Desktop Game Entry Point

Run this file to start playing the desktop-based Memory Match game with Tkinter!

    python src/play_desktop_game.py
"""

import sys
from pathlib import Path

# Add src to path so we can import memory_game
sys.path.insert(0, str(Path(__file__).parent))

from memory_game.desktop_game import DesktopGame


def main():
    """Launch the Memory Match Arena desktop game."""
    game = DesktopGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing! 👋\n")


if __name__ == "__main__":
    main()
