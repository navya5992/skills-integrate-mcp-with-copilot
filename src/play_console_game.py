#!/usr/bin/env python3
"""
Memory Match Arena - Console Game Entry Point

Run this file to start playing the console-based Memory Match game!
"""

import sys
from pathlib import Path

# Add src to path so we can import memory_game
sys.path.insert(0, str(Path(__file__).parent))

from memory_game.console_game import ConsoleGame


def main():
    """Launch the Memory Match Arena console game."""
    game = ConsoleGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing! 👋\n")


if __name__ == "__main__":
    main()
