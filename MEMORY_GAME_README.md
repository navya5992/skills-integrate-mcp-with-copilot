# Memory Match Arena - Console Game

## 🎮 Overview

**Memory Match Arena** is a card-matching memory game built across three progressive stages:
1. **Stage 1** ✅ Console Application (Core Engine Validation) — *Complete*
2. **Stage 2** 🪟 Desktop Application (User Interaction) — *Coming Next*
3. **Stage 3** 🌐 Web Application (Scalability & Accessibility) — *Coming Later*

This document covers **Stage 1: Console Application**.

---

## 🌍 Theme: Countries & Flags

The game features 32 country/flag pairs, supporting three difficulty levels:
- **Easy**: 4×4 grid (8 pairs)
- **Medium**: 6×6 grid (18 pairs)
- **Hard**: 8×8 grid (32 pairs)

---

## 📋 How to Play

### 1. **Start the Game**

Run the console game:

```bash
cd /workspaces/skills-integrate-mcp-with-copilot
python src/play_console_game.py
```

### 2. **Select Difficulty**

```
Select Grid Size:
  (1) 4×4 Grid  -  8 pairs (Easy)
  (2) 6×6 Grid  - 18 pairs (Medium)
  (3) 8×8 Grid  - 32 pairs (Hard)

Enter your choice (1/2/3):
```

### 3. **Play a Turn**

- You flip exactly **2 cards per turn**
- Enter row (0-based) and column (0-based)
- If cards match → they stay face-up ✅
- If cards don't match → they flip back after 2 seconds ❌

### 4. **Win**

Match all pairs to win! 🎉

---

## 🏗️ Architecture

### **Strict Separation of Concerns**

```
┌─────────────────────────────────────────┐
│   Console UI (Input/Display)            │
│   - ConsoleRenderer (render grid/info)  │
│   - InputHandler (get user input)       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Game Controller (Flow)                │
│   - ConsoleGame (turn loop, timing)     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   CORE GAME ENGINE (Pure Logic) ⭐     │
│   - Game (main orchestrator)            │
│   - GameGrid (grid management)          │
│   - Card/CardPair (data structures)     │
│   NO UI CODE HERE - 100% Reusable!      │
└─────────────────────────────────────────┘
```

### **File Structure**

```
src/
├── memory_game/
│   ├── __init__.py              # Package exports
│   ├── game_engine.py           # Core logic (pure engine)
│   ├── card_data.py             # 32 country/flag pairs
│   ├── console_ui.py            # Console renderer & input handler
│   └── console_game.py          # Game flow controller
├── play_console_game.py         # Entry point
└── app.py                       # (Existing High School API)
```

---

## 🎯 Stage 1: Validation Checklist

✅ **Grid Initialization** — Correct pair count for each size  
✅ **Shuffling** — Cards positioned randomly each game  
✅ **Card Flipping** — Turn-based flip system (max 2 cards)  
✅ **Match Logic** — Matching pairs stay face-up  
✅ **Non-Match Handling** — Cards flip back after delay  
✅ **Turn Management** — Cannot flip >2 cards per turn  
✅ **Win Detection** — Game ends when all pairs matched  
✅ **Input Validation** — Prevents invalid moves, re-prompts  
✅ **Game Replay** — Choose to play again after winning  

---

## 🚀 Next Steps (Stages 2 & 3)

The core engine is **platform-agnostic** and reusable. Stages 2 and 3 will:

### **Stage 2: Desktop GUI (Tkinter)**
- Create `desktop_game.py` using Tkinter
- **Reuse** `game_engine.py` and `card_data.py` *without modification*
- Add click-based card flipping UI
- Replace `time.sleep()` with `after()` for async delays

### **Stage 3: Web Application (Flask)**
- Create `web_backend.py` (Flask server)
- Create `web_frontend/` (HTML/CSS/JS)
- **Reuse** `game_engine.py` and `card_data.py` *without modification*
- Handle session state management
- Add WebSocket for real-time UI updates

---

## 🧪 Testing

### Run Quick Unit Tests

