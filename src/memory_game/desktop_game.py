"""
Desktop Game Controller for Memory Match Arena

Orchestrates the game flow using Tkinter's event system.
Acts as a bridge between the pure game engine and the desktop UI.
Replaces time.sleep() with Tkinter's after() for non-blocking delays.
"""

import tkinter as tk
from .game_engine import Game, InvalidMoveError
from .desktop_ui import DesktopRenderer
from .card_data import CARD_PAIRS


class DesktopGame:
    """Main controller for the desktop-based game."""

    # Delay in milliseconds before non-matching cards flip back
    FLIP_BACK_DELAY = 2000  # 2 seconds
    MATCH_CELEBRATE_DELAY = 500  # 0.5 seconds

    def __init__(self):
        """Initialize the desktop game controller."""
        self.root = tk.Tk()
        self.renderer = DesktopRenderer(self.root)
        self.game: Game = None
        self.first_card_position: tuple = None
        self.card_flips_enabled = True

    def on_card_click(self, row: int, col: int) -> None:
        """
        Handle card click event.

        Args:
            row: Card row index
            col: Card column index
        """
        if not self.card_flips_enabled:
            self.renderer.show_error("Wait", "Please wait for cards to resolve...")
            return

        if self.game.is_won:
            self.renderer.show_error("Game Over", "Game already won! Click 'New Game' to play again.")
            return

        try:
            result = self.game.flip_card(row, col)
            self.renderer.update_card(self.game, row, col)
            self.renderer.update_stats(self.game)

            # First card of the turn
            if result.flipped_count == 1:
                self.first_card_position = (row, col)

            # Second card of the turn - check for match
            elif result.flipped_count == 2:
                self.card_flips_enabled = False

                if result.is_matched:
                    # Match found - celebrate then continue
                    self.root.after(
                        self.MATCH_CELEBRATE_DELAY,
                        self._on_match_found,
                    )
                else:
                    # No match - wait then flip back
                    self.root.after(
                        self.FLIP_BACK_DELAY,
                        self._on_no_match,
                    )

            # Check if won
            if result.is_game_won:
                self.card_flips_enabled = False
                self.root.after(500, self._on_game_won)

        except InvalidMoveError as e:
            self.renderer.show_error("Invalid Move", str(e))

    def _on_match_found(self) -> None:
        """Handle successful match."""
        self.renderer.update_stats(self.game)
        self.card_flips_enabled = True

    def _on_no_match(self) -> None:
        """Handle non-matching cards - flip them back."""
        self.game.reset_non_matching_flips()
        self.renderer.update_all_cards(self.game)
        self.renderer.update_stats(self.game)
        self.card_flips_enabled = True

    def _on_game_won(self) -> None:
        """Handle game won."""
        self.renderer.update_stats(self.game)

        msg = f"""
Congratulations! You Won! 🎉

Grid Size: {self.game.size}×{self.game.size}
Total Moves: {self.game.move_count}
Pairs Found: {self.game.pairs_found}/{self.game.pairs_needed}

Great job! 🌟
        """.strip()

        self.renderer.show_message("Game Won!", msg)
        self._setup_replay_screen()

    def _setup_replay_screen(self) -> None:
        """Setup the replay screen options."""
        self.renderer.clear_buttons()
        self.renderer.add_button("New Game", self._on_new_game, color="#27ae60")
        self.renderer.add_button("Quit", self._on_quit, color="#e74c3c")

    def _on_new_game(self) -> None:
        """Handle new game button."""
        self.run()

    def _on_quit(self) -> None:
        """Handle quit button."""
        self.root.quit()
        self.root.destroy()

    def start_game(self, size: int) -> None:
        """
        Start a new game with the given grid size.

        Args:
            size: Grid size (4, 6, or 8)
        """
        self.game = Game(size=size, card_pairs=CARD_PAIRS)
        self.first_card_position = None
        self.card_flips_enabled = True

        self.renderer.setup_window(self.game, self.on_card_click)
        self.renderer.clear_buttons()
        self.renderer.add_button("Quit Game", self._on_quit, color="#e74c3c")

    def run(self) -> None:
        """
        Main entry point - run a complete game session.

        Allows multiple games via replay loop.
        """
        # Get difficulty
        difficulty = self.renderer.ask_difficulty()

        if difficulty is None:
            self.root.destroy()
            return

        # Start game
        self.start_game(difficulty)

        # Run Tkinter event loop
        self.root.mainloop()
