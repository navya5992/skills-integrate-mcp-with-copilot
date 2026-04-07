"""
Desktop UI Components for Memory Match Arena (Tkinter)

Handles rendering and user interaction for the desktop GUI.
Contains NO game logic - only display and event handling.
All game logic is delegated to the core Game engine.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from .game_engine import Game
from typing import Callable, Optional, Tuple


class DesktopRenderer:
    """Renders the game grid and stats to a Tkinter window."""

    # Colors
    COLOR_HIDDEN = "#4a7c9e"
    COLOR_FLIPPED = "#87ceeb"
    COLOR_MATCHED = "#98ff98"
    COLOR_SELECTED = "#ffd700"
    COLOR_BACKGROUND = "#2c3e50"
    COLOR_TEXT = "#ffffff"

    CARD_SIZE = 80
    PADDING = 5
    FONT_COUNTRY = ("Arial", 28)
    FONT_STATS = ("Arial", 12, "bold")
    FONT_INFO = ("Arial", 10)

    def __init__(self, root: tk.Tk):
        """Initialize the renderer."""
        self.root = root
        self.root.title("🎮 Memory Match Arena 🎮")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLOR_BACKGROUND)

        self.grid_frame = None
        self.stats_frame = None
        self.button_frame = None
        self.card_buttons = {}  # Dict[(row, col)] = Button

    def setup_window(self, game: Game, on_card_click: Callable[[int, int], None]):
        """
        Setup and initialize the window layout.

        Args:
            game: Game instance
            on_card_click: Callback function for card clicks
        """
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = tk.Label(
            self.root,
            text="🎮 MEMORY MATCH ARENA 🎮",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BACKGROUND,
            fg=self.COLOR_TEXT,
        )
        title_label.pack(pady=10)

        # Stats frame (top)
        self.stats_frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        self.stats_frame.pack(pady=5)

        # Grid frame (center)
        self.grid_frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        self.grid_frame.pack(padx=10, pady=10)

        self._create_grid(game, on_card_click)
        self._update_stats(game)

        # Button frame (bottom)
        self.button_frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        self.button_frame.pack(pady=10)

    def _create_grid(
        self, game: Game, on_card_click: Callable[[int, int], None]
    ) -> None:
        """Create the card grid."""
        self.card_buttons = {}

        for row in range(game.size):
            for col in range(game.size):
                btn = tk.Button(
                    self.grid_frame,
                    width=6,
                    height=3,
                    font=self.FONT_COUNTRY,
                    bg=self.COLOR_HIDDEN,
                    fg=self.COLOR_TEXT,
                    relief=tk.RAISED,
                    bd=2,
                    command=lambda r=row, c=col: on_card_click(r, c),
                )
                btn.grid(row=row, column=col, padx=self.PADDING, pady=self.PADDING)
                self.card_buttons[(row, col)] = btn

    def _update_stats(self, game: Game) -> None:
        """Update the stats display."""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        pairs_found, pairs_needed = game.progress
        status = "🎉 GAME WON! 🎉" if game.is_won else "Status: Playing"

        stats_text = f"Grid: {game.size}×{game.size}  |  Pairs: {pairs_found}/{pairs_needed}  |  Moves: {game.move_count}  |  {status}"

        stats_label = tk.Label(
            self.stats_frame,
            text=stats_text,
            font=self.FONT_STATS,
            bg=self.COLOR_BACKGROUND,
            fg=self.COLOR_TEXT,
        )
        stats_label.pack()

    def update_card(self, game: Game, row: int, col: int) -> None:
        """Update a single card's display."""
        btn = self.card_buttons[(row, col)]
        card = game.grid.get_card(row, col)

        if card.is_matched:
            btn.config(state=tk.DISABLED, bg=self.COLOR_MATCHED, relief=tk.SUNKEN)
            btn.config(text=card.flag)
        elif card.is_flipped:
            btn.config(bg=self.COLOR_FLIPPED, text=card.flag, relief=tk.SUNKEN)
        else:
            btn.config(bg=self.COLOR_HIDDEN, text="❓", relief=tk.RAISED)

    def update_all_cards(self, game: Game) -> None:
        """Update all card displays."""
        for row in range(game.size):
            for col in range(game.size):
                self.update_card(game, row, col)

    def update_stats(self, game: Game) -> None:
        """Update the stats display."""
        self._update_stats(game)

    def add_button(
        self,
        text: str,
        command: Callable,
        color: str = "#5dade2",
        width: int = 15,
    ) -> None:
        """Add a button to the button frame."""
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            font=self.FONT_INFO,
            bg=color,
            fg=self.COLOR_TEXT,
            relief=tk.RAISED,
            bd=2,
            width=width,
            activebackground="#3498db",
        )
        btn.pack(side=tk.LEFT, padx=5)

    def clear_buttons(self) -> None:
        """Clear all buttons from the button frame."""
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def show_message(self, title: str, message: str) -> None:
        """Show an info message box."""
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str) -> None:
        """Show an error message box."""
        messagebox.showerror(title, message)

    def ask_difficulty(self) -> Optional[int]:
        """
        Ask user to select difficulty.

        Returns:
            4, 6, 8 for grid sizes, or None if cancelled
        """
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=self.COLOR_BACKGROUND)
        frame.pack(expand=True, padx=20, pady=20)

        title = tk.Label(
            frame,
            text="🎮 SELECT DIFFICULTY 🎮",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_BACKGROUND,
            fg=self.COLOR_TEXT,
        )
        title.pack(pady=20)

        selected = tk.IntVar(value=4)

        options = [
            ("Easy: 4×4 Grid (8 pairs)", 4),
            ("Medium: 6×6 Grid (18 pairs)", 6),
            ("Hard: 8×8 Grid (32 pairs)", 8),
        ]

        for text, value in options:
            rb = tk.Radiobutton(
                frame,
                text=text,
                variable=selected,
                value=value,
                font=self.FONT_INFO,
                bg=self.COLOR_BACKGROUND,
                fg=self.COLOR_TEXT,
                selectcolor="#4a7c9e",
            )
            rb.pack(anchor=tk.W, pady=5)

        def on_start():
            self.root.quit()
            self.root.difficulty = selected.get()

        start_btn = tk.Button(
            frame,
            text="Start Game",
            command=on_start,
            font=self.FONT_STATS,
            bg="#27ae60",
            fg=self.COLOR_TEXT,
            relief=tk.RAISED,
            bd=2,
            width=20,
        )
        start_btn.pack(pady=20)

        self.root.update()
        self.root.mainloop()

        difficulty = getattr(self.root, "difficulty", None)
        if difficulty:
            # Recreate mainloop for next phase
            self.root.withdraw()
            self.root.deiconify()
        return difficulty

    def ask_replay(self) -> bool:
        """
        Ask player if they want to play again.

        Returns:
            True to replay, False to quit
        """
        result = messagebox.askyesno("Game Over", "Play another game?")
        return result
