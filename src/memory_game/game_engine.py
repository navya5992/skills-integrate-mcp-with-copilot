"""
Core Game Engine for Memory Match Arena

Pure logic layer - contains all game rules, state management, and validation.
No UI code here. This engine is platform-agnostic and reusable for console,
desktop, and web implementations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, List
import random


class GameState(Enum):
    """Enum representing the current state of the game."""
    PLAYING = "playing"
    WON = "won"


class InvalidMoveError(Exception):
    """Raised when an invalid move is attempted."""
    pass


@dataclass
class Card:
    """Represents a single card in the game grid."""
    country: str        # Country name
    flag: str           # Flag emoji
    country_code: str   # ISO country code (e.g., 'us', 'ca')
    flag_image_url: str # URL to flag image
    display_type: str   # 'name' or 'flag' - what to display
    is_flipped: bool = False
    is_matched: bool = False

    def flip(self):
        """Toggle the flipped state of the card."""
        if not self.is_matched:
            self.is_flipped = not self.is_flipped

    def __repr__(self):
        if self.is_matched:
            return f"Card({self.country}, matched)"
        return f"Card({self.country}, {'flipped' if self.is_flipped else 'hidden'})"


@dataclass
class CardPair:
    """Represents a pair of matching cards."""
    card1: Card
    card2: Card

    def are_matching(self) -> bool:
        """Check if both cards in the pair are of the same country."""
        return card1.country == card2.country if card1 and card2 else False


@dataclass
class FlipResult:
    """Result of flipping a card."""
    card: Card
    flipped_count: int  # How many cards are currently flipped (1 or 2)
    is_matched: bool = False
    is_game_won: bool = False


class GameGrid:
    """Manages the game grid, shuffling, and card access."""

    def __init__(self, size: int, card_pairs: List[Tuple[str, str, str, str]]):
        """
        Initialize game grid.

        Args:
            size: Grid size (4 for 4x4, 6 for 6x6, 8 for 8x8)
            card_pairs: List of (country, flag, country_code, flag_image_url) tuples to draw from
        """
        if size not in (4, 6, 8):
            raise ValueError("Grid size must be 4, 6, or 8")

        self.size = size
        self.grid_count = size * size
        self.pairs_needed = self.grid_count // 2

        if len(card_pairs) < self.pairs_needed:
            raise ValueError(
                f"Not enough card pairs. Need {self.pairs_needed}, got {len(card_pairs)}"
            )

        # Select and shuffle which pairs to use
        selected_pairs = random.sample(card_pairs, self.pairs_needed)

        # Create cards (each pair appears twice - one name, one flag)
        cards_list = []
        for country, flag, country_code, flag_image_url in selected_pairs:
            # One card shows country name
            cards_list.append(Card(country=country, flag=flag, country_code=country_code, flag_image_url=flag_image_url, display_type='name'))
            # Other card shows flag
            cards_list.append(Card(country=country, flag=flag, country_code=country_code, flag_image_url=flag_image_url, display_type='flag'))

        # Shuffle and create grid
        random.shuffle(cards_list)
        self.grid = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(cards_list[i * size + j])
            self.grid.append(row)

    def get_card(self, row: int, col: int) -> Card:
        """Get card at position (row, col)."""
        if not self._is_valid_position(row, col):
            raise InvalidMoveError(f"Position ({row}, {col}) is out of bounds")
        return self.grid[row][col]

    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= row < self.size and 0 <= col < self.size


class Game:
    """
    Main game orchestrator. Handles turn logic, matching, and game state.

    This is the interface that UIs interact with - it's a black box that
    only exposes game rules, not implementation details.
    """

    def __init__(self, size: int, card_pairs: List[Tuple[str, str, str, str]]):
        """
        Initialize a new game.

        Args:
            size: Grid size (4, 6, or 8)
            card_pairs: Available card pairs to use
        """
        self.size = size
        self.grid = GameGrid(size, card_pairs)
        self.state = GameState.PLAYING
        self.move_count = 0
        self.pairs_found = 0
        self.pairs_needed = self.grid.pairs_needed
        self.flipped_cards: List[Tuple[int, int]] = []  # [(row, col), (row, col)]

    def flip_card(self, row: int, col: int) -> FlipResult:
        """
        Flip a card at the given position.

        This is the main interface method UIs call. It validates the move,
        updates game state, and returns the result.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)

        Returns:
            FlipResult containing card info and game state

        Raises:
            InvalidMoveError: If move is invalid (out of bounds, already flipped, etc.)
        """
        if self.state == GameState.WON:
            raise InvalidMoveError("Game is already won. Cannot flip more cards.")

        # Get the card
        card = self.grid.get_card(row, col)

        # Validate move
        self._validate_flip(row, col, card)

        # Flip the card
        card.flip()
        self.flipped_cards.append((row, col))

        flipped_count = len(self.flipped_cards)

        result = FlipResult(
            card=card,
            flipped_count=flipped_count,
            is_matched=False,
            is_game_won=False,
        )

        # If 2 cards are flipped, check for match
        if flipped_count == 2:
            result.is_matched = self._check_and_handle_match()
            if result.is_matched:
                self.pairs_found += 1
                self.flipped_cards = []

            # Check win condition
            if self.pairs_found == self.pairs_needed:
                self.state = GameState.WON
                result.is_game_won = True

        return result

    def reset_non_matching_flips(self) -> None:
        """
        Flip back the two non-matching cards.

        Called after a delay when cards don't match.
        """
        if len(self.flipped_cards) == 2:
            row1, col1 = self.flipped_cards[0]
            row2, col2 = self.flipped_cards[1]

            card1 = self.grid.get_card(row1, col1)
            card2 = self.grid.get_card(row2, col2)

            card1.flip()
            card2.flip()
            self.flipped_cards = []

    def _validate_flip(self, row: int, col: int, card: Card) -> None:
        """Validate that a flip move is legal."""
        # Cannot flip if already have 2 flipped cards
        if len(self.flipped_cards) >= 2:
            raise InvalidMoveError(
                "Already flipped 2 cards. Resolve current pair first."
            )

        # Cannot flip already-matched card
        if card.is_matched:
            raise InvalidMoveError("Card is already matched.")

        # Cannot flip already-flipped card
        if card.is_flipped:
            raise InvalidMoveError("Card is already flipped.")

        # Cannot flip same card twice
        if (row, col) in self.flipped_cards:
            raise InvalidMoveError("Cannot flip the same card twice.")

    def _check_and_handle_match(self) -> bool:
        """
        Check if the two flipped cards match.

        If they match, mark them as matched and increment move count.
        """
        row1, col1 = self.flipped_cards[0]
        row2, col2 = self.flipped_cards[1]

        card1 = self.grid.get_card(row1, col1)
        card2 = self.grid.get_card(row2, col2)

        self.move_count += 1

        if card1.country == card2.country:
            # Match found
            card1.is_matched = True
            card2.is_matched = True
            return True
        return False

    def get_card_display(self, row: int, col: int) -> str:
        """
        Get the display representation of a card.

        Used by UI to render the card without exposing internals.

        Returns:
            "?" if hidden
            Country name or flag emoji if flipped/matched
            Empty space if error
        """
        try:
            card = self.grid.get_card(row, col)
            if card.is_matched or card.is_flipped:
                if card.display_type == 'name':
                    return card.country
                else:  # display_type == 'flag'
                    return card.flag
            return "?"
        except InvalidMoveError:
            return " "

    @property
    def is_won(self) -> bool:
        """Check if game is won."""
        return self.state == GameState.WON

    @property
    def progress(self) -> Tuple[int, int]:
        """Return (pairs_found, pairs_needed)."""
        return (self.pairs_found, self.pairs_needed)

    def __repr__(self):
        return (
            f"Game(size={self.size}, moves={self.move_count}, "
            f"pairs_found={self.pairs_found}/{self.pairs_needed}, state={self.state.value})"
        )
