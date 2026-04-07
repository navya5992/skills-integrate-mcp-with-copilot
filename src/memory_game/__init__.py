"""
Memory Match Arena - Core Game Engine Package

A progressive engineering challenge featuring a memory-matching card game
built across three stages: Console, Desktop, and Web.
"""

from .game_engine import Game, GameGrid, Card, CardPair, GameState, InvalidMoveError
from .card_data import CARD_PAIRS

__all__ = [
    "Game",
    "GameGrid",
    "Card",
    "CardPair",
    "GameState",
    "InvalidMoveError",
    "CARD_PAIRS",
]
