import { MemoryGame } from './game';

export class Board {
    private readonly container: HTMLElement;
    private readonly game: MemoryGame;

    constructor(containerId: string, game: MemoryGame) {
        const element = document.getElementById(containerId);

        if (!element) {
            throw new Error(`Could not find container with ID: ${containerId}`);
        }

        this.container = element;
        this.game = game;
    }

    public render(): void {
        this.container.innerHTML = '';

        const cards = this.game.getCards();
        const columns = Math.ceil(Math.sqrt(cards.length));

        this.container.style.display = 'grid';
        this.container.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;

        cards.forEach((card) => {
            const cardElement = document.createElement('div');

            cardElement.classList.add('card');

            if (card.isRevealed) {
                cardElement.classList.add('flipped');
            }

            if (card.isMatched) {
                cardElement.classList.add('matched');
            }

            cardElement.dataset.id = card.id.toString();

            this.container.appendChild(cardElement);
        });
    }
}