"""
Card Data for Memory Match Arena

Contains all country/flag pairs used in the game.
Sufficient pairs for maximum 8x8 grid (32 pairs needed).
"""

# 32 country/flag pairs - covers all grid sizes (4x4=8 pairs, 6x6=18 pairs, 8x8=32 pairs)
# Format: (country_name, flag_emoji, country_code, flag_image_url)
CARD_PAIRS = [
    ("Canada", "🇨🇦", "ca", "https://flagcdn.com/w160/ca.png"),
    ("India", "🇮🇳", "in", "https://flagcdn.com/w160/in.png"),
    ("Japan", "🇯🇵", "jp", "https://flagcdn.com/w160/jp.png"),
    ("France", "🇫🇷", "fr", "https://flagcdn.com/w160/fr.png"),
    ("Germany", "🇩🇪", "de", "https://flagcdn.com/w160/de.png"),
    ("Brazil", "🇧🇷", "br", "https://flagcdn.com/w160/br.png"),
    ("Spain", "🇪🇸", "es", "https://flagcdn.com/w160/es.png"),
    ("Italy", "🇮🇹", "it", "https://flagcdn.com/w160/it.png"),
    ("Mexico", "🇲🇽", "mx", "https://flagcdn.com/w160/mx.png"),
    ("Australia", "🇦🇺", "au", "https://flagcdn.com/w160/au.png"),
    ("United Kingdom", "🇬🇧", "gb", "https://flagcdn.com/w160/gb.png"),
    ("South Korea", "🇰🇷", "kr", "https://flagcdn.com/w160/kr.png"),
    ("Russia", "🇷🇺", "ru", "https://flagcdn.com/w160/ru.png"),
    ("China", "🇨🇳", "cn", "https://flagcdn.com/w160/cn.png"),
    ("Greece", "🇬🇷", "gr", "https://flagcdn.com/w160/gr.png"),
    ("Portugal", "🇵🇹", "pt", "https://flagcdn.com/w160/pt.png"),
    ("Netherlands", "🇳🇱", "nl", "https://flagcdn.com/w160/nl.png"),
    ("Belgium", "🇧🇪", "be", "https://flagcdn.com/w160/be.png"),
    ("Switzerland", "🇨🇭", "ch", "https://flagcdn.com/w160/ch.png"),
    ("Sweden", "🇸🇪", "se", "https://flagcdn.com/w160/se.png"),
    ("Norway", "🇳🇴", "no", "https://flagcdn.com/w160/no.png"),
    ("Denmark", "🇩🇰", "dk", "https://flagcdn.com/w160/dk.png"),
    ("Poland", "🇵🇱", "pl", "https://flagcdn.com/w160/pl.png"),
    ("Turkey", "🇹🇷", "tr", "https://flagcdn.com/w160/tr.png"),
    ("Egypt", "🇪🇬", "eg", "https://flagcdn.com/w160/eg.png"),
    ("South Africa", "🇿🇦", "za", "https://flagcdn.com/w160/za.png"),
    ("Kenya", "🇰🇪", "ke", "https://flagcdn.com/w160/ke.png"),
    ("Nigeria", "🇳🇬", "ng", "https://flagcdn.com/w160/ng.png"),
    ("Thailand", "🇹🇭", "th", "https://flagcdn.com/w160/th.png"),
    ("Vietnam", "🇻🇳", "vn", "https://flagcdn.com/w160/vn.png"),
    ("New Zealand", "🇳🇿", "nz", "https://flagcdn.com/w160/nz.png"),
    ("Argentina", "🇦🇷", "ar", "https://flagcdn.com/w160/ar.png"),
]

# Validate we have at least 32 pairs
if len(CARD_PAIRS) < 32:
    raise ValueError(
        f"Need at least 32 card pairs for 8x8 grid, but only have {len(CARD_PAIRS)}"
    )
