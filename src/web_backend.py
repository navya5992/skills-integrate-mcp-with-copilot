"""
Web Backend for Memory Match Arena (Flask)

RESTful API for the web-based Memory Match Game.
Reuses core game engine (game_engine.py) without modification.
Handles session management and game state persistence.
"""

from flask import Flask, render_template, request, jsonify, session
from functools import wraps
import uuid
import os
import socket
from memory_game.game_engine import Game, InvalidMoveError
from memory_game.card_data import CARD_PAIRS

app = Flask(__name__, template_folder='web_frontend', static_folder='web_frontend/static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Store active game sessions
# In production, use Redis or database
GAME_SESSIONS = {}


def get_session_id():
    """Get or create session ID for user."""
    if 'game_session_id' not in session:
        session['game_session_id'] = str(uuid.uuid4())
    return session['game_session_id']


def get_local_network_ip():
    """Get the local network IP address."""
    try:
        # Try to get the local IP by connecting to a remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_user_game(session_id: str) -> Game:
    """Get game instance for session, create if doesn't exist."""
    if session_id not in GAME_SESSIONS:
        raise ValueError(f"No game session found: {session_id}")
    return GAME_SESSIONS[session_id]


def require_session(f):
    """Decorator to ensure valid session exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session_id = get_session_id()
            return f(session_id, *args, **kwargs)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
    return decorated_function


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/play')
@app.route('/game')
def play_game():
    """Alias routes for the main game page."""
    return render_template('index.html')


@app.route('/api/server-info', methods=['GET'])
def server_info():
    """
    Get server information for mobile access.
    
    Returns:
    {
        "local_ip": "10.0.4.242",
        "port": 5000,
        "localhost_url": "http://127.0.0.1:5000",
        "network_url": "http://10.0.4.242:5000",
        "mobile_instructions": "...",
        "recommended_mobile_url": "http://localhost:5000"
    }
    """
    local_ip = get_local_network_ip()
    port = 5000
    
    # Check if we're in a dev container (common indicators)
    in_dev_container = (
        local_ip.startswith('10.') or  # Docker bridge network
        local_ip.startswith('172.') or # Docker bridge network  
        '/workspaces/' in os.getcwd()  # VS Code dev container
    )
    
    if in_dev_container:
        mobile_instructions = (
            "📱 MOBILE ACCESS IN DEV CONTAINER:\n"
            "1. In VS Code: Ctrl+Shift+P → 'Ports: Focus on Ports View'\n"
            "2. Forward port 5000 to localhost\n"
            "3. Use the forwarded localhost URL on mobile\n"
            "4. Make sure mobile device is on same WiFi as host"
        )
        recommended_mobile_url = f"http://localhost:{port}"
    else:
        mobile_instructions = "📱 Use the network URL on your mobile device (same WiFi network)"
        recommended_mobile_url = f"http://{local_ip}:{port}"
    
    return jsonify({
        "local_ip": local_ip,
        "port": port,
        "localhost_url": f"http://127.0.0.1:{port}",
        "network_url": f"http://{local_ip}:{port}",
        "mobile_instructions": mobile_instructions,
        "recommended_mobile_url": recommended_mobile_url,
        "in_dev_container": in_dev_container
    }), 200


@app.route('/api/game/new', methods=['POST'])
def new_game():
    """
    Start a new game.
    
    Expected JSON:
    {
        "size": 4  // 4, 6, or 8
    }
    
    Returns:
    {
        "session_id": "uuid",
        "game": { grid_size, pairs_needed, ... },
        "grid": [ ... ]
    }
    """
    try:
        data = request.get_json()
        size = int(data.get('size', 4))
        
        if size not in (4, 6, 8):
            return jsonify({"error": "Invalid grid size. Must be 4, 6, or 8"}), 400
        
        session_id = get_session_id()
        game = Game(size=size, card_pairs=CARD_PAIRS)
        GAME_SESSIONS[session_id] = game
        
        return jsonify({
            "session_id": session_id,
            "game": {
                "size": game.size,
                "pairs_needed": game.pairs_needed,
                "pairs_found": game.pairs_found,
                "moves": game.move_count,
                "is_won": game.is_won
            },
            "grid": get_grid_state(game)
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/game/state', methods=['GET'])
@require_session
def get_game_state(session_id):
    """
    Get current game state.
    
    Returns:
    {
        "game": { ... },
        "grid": [ ... ]
    }
    """
    try:
        game = get_user_game(session_id)
        return jsonify({
            "game": {
                "size": game.size,
                "pairs_needed": game.pairs_needed,
                "pairs_found": game.pairs_found,
                "moves": game.move_count,
                "is_won": game.is_won,
                "state": game.state.value
            },
            "grid": get_grid_state(game)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/game/flip', methods=['POST'])
@require_session
def flip_card(session_id):
    """
    Flip a card.
    
    Expected JSON:
    {
        "row": 0,
        "col": 1
    }
    
    Returns:
    {
        "success": true,
        "result": {
            "card": { country, flag },
            "flipped_count": 1,
            "is_matched": false,
            "is_game_won": false
        },
        "grid": [ ... ],
        "game": { ... }
    }
    """
    try:
        game = get_user_game(session_id)
        data = request.get_json()
        row = int(data.get('row', -1))
        col = int(data.get('col', -1))
        
        # Flip the card using core engine
        result = game.flip_card(row, col)
        
        return jsonify({
            "success": True,
            "result": {
                "card": {
                    "country": result.card.country,
                    "flag": result.card.flag,
                    "country_code": result.card.country_code,
                    "flag_image_url": result.card.flag_image_url,
                    "display_type": result.card.display_type
                },
                "flipped_count": result.flipped_count,
                "is_matched": result.is_matched,
                "is_game_won": result.is_game_won
            },
            "grid": get_grid_state(game),
            "game": {
                "size": game.size,
                "pairs_needed": game.pairs_needed,
                "pairs_found": game.pairs_found,
                "moves": game.move_count,
                "is_won": game.is_won,
                "state": game.state.value
            }
        }), 200
    
    except InvalidMoveError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/game/reset', methods=['POST'])
@require_session
def reset_nonmatching(session_id):
    """
    Reset non-matching cards (flip them back).
    Called after delay when cards don't match.
    
    Returns:
    {
        "success": true,
        "grid": [ ... ],
        "game": { ... }
    }
    """
    try:
        game = get_user_game(session_id)
        game.reset_non_matching_flips()
        
        return jsonify({
            "success": True,
            "grid": get_grid_state(game),
            "game": {
                "size": game.size,
                "pairs_needed": game.pairs_needed,
                "pairs_found": game.pairs_found,
                "moves": game.move_count,
                "is_won": game.is_won,
                "state": game.state.value
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/game/delete', methods=['DELETE'])
@require_session
def delete_game(session_id):
    """Delete game session."""
    try:
        if session_id in GAME_SESSIONS:
            del GAME_SESSIONS[session_id]
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_grid_state(game: Game) -> list:
    """
    Get visual representation of grid for frontend.
    
    Returns:
    [
        [
            {
                "country": "Canada",
                "flag": "🇨🇦",
                "display": "🇨🇦"  # What to show (?, flag, or empty)
            },
            ...
        ],
        ...
    ]
    """
    grid_state = []
    for row in range(game.size):
        row_state = []
        for col in range(game.size):
            card = game.grid.get_card(row, col)
            display = game.get_card_display(row, col)
            
            row_state.append({
                "country": card.country,
                "flag": card.flag,
                "country_code": card.country_code,
                "flag_image_url": card.flag_image_url,
                "display_type": card.display_type,
                "display": display,
                "is_matched": card.is_matched,
                "is_flipped": card.is_flipped
            })
        grid_state.append(row_state)
    
    return grid_state


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "Memory Match Arena API",
        "version": "1.0.0"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
