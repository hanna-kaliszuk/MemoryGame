import { MemoryGame } from "./game.js";

const game = new MemoryGame(2, 10);
const cards = game.getCards();

// Find two cards from different pairs.
const firstCard = cards[0];
const secondCard = cards.find(
    (card) => card.pairId !== firstCard.pairId,
)!;

console.log("First card:", firstCard);
console.log("Second card:", secondCard);

console.log("Reveal first:", game.revealCard(firstCard.id));
console.log("Reveal second:", game.revealCard(secondCard.id));

console.log("Match:", game.checkMatch());
console.log("Score immediately:", game.getScore());

console.log("Before reset:");
console.log("First revealed:", firstCard.isRevealed);
console.log("Second revealed:", secondCard.isRevealed);

setTimeout(() => {
    console.log("After 1 second:");
    console.log("First revealed:", firstCard.isRevealed);
    console.log("Second revealed:", secondCard.isRevealed);
    console.log("Score:", game.getScore());
}, 1100);