export type ActionData =
    | {
        type: "hand";
        slot: number;
    }
    | {
        type: "board";
        pos: number[];
    }
    | {
        type: "rotate";
        rotation: number;
    }
    | {
        type: "button";
        name: string;
    };