```python
from src.memory_game.game_engine import Game
from src.memory_game.card_data import CARD_PAIRS

# Create game
game = Game(size=4, card_pairs=CARD_PAIRS)

# Flip cards
result1 = game.flip_card(0, 0)
result2 = game.flip_card(1, 1)

# Check state
print(game.is_won)        # False (no match)
print(game.move_count)    # 1
print(game.pairs_found)   # 0/8
```

---

## 🔧 Development Notes

### **Key Design Principles**

1. **Core Engine = Black Box**
   - Only public interface: `game.flip_card(row, col)` returns `FlipResult`
   - All validation and logic is private

2. **No Game Logic in UI**
   - UI only calls engine methods and renders results
   - Display code is completely decoupled from rules

3. **Reusable Across Platforms**
   - Same engine works for console, desktop, web
   - Only UI layer changes

4. **State Management**
   - Engine maintains complete game state
   - No UI-side state tracking needed

### **Custom Exceptions**

- `InvalidMoveError` — Raised when move violates game rules

### **Enums & Data Classes**

- `GameState` — PLAYING, WON
- `Card` — Individual card with country, flag, flip/match state
- `FlipResult` — Result of a flip operation
- `CardPair` — Pair structure

---

## 📖 Code Tour

### **game_engine.py** (Core Logic)

```python
# Create game
game = Game(size=4, card_pairs=CARD_PAIRS)

# Flip a card (main interface)
result = game.flip_card(row, col)

# Check game state
game.is_won                    # bool
game.move_count                # int
game.pairs_found / pairs_needed # tuple
game.get_card_display(row, col) # str (?, flag, or empty)

# Handle non-matches
game.reset_non_matching_flips()
```

### **console_ui.py** (Display & Input)

```python
# Render
ConsoleRenderer.render_grid(game)      # ASCII grid
ConsoleRenderer.render_info(game)      # Stats
ConsoleRenderer.render_full_screen(game)

# Input
InputHandler.get_difficulty()          # 4, 6, or 8
InputHandler.get_card_position(game)   # (row, col)
InputHandler.get_replay_choice()       # bool
```

### **console_game.py** (Game Flow)

```python
# Orchestrate
console_game = ConsoleGame()
console_game.select_difficulty()
console_game.start_game(size)
console_game.play_turn()
console_game.game_loop()
console_game.show_win_screen()
```

---

## 🎨 Terminal Display Example

```
🎮 MEMORY MATCH ARENA 🎮
========================================
      0    1    2    3  
   ┌─────┬─────┬─────┬─────┐
0  │  ?  │  ?  │  ?  │  ?  │
   ├─────┼─────┼─────┼─────┤
1  │  ?  │  ?  │  ?  │  ?  │
   ├─────┼─────┼─────┼─────┤
2  │  ?  │  ?  │  ?  │  ?  │
   ├─────┼─────┼─────┼─────┤
3  │  ?  │  ?  │  ?  │  ?  │
   └─────┴─────┴─────┴─────┘

========================================
Grid Size: 4×4
Pairs Found: 3/8
Moves: 5
Status: Playing
========================================

Flip Card #1:
Enter row (0-3): 0
Enter column (0-3): 0

🇨🇦 Canada!

Flip Card #2:
Enter row (0-3): 2
Enter column (0-3): 1

🇮🇳 India

❌ No match! Cards will flip back in 2 seconds...
```

---

## 📝 Notes

- **No external dependencies** — Only Python stdlib
- **Works in any terminal** — Tested on macOS, Linux, Windows
- **Colors not used** — Pure ASCII art for compatibility
- **Input validation** — Re-prompts on invalid entry

---

## 🎯 Success Criteria Met

- ✅ Core game logic implemented and tested
- ✅ Grid initializes correctly with correct pair counts
- ✅ Cards shuffle randomly each game
- ✅ Turn-based system (flip 2 cards)
- ✅ Match detection and flip-back delays working
- ✅ Input validation prevents invalid moves
- ✅ Win detection functioning properly
- ✅ Console interface provides clear feedback
- ✅ Engine completely decoupled from UI
- ✅ Ready for Stage 2 (Desktop) and Stage 3 (Web)

---

Happy playing! 🎮🌟
