export type Fraction =
    | "borgo"
    | "hegemonia"
    | "moloch"
    | "posterunek";

export type UIMode =
    | "default"
    | "rotation"
    | "decision";

export interface Unit {
    name: string;
    fraction: string;
    ROTATION: number;
    DAMAGE: number;
    WIRED: number;
    ability_used: boolean;
}

export interface BoardField {
    pos: number[];
    unit: Unit;
}

export interface HandData {
    tokens: string[];
}

export interface GameView {
    view: {
        state: {
            fractions: string[];

            board: BoardField[];

            hands: Record<string, HandData>;
        };

        availableActions: {
            hand: boolean[];

            board: number[][];

            buttons: string[];
        };

        uiState: {
            fraction: string;

            mode: string;

            message: string;
        };
    };
}