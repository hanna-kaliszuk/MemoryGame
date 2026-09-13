import { MemoryGame } from './game';
import { Board } from './board';
import { LEVELS } from './config';

let currentGame: MemoryGame | null = null;
let currentBoard: Board | null = null;

document.addEventListener('DOMContentLoaded', () => {
    const levelButtons = document.querySelectorAll<HTMLButtonElement>('.level-btn');

    levelButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const level = Number(button.dataset.level);
            startGame(level);
        });
    });
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
}