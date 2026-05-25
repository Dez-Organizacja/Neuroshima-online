import { WebSocketMessage } from "./websocketClient";

type UnitState = [string, string, number, number, boolean]

type BoardCellUnit = {
    x : number,
    y : number,
    value : UnitState
}

type BoardCellBoolean = {
    x : number,
    y : number,
    value : boolean,
}

type UIMode = "default" | "rotation" | "decision";

export type GameState = {
    view : {
        state : {
            fractions : string[];
            board : BoardCellUnit[];
            hands : Record<string, string[]>;
        }
        available_actions : {
            hand : Record<string, boolean[]>;
            board : BoardCellBoolean[];
        }
        ui_state : {
            fraction : string;
            mode : UIMode;
            message : string;
        }
    }
}

