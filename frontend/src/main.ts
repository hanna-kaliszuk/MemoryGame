import { MemoryGame } from "./game.js";
import { LEVELS } from "./config.js";

const level = LEVELS[1];

const game = new MemoryGame(level.pairs, level.timeLimit);

console.log(game.getCards());
console.log(game.revealCard(0));
console.log(game.getCards());

game.revealCard(1);
game.revealCard(2);
console.log(game.checkMatch());