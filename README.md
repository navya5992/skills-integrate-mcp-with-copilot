# Integrate MCP with Copilot

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="200px" />

This repository contains the **Memory Match Arena** project — a progressive engineering challenge building a memory-matching card game across three stages.

---

## 🎮 Memory Match Arena

A card-based memory game where players flip cards to find matching pairs. The project demonstrates **clean architecture** and **separation of concerns** by building the same game across three different platforms:

### **📊 Project Status**

| Stage | Status | Type | Play Command |
|-------|--------|------|--------------|
| **Stage 1** | ✅ Complete | Console | `python src/play_console_game.py` |
| **Stage 2** | ✅ Complete | Desktop (Tkinter) | `python src/play_desktop_game.py` |
| **Stage 3** | 🚀 Coming | Web (Flask) | TBD |

### **📚 Documentation**

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — Overall project overview
- [MEMORY_GAME_README.md](MEMORY_GAME_README.md) — Stage 1 (Console) guide
- [DESKTOP_GAME_README.md](DESKTOP_GAME_README.md) — Stage 2 (Desktop) guide

### **🚀 Quick Start**

```bash
# Play console version
python src/play_console_game.py

# Play desktop version (GUI)
python src/play_desktop_game.py
```

### **🎯 Key Features**

✅ **Multiple grid sizes**: 4×4 (Easy), 6×6 (Medium), 8×8 (Hard)  
✅ **Countries & Flags theme**: 32 unique country-flag pairs  
✅ **Reusable core engine**: Same logic across all 3 stages  
✅ **Clean architecture**: UI completely separated from game logic  
✅ **Progressive stages**: Console → Desktop → Web  

### **🏗️ Architecture Highlights**

- **Core Engine** (`game_engine.py`): 350+ lines of pure logic, no UI knowledge
- **Stage 1**: Console UI with text input and ASCII grid
- **Stage 2**: Tkinter GUI with click-based interaction
- **Stage 3**: Flask backend + web frontend (planned)

**Key Principle**: The core engine is modified **zero times** across all three stages!

---

## 📂 Repository Structure

```
/
├── src/
│   ├── memory_game/              # Memory Match Arena game code
│   │   ├── game_engine.py        # ⭐ Core logic (reused in all stages)
│   │   ├── card_data.py          # ⭐ Country/flag data
│   │   ├── console_ui.py         # Stage 1: Console UI
│   │   ├── console_game.py       # Stage 1: Game controller
│   │   ├── desktop_ui.py         # Stage 2: Tkinter UI
│   │   └── desktop_game.py       # Stage 2: Desktop controller
│   ├── play_console_game.py      # Stage 1: Entry point
│   ├── play_desktop_game.py      # Stage 2: Entry point
│   └── app.py                    # (Original High School API)
│
├── PROJECT_STATUS.md             # Overall project status
├── MEMORY_GAME_README.md         # Stage 1 documentation
├── DESKTOP_GAME_README.md        # Stage 2 documentation
└── README.md                     # This file
```

---

## 🎯 Learning Outcomes

This project demonstrates:

1. **Separation of Concerns** — Game logic isolated from UI
2. **Reusable Architecture** — Same engine works for console, desktop, and web
3. **Design Patterns** — MVC-like architecture applied to game development
4. **Event-Driven Programming** — Different event models per platform
5. **Cross-Platform Development** — Moving logic between console, GUI, and web
6. **Python Fundamentals** — Classes, data structures, exception handling
7. **UI Frameworks** — Console printing, Tkinter, (Flask + JavaScript coming)

---

## 🛠️ Technologies Used

### **Stage 1 (Console)**
- Python 3
- Standard library only

### **Stage 2 (Desktop)**
- Python 3
- Tkinter (built-in)

### **Stage 3 (Web)** [Planned]
- Python 3 + Flask
- HTML5 + CSS3 + JavaScript

---

## 📋 Original Exercise

<img src="https://octodex.github.com/images/Professortocat_v2.png" align="right" height="100px" />

This repository was originally prepared as an exercise by GitHub. 

Hey navya5992! Remember, it's self-paced so feel free to take a break! ☕️

[![](https://img.shields.io/badge/Go%20to%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/navya5992/skills-integrate-mcp-with-copilot/issues/1)

---

&copy; 2025 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

