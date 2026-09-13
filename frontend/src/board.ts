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

    constructor(containerId: string, game: MemoryGame) {
        const element = document.getElementById(containerId);

        if (!element) {
            throw new Error(`Nie znaleziono kontenera o ID: ${containerId}`);
        }

        this.container = element;
        this.game = game;
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
        const columns = Math.ceil(Math.sqrt(cards.length));

        this.container.style.display = 'grid';
        this.container.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

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