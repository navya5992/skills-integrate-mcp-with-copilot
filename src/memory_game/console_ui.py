"""
Console UI Components for Memory Match Arena

Handles rendering and user input. Contains NO game logic - only display
and input handling. All game logic is delegated to the Game engine.
"""

import os
from typing import Tuple
from .game_engine import Game


class ConsoleRenderer:
    """Renders the game grid and stats to the console."""

    HIDDEN_CARD = "❓"
    GRID_BORDER = "─"
    GRID_CORNER = "┼"
    GRID_V_LINE = "│"
    GRID_H_LINE = "─"

    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        os.system("clear" if os.name == "posix" else "cls")

    @staticmethod
    def render_grid(game: Game) -> str:
        """
        Render the game grid as a string.

        Args:
            game: Game instance

        Returns:
            Multi-line string representation of the grid
        """
        lines = []
        size = game.size

        # Column headers
        header = "    "
        for col in range(size):
            header += f"  {col}  "
        lines.append(header)

        # Top border
        border = "   ┌" + ("─────┬" * (size - 1)) + "─────┐"
        lines.append(border)

        # Rows
        for row in range(size):
            row_line = f"{row}  │"
            for col in range(size):
                card_display = game.get_card_display(row, col)
                row_line += f"  {card_display}  │"
            lines.append(row_line)

            # Row separator
            if row < size - 1:
                separator = "   ├" + ("─────┼" * (size - 1)) + "─────┤"
            else:
                separator = "   └" + ("─────┴" * (size - 1)) + "─────┘"
            lines.append(separator)

        return "\n".join(lines)

    @staticmethod
    def render_info(game: Game) -> str:
        """
        Render game info (stats and status).

        Args:
            game: Game instance

        Returns:
            Multi-line string with game stats
        """
        lines = []
        lines.append("=" * 40)
        lines.append(f"Grid Size: {game.size}×{game.size}")
        lines.append(f"Pairs Found: {game.pairs_found}/{game.pairs_needed}")
        lines.append(f"Moves: {game.move_count}")

        if game.is_won:
            lines.append("\n🎉 GAME WON! 🎉")
        else:
            lines.append(f"Status: Playing")

        lines.append("=" * 40)
        return "\n".join(lines)

    @staticmethod
    def render_full_screen(game: Game) -> None:
        """
        Render complete game screen (clear, grid, and info).

        Args:
            game: Game instance
        """
        ConsoleRenderer.clear_screen()
        print("\n🎮 MEMORY MATCH ARENA 🎮")
        print("=" * 40)
        print(ConsoleRenderer.render_grid(game))
        print()
        print(ConsoleRenderer.render_info(game))
        print()

    @staticmethod
    def render_title() -> None:
        """Render the game title screen."""
        ConsoleRenderer.clear_screen()
        print("\n" + "=" * 50)
        print("🎮 WELCOME TO MEMORY MATCH ARENA 🎮".center(50))
        print("=" * 50)
        print("\nA game of memory and strategy!")
        print("\nFlip cards to find matching country pairs:")
        print("  🇨🇦 Canada    🇮🇳 India    🇯🇵 Japan    🇫🇷 France")
        print("  ... and many more!")
        print("\n" + "=" * 50 + "\n")

    @staticmethod
    def render_difficulty_menu() -> None:
        """Render the difficulty selection menu."""
        print("\nSelect Grid Size:")
        print("  (1) 4×4 Grid  -  8 pairs (Easy)")
        print("  (2) 6×6 Grid  - 18 pairs (Medium)")
        print("  (3) 8×8 Grid  - 32 pairs (Hard)")
        print()

    @staticmethod
    def render_game_won(game: Game) -> None:
        """
        Render the win screen.

        Args:
            game: Game instance
        """
        ConsoleRenderer.clear_screen()
        print("\n" + "=" * 50)
        print("🎉 CONGRATULATIONS! YOU WON! 🎉".center(50))
        print("=" * 50)
        print(f"\nGrid Size: {game.size}×{game.size}")
        print(f"Total Moves: {game.move_count}")
        print(f"Pairs Found: {game.pairs_found}/{game.pairs_needed}")
        print("\nGreat job! 🌟")
        print("\n" + "=" * 50 + "\n")


class InputHandler:
    """Handles user input for the game."""

    @staticmethod
    def get_difficulty() -> int:
        """
        Get player's difficulty selection.

        Returns:
            Grid size (4, 6, or 8)
        """
        while True:
            ConsoleRenderer.render_title()
            ConsoleRenderer.render_difficulty_menu()

            choice = input("Enter your choice (1/2/3): ").strip()

            if choice == "1":
                return 4
            elif choice == "2":
                return 6
            elif choice == "3":
                return 8
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                input("Press Enter to continue...")

    @staticmethod
    def get_card_position(game: Game) -> Tuple[int, int]:
        """
        Get player's card flip selection.

        Args:
            game: Game instance (for grid size validation)

        Returns:
            (row, col) tuple
        """
        while True:
            try:
                row_input = input(f"Enter row (0-{game.size - 1}): ").strip()
                col_input = input(f"Enter column (0-{game.size - 1}): ").strip()

                row = int(row_input)
                col = int(col_input)

                if not (0 <= row < game.size and 0 <= col < game.size):
                    print(
                        f"Invalid position! Row and column must be between 0 and {game.size - 1}."
                    )
                    continue

                return (row, col)

            except ValueError:
                print("Invalid input! Please enter numeric values.")

    @staticmethod
    def get_replay_choice() -> bool:
        """
        Ask player if they want to play again.

        Returns:
            True to play again, False to quit
        """
        while True:
            choice = input("\nPlay again? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                return True
            elif choice in ("n", "no"):
                return False
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")
