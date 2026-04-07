# Memory Match Arena - Web Application (Stage 3)

## 🌐 Overview

**Stage 3: Web Application** completes the Memory Match Arena journey by bringing the game to the browser! 

### Key Principle: **100% Core Engine Reusability**

✅ The web app **reuses** `game_engine.py` and `card_data.py` **without any modifications**  
✅ All backend logic uses the same core engine  
✅ Frontend communicates via REST API  

---

## 🚀 Quick Start

### **Option 1: Run Locally (Recommended)**

```bash
# Navigate to project
cd skills-integrate-mcp-with-copilot

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m flask --app src.web_backend run
# Or:
python src/web_backend.py
```

Server starts at: **http://localhost:5000**

### **Option 2: Development Mode**

```bash
python src/web_backend.py
```

Then open browser to: http://localhost:5000

---

## 🎮 How to Play

1. **Open** http://localhost:5000 in your browser
2. **Select difficulty** (4×4, 6×6, or 8×8)
3. **Click "Start Game"**
4. **Click cards** to flip and find matches
5. **Win** when all pairs are matched! 🎉

---

## 📱 Mobile & Network Access

The game is fully accessible on mobile devices and across your local network:

### **Desktop Access**
- Desktop browser: `http://localhost:5000` or `http://127.0.0.1:5000`

### **Mobile Access** 
- On the same network as your dev container
- Open: `http://<container-ip>:5000`
- Example: `http://10.0.4.242:5000`

### **Quick Mobile Setup**
1. Find the container's network IP (displayed on the game page)
2. On your mobile device, open the game URL
3. Or scan the QR code on the desktop version
4. The game works on all screen sizes

### **QR Code**
- Built into the game page
- Points to the network IP
- Shareable with others on the same network
- Download the QR code image for offline sharing

### **Responsive Design**
✅ Desktop browsers  
✅ Tablets  
✅ Mobile phones  
✅ Any device with a web browser  

## 🏗️ Architecture

### **Web App Layers**

```
┌─────────────────────────────────────────┐
│   HTML/CSS/JavaScript (Browser)         │
│   - Renders UI                          │
│   - Handles user clicks                 │
│   - Updates display                     │
└──────────────┬──────────────────────────┘
               │ JSON API calls
┌──────────────▼──────────────────────────┐
│   Flask REST API (web_backend.py)       │
│   - Game session management             │
│   - Card flip orchestration             │
│   - Returns game state                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   CORE GAME ENGINE (game_engine.py) ⭐ │
│   - ZERO CHANGES from Stage 1 & 2      │
│   - Pure logic, no web knowledge       │
└─────────────────────────────────────────┘
```

### **File Structure**

```
src/
├── web_backend.py                 # Flask REST API server
├── memory_game/
│   ├── game_engine.py            # ⭐ Core (unchanged)
│   ├── card_data.py              # ⭐ Data (unchanged)
│   └── ...
└── web_frontend/
    ├── index.html                # Game UI
    ├── styles.css                # Styling
    └── static/
        └── app.js                # Client-side logic
```

---

## 📡 API Endpoints

### **1. Start New Game**

**POST** `/api/game/new`

```json
Request:
{
    "size": 4  // 4, 6, or 8
}

Response (201):
{
    "session_id": "uuid-string",
    "game": {
        "size": 4,
        "pairs_needed": 8,
        "pairs_found": 0,
        "moves": 0,
        "is_won": false,
        "state": "playing"
    },
    "grid": [ ... ]
}
```

### **2. Get Game State**

**GET** `/api/game/state`

```json
Response (200):
{
    "game": { ... },
    "grid": [ 
        [
            {
                "country": "Canada",
                "flag": "🇨🇦",
                "display": "❓",
                "is_matched": false,
                "is_flipped": false
            },
            ...
        ],
        ...
    ]
}
```

### **3. Flip Card**

**POST** `/api/game/flip`

```json
Request:
{
    "row": 0,
    "col": 1
}

Response (200):
{
    "success": true,
    "result": {
        "card": {
            "country": "Canada",
            "flag": "🇨🇦"
        },
        "flipped_count": 1,
        "is_matched": false,
        "is_game_won": false
    },
    "grid": [ ... ],
    "game": { ... }
}

Error Response (400):
{
    "success": false,
    "error": "Position (0, 0) is out of bounds"
}
```

### **4. Reset Non-Matching Cards**

**POST** `/api/game/reset`

Called after delay when cards don't match.

```json
Response (200):
{
    "success": true,
    "grid": [ ... ],
    "game": { ... }
}
```

### **5. Delete Game Session**

**DELETE** `/api/game/delete`

```json
Response (200):
{
    "success": true
}
```

### **6. Health Check**

**GET** `/api/health`

```json
Response (200):
{
    "status": "ok",
    "service": "Memory Match Arena API",
    "version": "1.0.0"
}
```

---

## 🖥️ Frontend Features

### **Screens**

1. **Difficulty Selection** — Choose 4×4, 6×6, or 8×8
2. **Game Screen** — Grid, stats, buttons
3. **Win Screen** — Celebrate with stats display

