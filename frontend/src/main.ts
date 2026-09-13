import { MemoryGame } from './game';
import { Board } from './board';
import { LEVELS } from './config';

let currentGame: MemoryGame | null = null;
let currentBoard: Board | null = null;
let gameUpdateInterval: ReturnType<typeof setInterval> | null = null;

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
    const config = LEVELS[level];

    if (!config) {
        return;
    }

    currentGame = new MemoryGame(config.pairs, config.timeLimit);
    currentBoard = new Board('game-board', currentGame);

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
    currentGame.startTimer();

    gameUpdateInterval = setInterval(() => {
        currentBoard?.updateStats();

        if (currentGame?.isGameOver()) {
            showGameOverModal();
        }
    }, 1000);
}

function returnToLevelSelection(): void {
    if (gameUpdateInterval !== null) {
        clearInterval(gameUpdateInterval);
        gameUpdateInterval = null;
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

function showGameOverModal(): void {
    const modal = document.getElementById('retro-modal');
    const message = document.getElementById('modal-message');

    if (!modal || !message || !currentGame) {
        return;
    }

    message.textContent = `Game over! Your score: ${currentGame.getScore()} p`;

    modal.style.display = 'block';
}