export interface Card {
    id: number;
    pairId: number;
    isRevealed: boolean;
    isMatched: boolean;
}

export class MemoryGame {
    private cards: Card[] = [];
    private firstCard: Card | null = null;
    private secondCard: Card | null = null;

    private score = 0;
    private mistakes = 0;
    private matchedPairs = 0;
    private remainingTime: number;

    constructor(
        private readonly pairs: number,
        timeLimit: number,
    ) {
        this.remainingTime = timeLimit;
        this.cards = this.createCards();
        this.shuffleCards();
    }

    private createCards(): Card[] {
        const cards: Card[] = [];

        for (let pairId = 0; pairId < this.pairs; pairId++) {
            cards.push(
                {
                    id: cards.length,
                    pairId,
                    isRevealed: false,
                    isMatched: false,
                },
                {
                    id: cards.length + 1,
                    pairId,
                    isRevealed: false,
                    isMatched: false,
                },
            );
        }

        return cards;
    }

    private shuffleCards(): void {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));

            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    public getCards(): Card[] {
        return this.cards;
    }
}