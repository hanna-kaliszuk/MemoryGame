import { MemoryGame } from "./game.js";
import { LEVELS } from "./config.js";

const level = LEVELS[1];

const game = new MemoryGame(level.pairs, level.timeLimit);

console.log(game.getCards());