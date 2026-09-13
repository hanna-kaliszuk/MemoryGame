import { MemoryGame } from './game';
import { Board } from './board';
import { LEVELS } from './config';

declare const isAuthenticated: boolean;

let currentGame: MemoryGame | null = null;
let currentBoard: Board | null = null;
let gameUpdateInterval: ReturnType<typeof setInterval> | null = null;
let currentLevel: number | null = null;
let resultSaved = false;
let sseConnection: EventSource | null = null;

document.addEventListener('DOMContentLoaded', () => {
    const levelButtons = document.querySelectorAll<HTMLButtonElement>('.level-btn');

    levelButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const level = Number(button.dataset.level);
            startGame(level);
        });
    });

    const closeModalButton = document.getElementById('close-modal-btn');
    const okModalButton = document.getElementById('modal-ok-btn');

    const closeModal = (): void => {
        const modal = document.getElementById('retro-modal');

        if (modal) {
            modal.style.display = 'none';
        }
    };

    closeModalButton?.addEventListener('click', closeModal);
    okModalButton?.addEventListener('click', returnToLevelSelection);
});

function startGame(level: number): void {
    if (!isAuthenticated) {
        window.location.href = '/accounts/login/';
        return;
    }

    const config = LEVELS[level];

    if (!config) {
        return;
    }

    resultSaved = false;

    currentLevel = level;
    currentGame = new MemoryGame(config.pairs, config.timeLimit);
    currentBoard = new Board('game-board', currentGame, config.rows, config.columns);

    connectToLiveRanking(level);

    const levelSelection = document.getElementById('level-selection');
    const gameContent = document.getElementById('game-content');
    const currentLevelDisplay = document.getElementById('current-level-display');

    if (levelSelection) {
        levelSelection.style.display = 'none';
    }

    if (gameContent) {
        gameContent.style.display = 'block';
    }

    if (currentLevelDisplay) {
        currentLevelDisplay.textContent = level.toString();
    }

    currentBoard.render();

    gameUpdateInterval = setInterval(() => {
        currentBoard?.updateStats();

        if (currentGame?.isGameOver() && !resultSaved) {
            resultSaved = true;

            if (currentGame.isFinished()) {
                saveGameResult();
            }

            showGameOverModal();
        }
    }, 1000);
}

function returnToLevelSelection(): void {
    if (gameUpdateInterval !== null) {
        clearInterval(gameUpdateInterval);
        gameUpdateInterval = null;
    }

    if (sseConnection !== null) {
        sseConnection.close();
        sseConnection = null;
    }

    currentGame?.stopTimer();

    const levelSelection = document.getElementById('level-selection');
    const gameContent = document.getElementById('game-content');
    const modal = document.getElementById('retro-modal');

    if (levelSelection) {
        levelSelection.style.display = 'block';
    }

    if (gameContent) {
        gameContent.style.display = 'none';
    }

    if (modal) {
        modal.style.display = 'none';
    }

    currentGame = null;
    currentBoard = null;
}

function getCookie(name: string): string | null {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

async function saveGameResult(): Promise<void> {
    if (currentGame === null || currentLevel === null) {
        return;
    }

    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
        console.warn('CSRF token not found.');
        return;
    }

    try {
        const response = await fetch('/api/results/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                level: currentLevel,
                score: currentGame.getScore(),
            }),
        });

        if (response.ok) {
            console.log('Game result saved.');
        } else {
            console.error(
                'Failed to save game result:',
                await response.text()
            );
        }
    } catch (error) {
        console.error('Network error while saving game result:', error);
    }
}

function showGameOverModal(): void {
    const modal = document.getElementById('retro-modal');
    const message = document.getElementById('modal-message');

    if (!modal || !message || !currentGame) {
        return;
    }

    if (currentGame.isFinished()) {
        message.textContent =
            `You won! Your score: ${currentGame.getScore()} p`;
    } else {
        message.textContent = 'Time is up! You lost.';
    }

    modal.style.display = 'block';
}

function connectToLiveRanking(level: number): void {
    if (sseConnection !== null) {
        sseConnection.close();
    }

    const levelDisplay = document.getElementById('current-level-display');

    if (levelDisplay) {
        levelDisplay.textContent = level.toString();
    }

    sseConnection = new EventSource(
        `/api/ranking/stream/${level}/`
    );

    sseConnection.onmessage = (event: MessageEvent): void => {
        const scores = JSON.parse(event.data) as Array<{
            username: string;
            score: number;
        }>;

        const listElement = document.getElementById('live-scores-list');

        if (!listElement) {
            return;
        }

        listElement.innerHTML = '';

        if (scores.length === 0) {
            listElement.textContent = 'No scores yet.';
            return;
        }

        scores.forEach((result, index) => {
            const entry = document.createElement('div');

            entry.textContent =
                `${index + 1}. ${result.username}: ${result.score} p`;

            listElement.appendChild(entry);
        });
    };

    sseConnection.onerror = (): void => {
        console.warn('SSE connection error.');
    };
}