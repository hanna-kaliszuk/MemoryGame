export interface LevelConfig {
    rows: number;
    columns: number;
    pairs: number;
    timeLimit: number;
}

export const LEVELS: Record<number, LevelConfig> = {
    1: {
        rows: 4,
        columns: 4,
        pairs: 8,
        timeLimit: 60,
    },
    2: {
        rows: 4,
        columns: 6,
        pairs: 12,
        timeLimit: 90,
    },
    3: {
        rows: 6,
        columns: 6,
        pairs: 18,
        timeLimit: 120,
    },
    4: {
        rows: 6,
        columns: 8,
        pairs: 24,
        timeLimit: 150,
    },
};