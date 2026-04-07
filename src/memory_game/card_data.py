"""
Card Data for Memory Match Arena

Contains all country/flag pairs used in the game.
Sufficient pairs for maximum 8x8 grid (32 pairs needed).
"""

# 32 country/flag pairs - covers all grid sizes (4x4=8 pairs, 6x6=18 pairs, 8x8=32 pairs)
CARD_PAIRS = [
    ("Canada", "🇨🇦"),
    ("India", "🇮🇳"),
    ("Japan", "🇯🇵"),
    ("France", "🇫🇷"),
    ("Germany", "🇩🇪"),
    ("Brazil", "🇧🇷"),
    ("Spain", "🇪🇸"),
    ("Italy", "🇮🇹"),
    ("Mexico", "🇲🇽"),
    ("Australia", "🇦🇺"),
    ("United Kingdom", "🇬🇧"),
    ("South Korea", "🇰🇷"),
    ("Russia", "🇷🇺"),
    ("China", "🇨🇳"),
    ("Greece", "🇬🇷"),
    ("Portugal", "🇵🇹"),
    ("Netherlands", "🇳🇱"),
    ("Belgium", "🇧🇪"),
    ("Switzerland", "🇨🇭"),
    ("Sweden", "🇸🇪"),
    ("Norway", "🇳🇴"),
    ("Denmark", "🇩🇰"),
    ("Poland", "🇵🇱"),
    ("Turkey", "🇹🇷"),
    ("Egypt", "🇪🇬"),
    ("South Africa", "🇿🇦"),
    ("Kenya", "🇰🇪"),
    ("Nigeria", "🇳🇬"),
    ("Thailand", "🇹🇭"),
    ("Vietnam", "🇻🇳"),
    ("New Zealand", "🇳🇿"),
    ("Argentina", "🇦🇷"),
]

# Validate we have at least 32 pairs
if len(CARD_PAIRS) < 32:
    raise ValueError(
        f"Need at least 32 card pairs for 8x8 grid, but only have {len(CARD_PAIRS)}"
    )
