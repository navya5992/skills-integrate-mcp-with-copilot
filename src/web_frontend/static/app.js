/**
 * Memory Match Arena - Web Frontend
 * 
 * Client-side game logic and API communication.
 * Communicates with Flask backend for game engine calls.
 */

class MemoryMatchGame {
    constructor() {
        this.gameSize = 4;
        this.flippedCards = [];
        this.canFlip = true;
        this.gameEnded = false;
        this.flipDelay = 2000; // 2 seconds
        
        this.initElements();
        this.attachEventListeners();
    }
    
    initElements() {
        // Screens
        this.difficultyScreen = document.getElementById('difficultyScreen');
        this.gameScreen = document.getElementById('gameScreen');
        this.winScreen = document.getElementById('winScreen');
        
        // Difficulty screen
        this.startBtn = document.getElementById('startBtn');
        this.difficultyRadios = document.querySelectorAll('input[name="difficulty"]');
        
        // Game screen
        this.gameGrid = document.getElementById('gameGrid');
        this.gridSizeDisplay = document.getElementById('gridSize');
        this.pairsDisplay = document.getElementById('pairsCount');
        this.movesDisplay = document.getElementById('movesCount');
        this.messageEl = document.getElementById('message');
        this.newGameBtn = document.getElementById('newGameBtn');
        this.quitBtn = document.getElementById('quitBtn');
        
        // Win screen
        this.winGridSizeDisplay = document.getElementById('winGridSize');
        this.winMovesDisplay = document.getElementById('winMoves');
        this.winPairsDisplay = document.getElementById('winPairs');
        this.playAgainBtn = document.getElementById('playAgainBtn');
        this.quitWinBtn = document.getElementById('quitWinBtn');
    }
    
    attachEventListeners() {
        this.startBtn.addEventListener('click', () => this.handleStartGame());
        this.newGameBtn.addEventListener('click', () => this.goToDifficultScreen());
        this.quitBtn.addEventListener('click', () => this.quit());
        this.playAgainBtn.addEventListener('click', () => this.goToDifficultScreen());
        this.quitWinBtn.addEventListener('click', () => this.quit());
    }
    
    handleStartGame() {
        const selectedSize = document.querySelector('input[name="difficulty"]:checked').value;
        this.gameSize = parseInt(selectedSize);
        this.startGame();
    }
    
    async startGame() {
        this.flippedCards = [];
        this.canFlip = true;
        this.gameEnded = false;
        
        try {
            const response = await fetch('/api/game/new', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ size: this.gameSize })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                alert(`Error: ${data.error}`);
                return;
            }
            
            this.showGameScreen();
            this.renderGrid(data.grid, data.game);
            this.updateStats(data.game);
            
        } catch (error) {
            console.error('Error starting game:', error);
            alert('Failed to start game');
        }
    }
    
    async handleCardClick(row, col) {
        if (!this.canFlip || this.gameEnded) return;
        
        this.canFlip = false;
        
        try {
            const response = await fetch('/api/game/flip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ row, col })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                this.showMessage(`❌ ${data.error}`, 'error');
                this.canFlip = true;
                return;
            }
            
            // Update grid
            this.renderGrid(data.grid, data.game);
            this.updateStats(data.game);
            
            const result = data.result;
            this.flippedCards.push({ row, col, matched: result.is_matched });
            
            // If 2 cards flipped
            if (result.flipped_count === 2) {
                if (result.is_matched) {
                    this.showMessage('✅ Match found!', 'success');
                    await this.delay(500);
                    this.flippedCards = [];
                    this.canFlip = true;
                } else {
                    this.showMessage('❌ No match! Cards will flip back...', 'info');
                    await this.delay(this.flipDelay);
                    await this.resetNonMatching();
                }
            } else {
                this.canFlip = true;
            }
            
            // Check for win
            if (result.is_game_won) {
                this.gameEnded = true;
                this.showMessage('🎉 YOU WON! 🎉', 'success');
                await this.delay(1000);
                this.showWinScreen(data.game);
            }
            
        } catch (error) {
            console.error('Error flipping card:', error);
            this.showMessage('Failed to flip card', 'error');
            this.canFlip = true;
        }
    }
    
    async resetNonMatching() {
        try {
            const response = await fetch('/api/game/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.renderGrid(data.grid, data.game);
                this.updateStats(data.game);
                this.flippedCards = [];
                this.canFlip = true;
                this.showMessage('', '');
            }
            
        } catch (error) {
            console.error('Error resetting cards:', error);
            this.canFlip = true;
        }
    }
    
    renderGrid(gridData, gameData) {
        // Clear and set grid class
        this.gameGrid.innerHTML = '';
        this.gameGrid.className = `game-grid size-${gameData.size}x${gameData.size}`;
        
        // Render cards
        gridData.forEach((row, rowIdx) => {
            row.forEach((card, colIdx) => {
                const cardEl = document.createElement('div');
                cardEl.className = 'card';
                
                // Determine state
                if (card.is_matched) {
                    cardEl.classList.add('matched');
                } else if (card.is_flipped) {
                    cardEl.classList.add('flipped');
                }
                
                // Set display
                if (card.is_matched || card.is_flipped) {
                    if (card.display_type === 'flag') {
                        // Show flag image
                        const img = document.createElement('img');
                        img.src = card.flag_image_url;
                        img.alt = card.country;
                        img.className = 'flag-image';
                        cardEl.appendChild(img);
                    } else {
                        // Show country name
                        cardEl.textContent = card.country;
                        cardEl.className += ' country-name';
                    }
                } else {
                    // Show question mark
                    cardEl.textContent = '?';
                }
                
                // Add click handler
                cardEl.addEventListener('click', () => this.handleCardClick(rowIdx, colIdx));
                
                // Disable if matched
                if (card.is_matched) {
                    cardEl.style.cursor = 'default';
                }
                
                this.gameGrid.appendChild(cardEl);
            });
        });
    }
    
    updateStats(gameData) {
        this.gridSizeDisplay.textContent = `${gameData.size}×${gameData.size}`;
        this.pairsDisplay.textContent = `${gameData.pairs_found}/${gameData.pairs_needed}`;
        this.movesDisplay.textContent = gameData.moves;
    }
    
    showMessage(message, type) {
        this.messageEl.textContent = message;
        this.messageEl.className = 'message';
        if (type) {
            this.messageEl.classList.add(type);
        }
    }
    
    showGameScreen() {
        this.difficultyScreen.classList.remove('active');
        this.gameScreen.classList.add('active');
        this.winScreen.classList.remove('active');
        this.showMessage('', '');
    }
    
    goToDifficultScreen() {
        this.difficultyScreen.classList.add('active');
        this.gameScreen.classList.remove('active');
        this.winScreen.classList.remove('active');
    }
    
    showWinScreen(gameData) {
        this.winGridSizeDisplay.textContent = `${gameData.size}×${gameData.size}`;
        this.winMovesDisplay.textContent = gameData.moves;
        this.winPairsDisplay.textContent = `${gameData.pairs_found}/${gameData.pairs_needed}`;
        
        this.gameScreen.classList.remove('active');
        this.winScreen.classList.add('active');
    }
    
    quit() {
        if (confirm('Are you sure you want to quit?')) {
            window.location.reload();
        }
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.game = new MemoryMatchGame();
});