### **Interactive Elements**

- 🎨 **Color-coded cards**:
  - Blue (❓) = Hidden
  - Light blue (🇨🇦) = Revealed
  - Green (🇨🇦) = Matched
  
- 📊 **Live stats**:
  - Grid size
  - Pairs found / Needed
  - Move count

- ⏱️ **Auto-delay**:
  - 2-second wait for non-matches
  - Cards flip back automatically

### **Responsive Design**

- Works on desktop, tablet, mobile
- Adaptive grid sizing
- Touch-friendly buttons

---

## 🔧 Session Management

### **How Sessions Work**

1. **Session ID assigned** on first game start (stored in browser cookie)
2. **Game state stored** on server (in-memory)
3. **Requests include session ID** automatically (browser cookie)
4. **Each user has separate game instance**

### **Session Data Structure**

```python
GAME_SESSIONS = {
    "uuid-session-id": Game(size=4, card_pairs=...),
    "another-uuid": Game(size=6, card_pairs=...),
    ...
}
```

### **Production Note**

For production, replace in-memory storage with:
- **Redis** — For distributed sessions
- **PostgreSQL/MongoDB** — For persistence
- **AWS DynamoDB** — For serverless deployments

---

## 🧪 Testing the API

### **Quick curl commands**

```bash
# Health check
curl http://localhost:5000/api/health

# Start new game
curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"size": 4}'

# Get game state
curl http://localhost:5000/api/game/state

# Flip a card (row 0, col 1)
curl -X POST http://localhost:5000/api/game/flip \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 1}'

# Reset non-matching
curl -X POST http://localhost:5000/api/game/reset

# Delete session
curl -X DELETE http://localhost:5000/api/game/delete
```

---

## 📱 Browser Compatibility

✅ Chrome 90+  
✅ Firefox 88+  
✅ Safari 14+  
✅ Edge 90+  
✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🐛 Troubleshooting

### **"Connection refused" or "localhost:5000 refused"**
- Make sure server is running: `python src/web_backend.py`
- Check port 5000 isn't already in use

### **"Module not found: flask"**
- Install dependencies: `pip install -r requirements.txt`

### **Cards not flipping**
- Check browser console (F12) for errors
- Verify server is running and responding to API calls

### **Session lost after refresh**
- Browser cookies might be disabled
- Check browser privacy settings

---

## 🚀 Advanced Configuration

### **Change Port**

```python
# At bottom of web_backend.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
```

### **Enable CORS (for external domains)**

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```

### **Add Authentication**

```python
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
```

---

## 📊 Stage Comparison: All 3 Stages

| Aspect | Stage 1 (Console) | Stage 2 (Desktop) | Stage 3 (Web) |
|--------|------------------|------------------|---------------|
| **Technology** | Bash/Terminal | Tkinter | Flask + HTML/JS |
| **Interaction** | Text input | Mouse clicks | Browser clicks |
| **Delay Model** | `time.sleep()` | `after()` | `setTimeout()` |
| **Session State** | Local | Local | Server-side |
| **Platforms** | All | Desktop | All browsers |
| **Core Engine Reuse** | 100% ✅ | 100% ✅ | 100% ✅ |
| **Lines of Code** | 700 | 450 | 800+ |

---

## 🎯 Implementation Highlights

### **Server-Side (Flask)**

- Session-based game management
- RESTful API endpoints
- JSON request/response handling
- Error handling and validation

### **Client-Side (JavaScript)**

- Event-driven UI
- Non-blocking async/await for delays
- Real-time grid rendering
- State synchronization

### **Core Engine (Unchanged)**

```python
# Same code used in all 3 stages!
game = Game(size=4, card_pairs=CARD_PAIRS)
result = game.flip_card(row, col)
game.reset_non_matching_flips()
```

---

## ✅ Acceptance Criteria Met

✅ **Game runs in browser**  
✅ **Core engine reused without modification**  
✅ **Interactive card flipping**  
✅ **Game state persists correctly**  
✅ **Match/mismatch logic with 2-sec delay**  
✅ **Win detection functional**  
✅ **Responsive UI (desktop + mobile)**  
✅ **Session management**  
✅ **REST API architecture**  
✅ **Production-ready error handling**  

---

## 🎉 Bonus Features

**Optional enhancements to add:**

- 🏆 Leaderboard (store scores in DB)
- 👥 Multiplayer mode (WebSocket support)
- 🎵 Sound effects (click, match, win)
- 🎨 Themes (dark mode, color schemes)
- 📊 Statistics (best scores, play history)
- 🌍 Internationalization (multiple languages)
- 🔒 User authentication
- 📱 PWA (Progressive Web App) support

---

## 📖 Summary

**Memory Match Arena** now has three complete implementations:

1. ✅ **Console** — Text-based, complete game logic
2. ✅ **Desktop** — Tkinter GUI, responsive
3. ✅ **Web** — Browser-based, production-ready

**All three reuse the same core engine without modification!**

This demonstrates enterprise-level software architecture: **single business logic layer serving multiple UI platforms**.

---

Happy playing! 🎮🌟
