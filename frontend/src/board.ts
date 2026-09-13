import {MemoryGame} from './game';

export class Board {
    private readonly container: HTMLElement;
    private readonly game: MemoryGame;
    private readonly emojis = [
        '🍎', '🍌', '🍇', '🍉',
        '🍓', '🍒', '🥝', '🍍',
        '🥑', '🍋', '🍊', '🥥',
        '🍑', '🍐', '🫐', '🥕',
        '🌽', '🍄', '🌻', '🌵',
        '🐶', '🐱', '🐭', '🐹',
    ];
    private readonly rows: number;
    private readonly columns: number;

    private firstCardFlipped = false;

    constructor(containerId: string, game: MemoryGame, rows: number, columns: number) {
        const element = document.getElementById(containerId);

        if (!element) {
            throw new Error(`Nie znaleziono kontenera o ID: ${containerId}`);
        }

        this.container = element;
        this.game = game;
        this.rows = rows;
        this.columns = columns;
    }

    public updateStats(): void {
        const scoreElement = document.getElementById('game-score');
        const timerElement = document.getElementById('game-timer');

        if (scoreElement) {
            scoreElement.textContent = `${this.game.getScore()} p`;
        }

        if (timerElement) {
            timerElement.textContent = `${this.game.getRemainingTime()}s`;
        }
    }

    public render(): void {
        this.updateStats();

        this.container.innerHTML = '';

        const cards = this.game.getCards();

        this.container.style.display = 'grid';
        this.container.style.gridTemplateColumns = `repeat(${this.columns}, 1fr)`;

        cards.forEach((card) => {
            const cardElement = document.createElement('div');

            cardElement.classList.add('card');
            if (card.isRevealed || card.isMatched) {
                    cardElement.textContent = this.emojis[card.pairId];
            }

            if (card.isRevealed) {
                cardElement.classList.add('flipped');
            }

            if (card.isMatched) {
                cardElement.classList.add('matched');
            }

            cardElement.dataset.id = card.id.toString();

            cardElement.addEventListener('click', () => {
                const cardId = Number(cardElement.dataset.id);

                if (!this.game.revealCard(cardId)) {
                    return;
                }

                if (!this.firstCardFlipped) {
                    this.game.startTimer();
                    this.firstCardFlipped = true;
                }

                this.render();

                const result = this.game.checkMatch();

                if (result !== null) {
                    this.render();

                    if (result === false) {
                        setTimeout(() => {
                            this.render();
                        }, 1000);
                    }
                }
            });

            this.container.appendChild(cardElement);
        });
    }

    public isGameOver(): boolean {
        return this.game.isGameOver();
    }

}