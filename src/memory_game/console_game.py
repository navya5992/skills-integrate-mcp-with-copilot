"""
Console Game Controller for Memory Match Arena

Orchestrates the game flow: difficulty selection, turn loop, timing,
and win detection. Acts as a bridge between the pure game engine and
the console UI.
"""

import time
from .game_engine import Game, InvalidMoveError
from .console_ui import ConsoleRenderer, InputHandler
from .card_data import CARD_PAIRS


class ConsoleGame:
    """Main controller for the console-based game."""

    # Delay in seconds before non-matching cards flip back
    FLIP_BACK_DELAY = 2.0

    def __init__(self):
        """Initialize the console game controller."""
        self.game: Game = None

    def select_difficulty(self) -> int:
        """
        Let player select game difficulty.

        Returns:
            Grid size (4, 6, or 8)
        """
        return InputHandler.get_difficulty()

    def start_game(self, size: int) -> None:
        """
        Start a new game with the given grid size.

        Args:
            size: Grid size (4, 6, or 8)
        """
        self.game = Game(size=size, card_pairs=CARD_PAIRS)
        ConsoleRenderer.render_full_screen(self.game)

    def play_turn(self) -> bool:
        """
        Execute a single player turn (flip 2 cards, check match, handle delay).

        Returns:
            True if game continues, False if game is won
        """
        # Get first card flip
        print("Flip Card #1:")
        row1, col1 = InputHandler.get_card_position(self.game)

        try:
            result1 = self.game.flip_card(row1, col1)
        except InvalidMoveError as e:
            print(f"❌ Invalid move: {e}")
            input("Press Enter to continue...")
            return not self.game.is_won

        ConsoleRenderer.render_full_screen(self.game)

        if result1.is_game_won:
            return False

        # Get second card flip
        print("Flip Card #2:")
        row2, col2 = InputHandler.get_card_position(self.game)

        try:
            result2 = self.game.flip_card(row2, col2)
        except InvalidMoveError as e:
            print(f"❌ Invalid move: {e}")
            input("Press Enter to continue...")
            return not self.game.is_won

        ConsoleRenderer.render_full_screen(self.game)

        # If non-match, show delay then flip back
        if not result2.is_matched:
            print(f"❌ No match! Cards will flip back in {self.FLIP_BACK_DELAY:.0f} seconds...")
            time.sleep(self.FLIP_BACK_DELAY)
            self.game.reset_non_matching_flips()
            ConsoleRenderer.render_full_screen(self.game)
        else:
            print("✅ Match found!")
            time.sleep(0.5)  # Brief pause to enjoy the match

        return not self.game.is_won

    def game_loop(self) -> None:
        """Main game loop - repeatedly execute turns until game is won."""
        while not self.game.is_won:
            game_continues = self.play_turn()
            if not game_continues:
                break

    def show_win_screen(self) -> None:
        """Display the win screen with stats."""
        ConsoleRenderer.render_game_won(self.game)

    def run(self) -> None:
        """
        Main entry point - run a complete game session.

        Allows multiple games via replay loop.
        """
        ConsoleRenderer.render_title()

        play = True
        while play:
            # Select difficulty
            size = self.select_difficulty()

            # Start game
            self.start_game(size)

            # Play game
            self.game_loop()

            # Show win
            self.show_win_screen()

            # Ask to replay
            play = InputHandler.get_replay_choice()

        ConsoleRenderer.clear_screen()
        print("Thanks for playing Memory Match Arena! 👋\n")
